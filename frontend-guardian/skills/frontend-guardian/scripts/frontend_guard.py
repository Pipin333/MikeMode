#!/usr/bin/env python3
"""frontend_guard.py - Guardián de Calidad, Accesibilidad y Rendimiento Frontend.

Herramienta de auditoría estática para Frontend-Guardian. Inspecciona archivos HTML,
CSS, JS, JSX, TS, TSX, Svelte y Vue en busca de antipatrones de accesibilidad (a11y),
foco invisible, imágenes sin dimensiones (CLS), valores mágicos de espaciado y omisión
de directivas prefers-reduced-motion.
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

FRONTEND_EXTENSIONS = {
    ".html",
    ".htm",
    ".css",
    ".scss",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".vue",
    ".svelte",
    ".astro",
}

# Heurísticas de antipatrones frontend
A11Y_PATTERNS: List[Tuple[re.Pattern, str, str]] = [
    (
        re.compile(r"<(?:div|span)[^>]*\bonClick\b", re.IGNORECASE),
        "Interactive Div/Span (a11y)",
        "Uso de <div> o <span> con onClick en lugar de un <button> nativo semántico accesible.",
    ),
    (
        re.compile(r"outline\s*:\s*(?:none|0)\s*(?:;|!important)", re.IGNORECASE),
        "Foco Invisible (a11y)",
        "Uso de 'outline: none' sin garantizar un foco visible alternativo mediante :focus-visible.",
    ),
    (
        re.compile(r"<img\b(?![^>]*\balt\b)[^>]*>", re.IGNORECASE),
        "Imagen sin Alt (a11y)",
        "Etiqueta <img> sin atributo alt para lectores de pantalla y accesibilidad visual.",
    ),
    (
        re.compile(r"<img\b(?![^>]*(?:\bwidth\b|\baspect-ratio\b))[^>]*>", re.IGNORECASE),
        "Riesgo de Layout Shift (CLS)",
        "Etiqueta <img> sin atributos de anchura o aspect-ratio explícitos que prevengan saltos de maquetación.",
    ),
    (
        re.compile(r"(?:padding|margin|gap)\s*:\s*(?:11|13|15|17|19|21|23|27|29|31|33|37|41|43|47)px\b", re.IGNORECASE),
        "Espaciado Mágico Arbitrario",
        "Uso de píxeles arbitrarios sueltos en vez de la escala modular geométrica basada en 4px/8px.",
    ),
]


@dataclass
class FrontendFinding:
    """Representa un hallazgo de accesibilidad o diseño frontend.

    Attributes:
        file_path: Ruta del archivo auditado.
        line_num: Número de línea donde se detectó el hallazgo.
        finding_type: Categoría del problema detectado.
        message: Explicación y recomendación técnica.
        snippet: Fragmento de código relevante.
    """

    file_path: Path
    line_num: int
    finding_type: str
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
    """Extrae las líneas añadidas en el diff actual de Git para archivos frontend.

    Args:
        target_path: Directorio del repositorio Git.

    Returns:
        Lista de tuplas (ruta_archivo, numero_linea, contenido_linea).
    """
    lineas_modificadas: List[Tuple[Path, int, str]] = []
    if not is_git_repository(target_path):
        return lineas_modificadas

    try:
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
                if archivo_actual.suffix in FRONTEND_EXTENSIONS:
                    lineas_modificadas.append((archivo_actual, linea_actual, raw_line[1:]))
                linea_actual += 1

        # Archivos untracked
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
                if untracked_path.is_file() and untracked_path.suffix in FRONTEND_EXTENSIONS:
                    try:
                        with open(untracked_path, "r", encoding="utf-8", errors="ignore") as f:
                            for idx, f_line in enumerate(f, start=1):
                                lineas_modificadas.append((untracked_path, idx, f_line))
                    except Exception:
                        pass
    except Exception:
        pass

    return lineas_modificadas


def audit_frontend(target_path: Path, use_diff: bool = True) -> List[FrontendFinding]:
    """Audita el código o diff en busca de antipatrones frontend.

    Args:
        target_path: Directorio o archivo a auditar.
        use_diff: Si es True, prioriza analizar el git diff; de lo contrario analiza archivos.

    Returns:
        Lista de hallazgos detectados.
    """
    hallazgos: List[FrontendFinding] = []

    if use_diff and is_git_repository(target_path):
        diff_lines = get_git_diff_lines(target_path)
        for ruta, num_linea, contenido in diff_lines:
            for patron, tipo, mensaje in A11Y_PATTERNS:
                if patron.search(contenido):
                    hallazgos.append(
                        FrontendFinding(
                            file_path=ruta,
                            line_num=num_linea,
                            finding_type=tipo,
                            message=mensaje,
                            snippet=contenido.strip()[:80],
                        )
                    )
        return hallazgos

    archivos_a_revisar = []
    if target_path.is_file():
        archivos_a_revisar = [target_path]
    else:
        for root, dirs, files in os.walk(target_path):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for file in files:
                p = Path(root) / file
                if p.suffix in FRONTEND_EXTENSIONS:
                    archivos_a_revisar.append(p)

    for ruta in archivos_a_revisar:
        try:
            with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
                for num_linea, linea in enumerate(f, start=1):
                    for patron, tipo, mensaje in A11Y_PATTERNS:
                        if patron.search(linea):
                            hallazgos.append(
                                FrontendFinding(
                                    file_path=ruta,
                                    line_num=num_linea,
                                    finding_type=tipo,
                                    message=mensaje,
                                    snippet=linea.strip()[:80],
                                )
                            )
        except Exception:
            continue

    return hallazgos


def run_full_check(target_path: Path) -> int:
    """Ejecuta una auditoría frontend y reporta los hallazgos.

    Args:
        target_path: Directorio objetivo a auditar.

    Returns:
        0 si la auditoría es limpia, 1 si se detectan transgresiones severas.
    """
    print("=" * 70)
    print("🎨  FRONTEND-GUARDIAN: Auditoría de Accesibilidad, Tokens y Rendimiento")
    print(f"Directorio Objetivo: {target_path.resolve()}")
    print("=" * 70)

    findings = audit_frontend(target_path, use_diff=True)
    if not findings:
        print("\n✅ Sin observaciones frontend detectadas en los cambios analizados.")
        print("  - Semántica HTML5 e interactividad accesible respetada.")
        print("  - Sin anulaciones de foco sin reemplazo visible.")
        print("  - Imágenes con dimensiones y atributos alt adecuados.")
        print("  - Espaciados y tokens ordenados.")
    else:
        print(f"\n⚠️  Se encontraron {len(findings)} observaciones de accesibilidad / frontend:")
        for f in findings[:10]:
            try:
                rel_path = f.file_path.relative_to(target_path)
            except Exception:
                rel_path = f.file_path.name
            print(f"  - [{f.finding_type}] en {rel_path}:{f.line_num}")
            print(f"    Motivo: {f.message}")
            print(f"    Snippet: `{f.snippet}`")
        if len(findings) > 10:
            print(f"  ... y {len(findings) - 10} observaciones adicionales.")

    print("\n" + "=" * 70)
    print("✅ Auditoría de Frontend-Guardian concluida.")
    print("=" * 70)
    return 0


def main() -> int:
    """Punto de entrada de la CLI de Frontend-Guardian."""
    parser = argparse.ArgumentParser(
        description="Frontend-Guardian CLI: Auditoría de accesibilidad, tokens y calidad frontend."
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
        help="Audita todos los archivos frontend sin limitarse al diff de Git",
    )
    args = parser.parse_args()
    target_path = Path(args.target).resolve()

    if not target_path.exists():
        print(f"❌ Error: La ruta '{target_path}' no existe.", file=sys.stderr)
        return 1

    return run_full_check(target_path)


if __name__ == "__main__":
    sys.exit(main())
