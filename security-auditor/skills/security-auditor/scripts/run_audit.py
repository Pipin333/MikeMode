"""Script runner seguro para Security Auditor (Semgrep / Trail of Bits).

Ejecuta escaneos estáticos de seguridad aplicando las directivas de privacidad
y contención de Balthasar-2: telemetría desactivada (--metrics=off), cuota de memoria
y exclusiones rigurosas de dependencias y cachés.
"""

import argparse
import subprocess
import sys
from pathlib import Path
from typing import List

# Inmunización contra charmap en Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DEFAULT_BIN_PATH = Path.home() / ".local" / "bin" / "semgrep.exe"

EXCLUDED_DIRS = [
    "node_modules",
    ".venv",
    "venv",
    ".git",
    "dist",
    "build",
    "__pycache__",
    ".cache",
    "graphify-out",
]


def locate_semgrep_binary() -> Path:
    """Localiza el binario de Semgrep en el sistema.

    Returns:
        Path al ejecutable semgrep.

    Raises:
        FileNotFoundError: Si semgrep no está disponible.
    """
    if DEFAULT_BIN_PATH.exists():
        return DEFAULT_BIN_PATH

    import shutil
    path_bin = shutil.which("semgrep")
    if path_bin:
        return Path(path_bin)

    raise FileNotFoundError(
        "No se encontró el ejecutable 'semgrep'. "
        "Instálalo con 'python -m uv tool install semgrep' o 'pip install semgrep'."
    )


def run_security_scan(
    target_dir: Path,
    mode: str = "default",
    output_sarif: bool = False,
) -> int:
    """Ejecuta el escaneo de seguridad con Semgrep.

    Args:
        target_dir: Directorio a auditar.
        mode: Perfil de escaneo ('default', 'audit', 'secrets', 'all').
        output_sarif: Si es True, emite el reporte en formato estándar SARIF.

    Returns:
        Código de salida del proceso Semgrep.
    """
    binary = locate_semgrep_binary()

    # Selección de rulepacks según el perfil
    rulepacks: List[str] = []
    if mode == "default":
        rulepacks = ["p/default"]
    elif mode == "audit":
        rulepacks = ["p/security-audit", "p/trailofbits"]
    elif mode == "secrets":
        rulepacks = ["p/secrets"]
    elif mode == "all":
        rulepacks = ["p/default", "p/security-audit", "p/secrets", "p/trailofbits"]

    cmd = [
        str(binary),
        "scan",
        "--metrics=off",         # Salvaguarda de privacidad estricta
        "--max-memory=2048",      # Límite de 2 GB de RAM
        "--timeout=60",           # Timeout de 60s por regla
    ]

    for pack in rulepacks:
        cmd.extend(["--config", pack])

    for exc in EXCLUDED_DIRS:
        cmd.extend(["--exclude", exc])

    if output_sarif:
        sarif_file = target_dir / "security_report.sarif"
        cmd.extend(["--sarif", f"--output={sarif_file}"])

    cmd.append(str(target_dir))

    print(f"🛡️ Iniciando auditoría estática de seguridad en: {target_dir}")
    print(f"🔍 Perfil: {mode.upper()} | Reglas: {', '.join(rulepacks)}")
    print("🔒 Salvaguarda activa: Telemetría desactivada (--metrics=off)\n")

    result = subprocess.run(cmd, cwd=str(target_dir), check=False)

    if result.returncode == 0:
        print("\n✅ Auditoría finalizada: Cero vulnerabilidades bloqueantes detectadas.")
    else:
        print(f"\n⚠️ Auditoría completada con hallazgos o advertencias (código {result.returncode}).")

    return result.returncode


def main() -> None:
    """Punto de entrada de la CLI del runner de auditoría."""
    parser = argparse.ArgumentParser(
        description="Runner seguro de Security Auditor con Semgrep y reglas Trail of Bits."
    )
    parser.add_argument(
        "--target",
        "-t",
        default=".",
        help="Ruta al directorio a auditar (por defecto: actual)",
    )
    parser.add_argument(
        "--mode",
        "-m",
        choices=["default", "audit", "secrets", "all"],
        default="default",
        help="Perfil de escaneo: default (vulnerabilidades clave), audit (Trail of Bits exhaustivo), secrets (claves), all (todos)",
    )
    parser.add_argument(
        "--sarif",
        action="store_true",
        help="Exporta los resultados a un archivo estándar SARIF",
    )

    args = parser.parse_args()
    target_path = Path(args.target).resolve()

    if not target_path.exists():
        print(f"❌ Error: La ruta no existe: {target_path}")
        sys.exit(1)

    exit_code = run_security_scan(target_path, mode=args.mode, output_sarif=args.sarif)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
