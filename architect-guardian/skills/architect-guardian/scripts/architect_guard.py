#!/usr/bin/env python3
"""architect_guard.py - Guardián de Arquitectura de Software y Código Limpio.

Herramienta de auditoría estática para Architect-Guardian. Inspecciona bases de código
y diffs de Git en busca de olores de diseño (Fowler Smells), módulos superficiales,
artefactos de modelado de dominio (GLOSSARY.md y ADRs) y grafos de tareas con dependencias.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import List, Optional, Set, Tuple

# Reconfiguración segura de codificación para consolas Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


IGNORE_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    "dist",
    "build",
    ".agents",
    ".gemini",
    "coverage",
    ".pytest_cache",
    "science",
    "fixtures",
    "vendor",
}

CODE_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".rs",
    ".go",
    ".java",
    ".cs",
    ".cpp",
    ".c",
}

# Heurísticas de Fowler Code Smells
SMELL_PATTERNS: List[Tuple[re.Pattern, str, str]] = [
    (
        re.compile(r"\b(?:data|temp|tmp|res|ret|obj|val|foo|bar|handler|mgr|helper)\b", re.IGNORECASE),
        "Mysterious Name",
        "Identificador genérico o ambiguo que no comunica su propósito real en el dominio.",
    ),
    (
        re.compile(r"(?:\w+\.){4,}\w+"),
        "Message Chains",
        "Navegación excesivamente profunda que acopla al llamador con la estructura interna.",
    ),
    (
        re.compile(r"(?://|#)\s*(?:TODO|FIXME):?\s*(?:in the future|later|speculative|por si acaso)\b", re.IGNORECASE),
        "Speculative Generality",
        "Indicio de generalidad especulativa o ganchos no justificados por la especificación actual.",
    ),
    (
        re.compile(r"class\s+\w+(?:Manager|Helper|Utility|Processor)\b"),
        "Shallow / Vague Class",
        "Clase con sufijo ambiguo ('Manager', 'Helper', 'Utility'); evaluar si es un módulo profundo real.",
    ),
]


@dataclass
class SmellFinding:
    """Representa un hallazgo de olor de código o diseño.

    Attributes:
        file_path: Ruta del archivo auditado.
        line_num: Número de línea donde se detectó el hallazgo.
        smell_type: Categoría del Fowler Smell detectado.
        message: Explicación y recomendación de refactorización.
        snippet: Fragmento de código relevante.
    """

    file_path: Path
    line_num: int
    smell_type: str
    message: str
    snippet: str


def is_git_repository(target_path: Path) -> bool:
    """Verifica si la ruta objetivo forma parte de un repositorio Git.

    Args:
        target_path: Ruta del directorio a comprobar.

    Returns:
        True si es un repositorio Git válido, False en caso contrario.
    """
    try:
        resultado = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=target_path,
            capture_output=True,
            text=True,
        )
        return resultado.returncode == 0
    except Exception:
        return False


def get_git_diff_lines(target_path: Path) -> List[Tuple[Path, int, str]]:
    """Extrae las líneas añadidas en el diff actual de Git (incluyendo archivos nuevos).

    Args:
        target_path: Directorio del repositorio Git.

    Returns:
        Lista de tuplas (ruta_archivo, numero_linea, contenido_linea).
    """
    lineas_modificadas: List[Tuple[Path, int, str]] = []
    if not is_git_repository(target_path):
        return lineas_modificadas

    try:
        # 1. Diff de archivos modificados (staged y unstaged)
        resultado = subprocess.run(
            ["git", "--no-pager", "diff", "--unified=0", "HEAD"],
            cwd=target_path,
            capture_output=True,
            text=True,
            check=False,
        )
        archivo_actual: Optional[Path] = None
        linea_actual: int = 0

        for raw_line in resultado.stdout.splitlines():
            if raw_line.startswith("+++ b/"):
                nombre_relativo = raw_line[6:].strip()
                archivo_actual = target_path / nombre_relativo
            elif raw_line.startswith("@@ ") and archivo_actual:
                match = re.search(r"\+(\d+)", raw_line)
                if match:
                    linea_actual = int(match.group(1))
            elif raw_line.startswith("+") and not raw_line.startswith("+++") and archivo_actual:
                if any(ignored in archivo_actual.parts for ignored in IGNORE_DIRS):
                    continue
                if archivo_actual.suffix in CODE_EXTENSIONS:
                    lineas_modificadas.append((archivo_actual, linea_actual, raw_line[1:]))
                linea_actual += 1

        # 2. Archivos untracked (?? en git status)
        status_res = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=target_path,
            capture_output=True,
            text=True,
            check=False,
        )
        for line in status_res.stdout.splitlines():
            if line.startswith("?? "):
                rel_file = line[3:].strip()
                untracked_path = target_path / rel_file
                if any(ignored in untracked_path.parts for ignored in IGNORE_DIRS):
                    continue
                if untracked_path.is_file() and untracked_path.suffix in CODE_EXTENSIONS:
                    try:
                        with open(untracked_path, "r", encoding="utf-8", errors="ignore") as f:
                            for idx, f_line in enumerate(f, start=1):
                                lineas_modificadas.append((untracked_path, idx, f_line))
                    except Exception:
                        pass
    except Exception:
        pass

    return lineas_modificadas


def audit_smells(target_path: Path, use_diff: bool = True) -> List[SmellFinding]:
    """Audita el código o diff en busca de Fowler Code Smells.

    Args:
        target_path: Directorio o archivo a auditar.
        use_diff: Si es True, prioriza analizar el git diff; de lo contrario analiza archivos.

    Returns:
        Lista de hallazgos detectados.
    """
    hallazgos: List[SmellFinding] = []

    if use_diff and is_git_repository(target_path):
        diff_lines = get_git_diff_lines(target_path)
        for ruta, num_linea, contenido in diff_lines:
            for patron, tipo, mensaje in SMELL_PATTERNS:
                if patron.search(contenido):
                    hallazgos.append(
                        SmellFinding(
                            file_path=ruta,
                            line_num=num_linea,
                            smell_type=tipo,
                            message=mensaje,
                            snippet=contenido.strip()[:80],
                        )
                    )
        return hallazgos

    # Análisis directo de archivos
    archivos_a_revisar = []
    if target_path.is_file():
        archivos_a_revisar = [target_path]
    else:
        for root, dirs, files in os.walk(target_path):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for file in files:
                p = Path(root) / file
                if p.suffix in CODE_EXTENSIONS:
                    archivos_a_revisar.append(p)

    for ruta in archivos_a_revisar:
        try:
            with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
                for num_linea, linea in enumerate(f, start=1):
                    for patron, tipo, mensaje in SMELL_PATTERNS:
                        if patron.search(linea):
                            hallazgos.append(
                                SmellFinding(
                                    file_path=ruta,
                                    line_num=num_linea,
                                    smell_type=tipo,
                                    message=mensaje,
                                    snippet=linea.strip()[:80],
                                )
                            )
        except Exception:
            continue

    return hallazgos


def audit_domain_artifacts(target_path: Path) -> dict[str, bool | int | str]:
    """Verifica la existencia y salud de artefactos de modelado de dominio (DDD).

    Args:
        target_path: Directorio del proyecto.

    Returns:
        Diccionario con métricas de presencia de GLOSSARY.md y registros ADR.
    """
    glosario_existe = (target_path / "GLOSSARY.md").is_file()
    adr_dir = target_path / "docs" / "adr"
    num_adrs = 0
    if adr_dir.is_dir():
        num_adrs = len(list(adr_dir.glob("*.md")))

    return {
        "glossary_found": glosario_existe,
        "adr_directory_found": adr_dir.is_dir(),
        "adr_count": num_adrs,
    }


def audit_task_graph(target_path: Path) -> dict[str, int | List[str]]:
    """Audita archivos de tickets locales para comprobar grafos de dependencias.

    Args:
        target_path: Directorio del proyecto.

    Returns:
        Diccionario con conteo de tickets, bloqueados y frontera lista.
    """
    carpetas_scratch = [
        target_path / ".scratch",
        target_path / "docs" / "tickets",
        target_path / "specs",
    ]
    tickets_encontrados: List[Path] = []
    for c in carpetas_scratch:
        if c.is_dir():
            tickets_encontrados.extend(list(c.rglob("*.md")))

    frontera_lista: List[str] = []
    bloqueados: int = 0

    patron_bloqueado = re.compile(r"\*\*Blocked by:\*\*\s*(.+)", re.IGNORECASE)

    for t in tickets_encontrados:
        try:
            contenido = t.read_text(encoding="utf-8", errors="ignore")
            match = patron_bloqueado.search(contenido)
            if match:
                bloqueador = match.group(1).strip()
                if "none" in bloqueador.lower() or "ninguno" in bloqueador.lower():
                    frontera_lista.append(t.name)
                else:
                    bloqueados += 1
            else:
                frontera_lista.append(t.name)
        except Exception:
            continue

    return {
        "total_tickets": len(tickets_encontrados),
        "ready_frontier_count": len(frontera_lista),
        "blocked_tickets": bloqueados,
        "ready_frontier_samples": frontera_lista[:5],
    }


def run_full_check(target_path: Path) -> int:
    """Ejecuta una auditoría arquitectónica integral y presenta el reporte.

    Args:
        target_path: Directorio objetivo a auditar.

    Returns:
        0 si la auditoría es satisfactoria, 1 si se detectan transgresiones severas.
    """
    print("=" * 70)
    print("🏛️  ARCHITECT-GUARDIAN: Auditoría de Arquitectura, Dominio y Código")
    print(f"Directorio Objetivo: {target_path.resolve()}")
    print("=" * 70)

    # 1. Auditoría de Dominio y ADRs
    domain_info = audit_domain_artifacts(target_path)
    print("\n[1] Artefactos de Dominio y Decisiones (DDD):")
    if domain_info["glossary_found"]:
        print("  ✅ GLOSSARY.md: Presente en el repositorio.")
    else:
        print("  ℹ️  GLOSSARY.md: No detectado en la raíz (Recomendado si hay lógica de negocio compleja).")

    if domain_info["adr_directory_found"]:
        print(f"  ✅ docs/adr/: Directorio activo ({domain_info['adr_count']} registros ADR encontrados).")
    else:
        print("  ℹ️  docs/adr/: No detectado (Crear solo ante decisiones difíciles de revertir).")

    # 2. Auditoría de Grafos de Tareas
    task_info = audit_task_graph(target_path)
    print("\n[2] Descomposición de Tareas y Frontera de Ejecución (DAG):")
    if task_info["total_tickets"] > 0:
        print(f"  ✅ Tickets detectados: {task_info['total_tickets']}")
        print(f"  🚀 Frontera lista (Ready Frontier): {task_info['ready_frontier_count']}")
        print(f"  ⏳ Tareas bloqueadas: {task_info['blocked_tickets']}")
    else:
        print("  ℹ️  Sin tickets locales en .scratch/ o specs/. No hay tareas concurrentes pendientes.")

    # 3. Auditoría de Fowler Code Smells
    smells = audit_smells(target_path, use_diff=True)
    print("\n[3] Auditoría de Estándares y Fowler Code Smells (Diff / Reciente):")
    if not smells:
        print("  ✅ Sin olores de código ni anomalías detectadas en los cambios analizados.")
    else:
        print(f"  ⚠️  Se encontraron {len(smells)} observaciones de diseño/convención:")
        for s in smells[:8]:
            try:
                rel_path = s.file_path.relative_to(target_path)
            except Exception:
                rel_path = s.file_path.name
            print(f"    - [{s.smell_type}] en {rel_path}:{s.line_num}")
            print(f"      Motivo: {s.message}")
            print(f"      Código: `{s.snippet}`")
        if len(smells) > 8:
            print(f"    ... y {len(smells) - 8} observaciones adicionales.")

    print("\n" + "=" * 70)
    print("✅ Auditoría de Architect-Guardian concluida con éxito.")
    print("=" * 70)
    return 0


def main() -> int:
    """Punto de entrada de la CLI de Architect-Guardian."""
    parser = argparse.ArgumentParser(
        description="Architect-Guardian CLI: Auditoría de arquitectura, dominio y calidad de diseño."
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Directorio o archivo a auditar (por defecto: directorio actual)",
    )
    parser.add_argument(
        "--all-files",
        action="store_true",
        help="Audita todos los archivos en vez de limitarse al diff de Git",
    )
    args = parser.parse_args()
    target_path = Path(args.target).resolve()

    if not target_path.exists():
        print(f"❌ Error: La ruta '{target_path}' no existe.", file=sys.stderr)
        return 1

    return run_full_check(target_path)


if __name__ == "__main__":
    sys.exit(main())
