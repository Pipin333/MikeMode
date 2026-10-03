#!/usr/bin/env python3
"""
Six Hats Council - Deliberation & Planning CLI Runner.
Executes Edward de Bono's 6 Thinking Hats methodology using a single LLM engine.

Can operate with local LLM CLIs (gemini, ollama, codex) or generate structured
deliberation prompts.
"""

import os
import sys
import shutil
import argparse
import subprocess
from typing import Dict, Tuple, Optional

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

        res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if res.returncode == 0:
            return True, res.stdout.strip()
        return False, f"Error {cli_type}: {res.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return False, f"Tiempo de espera agotado ({timeout}s) para {cli_type}"
    except Exception as exc:
        return False, f"Excepción ejecutando {cli_type}: {exc}"


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
    parser = argparse.ArgumentParser(description="Consejo de los 6 Sombreros para Pensar (De Bono)")
    parser.add_argument("topic", nargs="?", help="Tema, pregunta técnica o arquitectura a deliberar")
    parser.add_argument("--cli", choices=["gemini", "ollama", "claude"], help="Forzar un motor CLI específico")
    parser.add_argument("--output", "-o", help="Ruta del archivo Markdown donde guardar el informe")

    args = parser.parse_args()

    topic = args.topic
    if not topic:
        if not sys.stdin.isatty():
            topic = sys.stdin.read().strip()
        else:
            topic = input("Introduce el tema o decisión técnica para el Consejo de los 6 Sombreros: ").strip()

    if not topic:
        print("Error: Se requiere un tema para deliberar.")
        sys.exit(1)

    report = run_deliberation(topic, cli_name=args.cli)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[✓] Informe guardado con éxito en: {args.output}")
    else:
        print("\n" + report)


if __name__ == "__main__":
    main()
