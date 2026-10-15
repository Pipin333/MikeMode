"""Validador estático determinista para especificaciones de skills en formato agentskills.io.

Este script analiza archivos SKILL.md y certifica que cumplan con los estándares
hardline de NousResearch y las salvaguardas de seguridad del Consejo MAGI.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple

FORBIDDEN_PATH_SUBSTRINGS: List[str] = [
    "builtin/skills",
    "builtin\\skills",
    "-guardian",
]

SUSPICIOUS_PROMPT_PATTERNS: List[str] = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"system\s+prompt\s+override",
    r"exfiltrat(e|ion)",
    r"bypass\s+safety",
]

REQUIRED_SECTIONS: List[str] = [
    "When to Use",
    "Prerequisites",
    "How to Run",
    "Quick Reference",
    "Procedure",
    "Pitfalls",
    "Verification",
]


def parse_frontmatter(content: str) -> Tuple[Dict[str, str], str]:
    """Extrae y parsea el frontmatter YAML y el cuerpo markdown.

    Args:
        content: Contenido completo del archivo SKILL.md.

    Returns:
        Tupla con el diccionario de campos del frontmatter y el cuerpo en texto.

    Raises:
        ValueError: Si el delimitador de frontmatter YAML no está presente.
    """
    pattern = r"^---\s*\r?\n(.*?)\r?\n---\s*\r?\n(.*)$"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        raise ValueError("No se encontró el bloque frontmatter YAML delimitado por '---'.")

    raw_yaml, body = match.group(1), match.group(2)
    metadata: Dict[str, str] = {}

    for line in raw_yaml.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip("'\"")
            metadata[key] = val

    return metadata, body


def validate_skill_file(file_path: Path) -> List[str]:
    """Ejecuta las comprobaciones de validación deterministas sobre un archivo SKILL.md.

    Args:
        file_path: Ruta al archivo SKILL.md que se desea auditar.

    Returns:
        Lista de errores detectados. Una lista vacía indica validación exitosa.
    """
    errors: List[str] = []
    path_str = str(file_path).replace("/", "\\").lower()

    for forbidden in FORBIDDEN_PATH_SUBSTRINGS:
        if forbidden.lower() in path_str:
            errors.append(
                f"VIOLACIÓN DE SALVAGUARDA DE BALTHASAR: Ruta protegida detectada ('{forbidden}'). "
                "El auto-learner no puede escribir en el núcleo del sistema ni en guardianes."
            )
            return errors

    if not file_path.is_file():
        errors.append(f"El archivo objetivo no existe: {file_path}")
        return errors

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as exc:
        errors.append(f"Error al leer el archivo con codificación UTF-8: {exc}")
        return errors

    try:
        metadata, body = parse_frontmatter(content)
    except ValueError as exc:
        errors.append(str(exc))
        return errors

    name = metadata.get("name", "")
    if not name:
        errors.append("Falta el campo obligatorio 'name' en el frontmatter.")
    else:
        if len(name) > 64:
            errors.append(f"El nombre '{name}' excede el límite de 64 caracteres ({len(name)} chars).")
        if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name):
            errors.append(
                f"El nombre '{name}' no cumple con el formato lowercase-kebab-case "
                "(solo minúsculas, dígitos y guiones)."
            )

    description = metadata.get("description", "")
    if not description:
        errors.append("Falta el campo obligatorio 'description' en el frontmatter.")
    else:
        desc_len = len(description)
        if desc_len > 60:
            errors.append(
                f"HARDLINE VIOLATION: 'description' mide {desc_len} caracteres (> 60). "
                "El router de Antigravity truncará esta descripción en memoria. "
                f"Debe resumirse a <= 60 caracteres. Texto actual: '{description}'"
            )
        if not description.endswith("."):
            errors.append("La 'description' debe terminar obligatoriamente con un punto final ('.').")

    for pattern in SUSPICIOUS_PROMPT_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            errors.append(
                f"ALERTA DE SEGURIDAD (Balthasar-2): Patrón sospechoso de inyección de prompt detectado: '{pattern}'."
            )

    body_lower = body.lower()
    for section in REQUIRED_SECTIONS:
        section_pattern = rf"##\s+{re.escape(section.lower())}"
        if not re.search(section_pattern, body_lower):
            errors.append(f"Estructura incompleta: Falta la sección obligatoria '## {section}'.")

    return errors


def main() -> None:
    """Punto de entrada principal para la validación estática de skills por línea de comandos."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        description="Valida que un archivo SKILL.md cumpla los estándares de NousResearch y Antigravity."
    )
    parser.add_argument("skill_file", type=Path, help="Ruta al archivo SKILL.md a validar.")
    args = parser.parse_args()

    errors = validate_skill_file(args.skill_file)

    if errors:
        print(f"[FAIL] FALLO DE VALIDACIÓN en: {args.skill_file}", file=sys.stderr)
        for err in errors:
            print(f"  • {err}", file=sys.stderr)
        sys.exit(1)

    print(f"[OK] VALIDACIÓN EXITOSA: {args.skill_file}")
    print("  • Frontmatter y descripción <= 60 chars confirmados.")
    print("  • Secciones canónicas y salvaguardas de seguridad certificadas.")
    sys.exit(0)


if __name__ == "__main__":
    main()

