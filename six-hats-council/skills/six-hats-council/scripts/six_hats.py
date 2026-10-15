#!/usr/bin/env python3
"""
Six Hats Council & MAGI System - Deliberation & Consensus CLI Runner.
Executes:
1. Edward de Bono's 6 Thinking Hats methodology.
2. Evangelion MAGI Supercomputer Tripartite Consensus (Melchior-1, Balthasar-2, Casper-3).

Can operate with local LLM CLIs (gemini, ollama, claude, codex) or generate structured
deliberation prompts.
"""

import os
import re
import sys
import shutil
import argparse
import subprocess
from typing import Dict, Tuple, Optional, List

# Ensure standard UTF-8 output on Windows
if sys.platform.startswith("win"):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

HATS = [
    {
        "id": "white",
        "name": "Sombrero Blanco",
        "emoji": "⚪",
        "focus": "Hechos, Datos, Métricas y Restricciones Objetivas (sin opiniones)",
        "prompt": (
            "Eres el Sombrero Blanco de Edward de Bono. Expón ÚNICAMENTE los hechos objetivos, "
            "datos verificables, restricciones técnicas y qué datos críticos faltan sobre el "
            "siguiente problema. Prohibido emitir juicios o valoraciones personales:\n\n{topic}"
        )
    },
    {
        "id": "red",
        "name": "Sombrero Rojo",
        "emoji": "🔴",
        "focus": "Intuición, Gut Feeling, Sentimientos del Dev y UX del Usuario",
        "prompt": (
            "Eres el Sombrero Rojo de Edward de Bono. Expresa sensaciones viscerales, corazonadas "
            "técnicas y percepción de experiencia de usuario o equipo sobre el siguiente problema. "
            "No requieres justificación lógica ni demostración formal:\n\n{topic}"
        )
    },
    {
        "id": "green",
        "name": "Sombrero Verde",
        "emoji": "🟢",
        "focus": "Creatividad, Pensamiento Lateral y Alternativas Radicales",
        "prompt": (
            "Eres el Sombrero Verde de Edward de Bono. Propón al menos 2 soluciones no convencionales, "
            "enfoques laterales o alternativas disruptivas que desafíen los supuestos habituales para:\n\n{topic}"
        )
    },
    {
        "id": "black",
        "name": "Sombrero Negro",
        "emoji": "⚫",
        "focus": "Riesgos Críticos, Puntos de Fallo, Seguridad y Abogado del Diablo",
        "prompt": (
            "Eres el Sombrero Negro de Edward de Bono. Actúa como el auditor más implacable y abogado del diablo. "
            "¿Por qué esta solución va a fallar? Señala vulnerabilidades de seguridad, cuellos de botella, "
            "deuda técnica y costes ocultos para:\n\n{topic}"
        )
    },
    {
        "id": "yellow",
        "name": "Sombrero Amarillo",
        "emoji": "🟡",
        "focus": "Optimismo Lógico, Beneficios, Valor Agregado y Condiciones de Éxito",
        "prompt": (
            "Eres el Sombrero Amarillo de Edward de Bono. Expón el valor positivo genuino, el mejor escenario "
            "viable y las ventajas competitivas de abordar con éxito el siguiente problema:\n\n{topic}"
        )
    },
    {
        "id": "blue",
        "name": "Sombrero Azul",
        "emoji": "🔵",
        "focus": "Síntesis Ejecutiva, Resolución de Tensiones y Plan de Acción",
        "prompt": (
            "Eres el Sombrero Azul y Facilitador Ejecutivo. Teniendo en cuenta la deliberación anterior, "
            "resuelve los conflictos entre el Sombrero Negro (riesgos) y el Verde/Amarillo (innovación y valor), "
            "y elabora un PLAN DE IMPLEMENTACIÓN DEFINITIVO por fases para:\n\n{topic}"
        )
    }
]

