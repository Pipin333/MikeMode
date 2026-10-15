"""Script runner seguro para Graphify con cumplimiento de directivas MAGI.

Verifica la existencia del binario graphify, asegura que las exclusiones
estén presentes en el .gitignore del proyecto y ejecuta la extracción
en modo local (AST determinista) para prevenir saturación de memoria.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Inmunización contra charmap en consolas Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DEFAULT_BIN_PATH = Path.home() / ".local" / "bin" / "graphify.exe"
EXCLUDED_PATTERNS = [
    "graphify-out/",
    ".graphify/",
    "graph.html",
    "graph.json",
    "GRAPH_REPORT.md",
]


def ensure_gitignore(target_dir: Path) -> None:
    """Verifica y actualiza el archivo .gitignore para evitar polución de artefactos.

    Args:
        target_dir: Directorio raíz del proyecto analizado.
    """
    gitignore_path = target_dir / ".gitignore"
    if not gitignore_path.exists():
        return

    content = gitignore_path.read_text(encoding="utf-8", errors="ignore")
    missing = [pat for pat in EXCLUDED_PATTERNS if pat not in content]

    if missing:
        with gitignore_path.open("a", encoding="utf-8") as f:
            f.write("\n# Graphify generated knowledge graph artifacts (Balthasar guard)\n")
            for pat in missing:
                f.write(f"{pat}\n")
        print(f"🛡️ .gitignore actualizado con exclusiones de Graphify en: {target_dir}")


def locate_graphify_binary() -> Path:
    """Localiza el binario de graphify en el sistema.

    Returns:
        Path al ejecutable graphify.

    Raises:
        FileNotFoundError: Si el binario no está instalado.
    """
    if DEFAULT_BIN_PATH.exists():
        return DEFAULT_BIN_PATH

    # Intento en PATH
    import shutil
    path_bin = shutil.which("graphify")
    if path_bin:
        return Path(path_bin)

    raise FileNotFoundError(
        "No se encontró el ejecutable 'graphify'. "
        "Instálalo con 'python -m uv tool install graphifyy' o 'pip install graphifyy'."
    )


def run_extraction(target_dir: Path, code_only: bool = True) -> int:
    """Ejecuta la extracción de AST y generación de grafo.

    Args:
        target_dir: Directorio objetivo a analizar.
        code_only: Si es True, utiliza AST local sin llamadas a APIs externas.

    Returns:
        Código de salida del proceso.
    """
    binary = locate_graphify_binary()
    ensure_gitignore(target_dir)

    cmd = [str(binary), "extract", str(target_dir)]
    if code_only:
        cmd.append("--code-only")

    print(f"🕸️ Iniciando extracción de Grafo de Conocimiento en: {target_dir}")
    print(f"⚙️ Comando: {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=str(target_dir), check=False)

    if result.returncode == 0:
        # Generar cluster, reporte Markdown y HTML interactivo
        cluster_cmd = [str(binary), "cluster-only", str(target_dir)]
        subprocess.run(cluster_cmd, cwd=str(target_dir), check=False)

        html_output = target_dir / "graphify-out" / "graph.html"
        report_output = target_dir / "graphify-out" / "GRAPH_REPORT.md"
        print("\n✅ Extracción y clustering completados con éxito.")
        if html_output.exists():
            print(f"🌐 Grafo interactivo listo en: {html_output.resolve().as_uri()}")
        if report_output.exists():
            print(f"📄 Reporte topológico listo en: {report_output.resolve().as_uri()}")
    else:
        print(f"\n❌ Error durante la extracción de Graphify (código {result.returncode}).")

    return result.returncode


def main() -> None:
    """Punto de entrada de la CLI del runner."""
    parser = argparse.ArgumentParser(
        description="Runner seguro de Graphify con aislamiento de .gitignore."
    )
    parser.add_argument(
        "--target",
        "-t",
        default=".",
        help="Ruta al directorio del proyecto (por defecto: actual)",
    )
    parser.add_argument(
        "--full-semantic",
        action="store_true",
        help="Permite inferencia semántica adicional con LLM si hay API keys configuradas.",
    )

    args = parser.parse_args()
    target_path = Path(args.target).resolve()

    if not target_path.exists() or not target_path.is_dir():
        print(f"❌ Error: La ruta especificada no existe o no es un directorio: {target_path}")
        sys.exit(1)

    code_only = not args.full_semantic
    exit_code = run_extraction(target_path, code_only=code_only)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