MAGI_NODES = [
    {
        "id": "melchior",
        "name": "MELCHIOR-1",
        "archetype": "La Científica (⚪ Blanco + 🔵 Azul)",
        "emoji": "🧠",
        "focus": "Lógica formal, Deep Modules, complejidad O(n) y consistencia de dominio",
        "prompt": (
            "Eres MELCHIOR-1, el primer nodo del supercomputador MAGI de Evangelion. "
            "Representas a la Dra. Naoko Akagi como CIENTÍFICA: lógica matemática pura, coherencia arquitectónica y rigor estructural. "
            "Evalúa la modularidad profunda (Ousterhout), complejidad asintótica O(n) y principios de diseño de dominio el siguiente dilema:\n\n{topic}\n\n"
            "Concluye tu respuesta estrictamente en este formato:\n"
            "VOTO: [AGREED | DENIED | CONDITIONAL]\n"
            "MOTIVO: [Justificación concisa en 1 frase]\n"
            "ESTIPULACIONES: [Requisitos arquitectónicos no negociables si aplica]"
        )
    },
    {
        "id": "balthasar",
        "name": "BALTHASAR-2",
        "archetype": "La Madre / Guardián (⚫ Negro + 🔴 Rojo)",
        "emoji": "🛡️",
        "focus": "Seguridad radical, worst-case scenario, blast radius y reversibilidad",
        "prompt": (
            "Eres BALTHASAR-2, el segundo nodo del supercomputador MAGI de Evangelion. "
            "Representas a la Dra. Naoko Akagi como MADRE y PROTECTORA: preservación del sistema, aversión al riesgo y seguridad. "
            "Evalúa el peor escenario posible (worst-case), radio de explosión (blast radius), plan de rollback y testing determinista para:\n\n{topic}\n\n"
            "Concluye tu respuesta estrictamente en este formato:\n"
            "VOTO: [AGREED | DENIED | CONDITIONAL]\n"
            "MOTIVO: [Justificación concisa en 1 frase]\n"
            "ESTIPULACIONES: [Salvaguardas obligatorias si aplica]"
        )
    },
    {
        "id": "casper",
        "name": "CASPER-3",
        "archetype": "La Mujer / Disruptora (🟢 Verde + 🟡 Amarillo)",
        "emoji": "⚡",
        "focus": "Pragmatismo 80/20, UX delightful, pensamiento lateral y velocidad de entrega",
        "prompt": (
            "Eres CASPER-3, el tercer nodo del supercomputador MAGI de Evangelion. "
            "Representas a la Dra. Naoko Akagi como MUJER y DISRUPTORA: pragmatismo implacable, valor humano, experiencia de usuario y atajos laterales. "
            "Evalúa la regla 80/20, eliminación de código redundante y simplificación radical para:\n\n{topic}\n\n"
            "Concluye tu respuesta estrictamente en este formato:\n"
            "VOTO: [AGREED | DENIED | CONDITIONAL]\n"
            "MOTIVO: [Justificación concisa en 1 frase]\n"
            "ESTIPULACIONES: [Requisitos de simplicidad y UX si aplica]"
        )
    }
]


def detect_cli() -> Optional[str]:
    """Detect available LLM CLI runner in system PATH."""
    for cli in ["gemini", "ollama", "codex", "claude"]:
        if shutil.which(cli):
            return cli
    return None


def query_cli(cli_type: str, prompt: str, timeout: int = 90) -> Tuple[bool, str]:
    """Query local CLI with prompt."""
    try:
        if cli_type == "gemini":
            cmd = ["gemini", "-p", prompt]
        elif cli_type == "ollama":
            cmd = ["ollama", "run", "llama3", prompt]
        elif cli_type == "claude":
            cmd = ["claude", "-p", prompt]
        else:
            return False, f"CLI no soportado directamente: {cli_type}"

        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout
        )
        if res.returncode == 0:
            return True, res.stdout.strip()
        return False, f"Error {cli_type}: {res.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return False, f"Tiempo de espera agotado ({timeout}s) para {cli_type}"
    except Exception as exc:
        return False, f"Excepción ejecutando {cli_type}: {exc}"


def extract_vote(text: str) -> str:
    """Extract AGREED, DENIED, or CONDITIONAL from response text."""
    match = re.search(r"VOTO:\s*(AGREED|DENIED|CONDITIONAL)", text, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    if "AGREED" in text.upper():
        return "AGREED"
    if "DENIED" in text.upper():
        return "DENIED"
    if "CONDITIONAL" in text.upper():
        return "CONDITIONAL"
    return "PENDING"


def run_magi_deliberation(topic: str, cli_name: Optional[str] = None) -> str:
    """Run the tripartite MAGI consensus protocol."""
    active_cli = cli_name or detect_cli()
    responses: Dict[str, str] = {}
    votes: Dict[str, str] = {}

    print(f"[*] Iniciando Protocolo de Consenso MAGI (Evangelion)...")
    if active_cli:
        print(f"[*] Motor CLI detectado: {active_cli}")
    else:
        print("[!] No se detectó CLI interactivo. Generando prompts estructurados para subagentes.")

    for node in MAGI_NODES:
        print(f" -> Consultando nodo {node['name']} ({node['archetype']})...")
        formatted_prompt = node["prompt"].format(topic=topic)

        if active_cli:
            ok, response_text = query_cli(active_cli, formatted_prompt)
            if not ok:
                response_text = f"*(Error consultando a {node['name']}: {response_text})*"
                vote = "DENIED"
            else:
                vote = extract_vote(response_text)
        else:
            response_text = f"*(Prompt listo para subagente independiente)*\n> {formatted_prompt}"
            vote = "PENDING"

        responses[node["id"]] = response_text
        votes[node["id"]] = vote

    # Determinar consenso
    v_melchior = votes.get("melchior", "PENDING")
    v_balthasar = votes.get("balthasar", "PENDING")
    v_casper = votes.get("casper", "PENDING")

    approved_count = sum(1 for v in [v_melchior, v_balthasar, v_casper] if v in ["AGREED", "CONDITIONAL"])
    if approved_count == 3:
        consensus_title = "3-0 UNANIMOUS CONSENSUS (APROBADO POR UNANIMIDAD)"
    elif approved_count == 2:
        consensus_title = "2-1 MAJORITY DECISION (APROBADO POR MAYORÍA CON CONDICIONES)"
    elif approved_count <= 1 and all(v != "PENDING" for v in [v_melchior, v_balthasar, v_casper]):
        consensus_title = "REJECTED (VETO DE LA MAYORÍA DE NODOS)"
    else:
        consensus_title = "CONSENSUS GRID READY FOR SUBAGENTS"

    output = [
        "# 🔮 SISTEMA MAGI: PROTOCOLO DE DELIBERACIÓN TÁCTICA\n",
        "```",
        "╔══════════════════════════════════════════════════════════════════════╗",
        "║                       MAGI SUPERCOMPUTER SYSTEM                      ║",
        "║                     NERV TOKYO-3 ARCHITECTURE GRID                   ║",
        "╚══════════════════════════════════════════════════════════════════════╝",
        "```\n",
        f"**Dilema Técnico Analizado**: {topic}\n",
        f"**Estado del Consenso**: `{consensus_title}`\n",
        "---\n",
        "## 1. Matriz de Votación de Nodos Soberanos\n",
        "| Nodo MAGI | Arquetipo / Sombreros | Voto | Dictamen Principal |",
        "| :--- | :--- | :---: | :--- |",
        f"| **MELCHIOR-1** | 🧠 Científica (⚪ Blanco + 🔵 Azul) | **{v_melchior}** | Lógica formal y Deep Modules |",
        f"| **BALTHASAR-2** | 🛡️ Madre (⚫ Negro + 🔴 Rojo) | **{v_balthasar}** | Preservación y mitigación de riesgos |",
        f"| **CASPER-3** | ⚡ Mujer (🟢 Verde + 🟡 Amarillo) | **{v_casper}** | Pragmatismo 80/20 y experiencia de usuario |",
        "\n---\n",
        "## 2. Dictámenes Detallados de los Nodos\n"
    ]

    for node in MAGI_NODES:
        output.append(f"### {node['emoji']} {node['name']} ({node['archetype']})")
        output.append(responses[node["id"]] + "\n")

    output.append("---\n")
    output.append("## 3. Plan de Acción y Salvaguardas Vinculantes\n")
    if approved_count >= 2:
        output.append("- **Aprobado para implementación**: Proceder incorporando las salvaguardas obligatorias señaladas por los nodos disidentes o condicionales.")
        output.append("- **Registro en ADR**: Si la decisión es de alto coste de reversión, exportar a `docs/adr/`.")
    else:
        output.append("- **Acción requerida**: Reformular la propuesta técnica atacando las objeciones de los nodos que votaron DENIED antes de volver a consultar a MAGI.")

    return "\n".join(output)


def run_deliberation(topic: str, cli_name: Optional[str] = None) -> str:
    """Run the 6 hats deliberation sequence."""
    output_lines = [
        f"# 🎩 Consejo de los 6 Sombreros: Deliberación Técnica\n",
        f"**Tema analizado**: {topic}\n",
        f"---\n"
    ]

    responses: Dict[str, str] = {}
    active_cli = cli_name or detect_cli()

    print(f"[*] Iniciando Consejo de los 6 Sombreros...")
    if active_cli:
        print(f"[*] Motor CLI detectado: {active_cli}")
    else:
        print("[!] No se detectó un CLI interactivo (gemini, ollama, etc.). Generando informe estructurado de prompts.")

    for hat in HATS:
        hat_header = f"### {hat['emoji']} {hat['name']} ({hat['focus']})"
        print(f" -> Consultando {hat['name']}...")
        formatted_prompt = hat["prompt"].format(topic=topic)

        if active_cli:
            ok, response_text = query_cli(active_cli, formatted_prompt)
            if not ok:
                response_text = f"*(No se pudo consultar al motor CLI: {response_text})*"
        else:
            response_text = f"*(Prompt listo para deliberar en el modelo activo)*\n> {formatted_prompt}"

        responses[hat["id"]] = response_text
        output_lines.append(hat_header)
        output_lines.append(response_text + "\n")

    return "\n".join(output_lines)


def main():
    parser = argparse.ArgumentParser(
        description="Consejo de los 6 Sombreros para Pensar & Sistema MAGI (Evangelion)"
    )
    parser.add_argument("topic", nargs="?", help="Tema, pregunta técnica o arquitectura a deliberar")
    parser.add_argument("--magi", "-m", action="store_true", help="Ejecutar protocolo de consenso tripartito MAGI (Evangelion)")
    parser.add_argument("--cli", choices=["gemini", "ollama", "claude"], help="Forzar un motor CLI específico")
    parser.add_argument("--output", "-o", help="Ruta del archivo Markdown donde guardar el informe")

    args = parser.parse_args()

    topic = args.topic
    if not topic:
        if not sys.stdin.isatty():
            topic = sys.stdin.read().strip()
        else:
            mode_desc = "MAGI (Evangelion)" if args.magi else "6 Sombreros"
            topic = input(f"Introduce el tema o decisión técnica para el Consejo ({mode_desc}): ").strip()

    if not topic:
        print("Error: Se requiere un tema para deliberar.")
        sys.exit(1)

    if args.magi:
        report = run_magi_deliberation(topic, cli_name=args.cli)
    else:
        report = run_deliberation(topic, cli_name=args.cli)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[✓] Informe guardado con éxito en: {args.output}")
    else:
        print("\n" + report)


if __name__ == "__main__":
    main()
