#!/usr/bin/env python3
"""
debug_guard.py - Asistente de Depuración, Testing e Higiene de Código (Debug-Guardian)
Audita bases de código en busca de residuos de depuración (prints, console.log, breakpoints),
verifica la existencia y ejecución de tests automatizados y previene regresiones.
"""

import sys
import os
import re
import subprocess
import argparse
from pathlib import Path

# Safe encoding for Windows consoles (cp1252 / cmd / powershell)
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass


DEBUG_PATTERNS = [
    (re.compile(r'\bconsole\.(?:log|debug|trace)\s*\('), 'JavaScript/TypeScript console.log/debug residual'),
    (re.compile(r'^\s*debugger\s*;', re.MULTILINE), 'JavaScript/TypeScript debugger breakpoint'),
    (re.compile(r'^\s*breakpoint\s*\(\s*\)', re.MULTILINE), 'Python breakpoint() activo'),
    (re.compile(r'\bpdb\.set_trace\s*\(\s*\)'), 'Python pdb.set_trace() activo'),
    (re.compile(r'^\s*print\s*\(\s*f?[\'"](?:DEBUG|TEST|AQUI|LLEGO|VALUE|TEMP)', re.MULTILINE | re.IGNORECASE), 'Python print() de depuración temporal'),
    (re.compile(r'(?://|#)\s*(?:TODO|FIXME):\s*(?:quitar|remove|borrar|temporal|temp|delete)\b', re.IGNORECASE), 'Comentario de residuo temporal'),
]

IGNORE_DIRS = {
    '.git', 'node_modules', '.venv', 'venv', '__pycache__', 'dist', 'build',
    '.agents', '.gemini', 'coverage', '.pytest_cache'
}

TEST_EXTENSIONS = {'.test.js', '.test.ts', '.test.jsx', '.test.tsx', '.spec.js', '.spec.ts', '_test.go', '_test.py'}


def is_git_repo(path: Path) -> bool:
    try:
        res = subprocess.run(
            ['git', 'rev-parse', '--is-inside-work-tree'],
            cwd=path, capture_output=True, text=True
        )
        return res.returncode == 0
    except Exception:
        return False


def get_changed_files(target_dir: Path) -> set[Path]:
    """Obtiene los archivos modificados si es repo Git, o archivos recientes."""
    changed = set()
    if is_git_repo(target_dir):
        try:
            res = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=target_dir, capture_output=True, text=True, check=True
            )
            for line in res.stdout.splitlines():
                if not line:
                    continue
                filename = line[3:].strip()
                if ' -> ' in filename:
                    filename = filename.split(' -> ')[1]
                p = target_dir / filename
                if p.is_file():
                    changed.add(p)
        except Exception:
            pass

    if not changed:
        # Fallback a escaneo general de archivos fuente
        for root, dirs, files in os.walk(target_dir):
            dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
            for f in files:
                p = Path(root) / f
                if p.suffix.lower() in {'.py', '.js', '.ts', '.jsx', '.tsx', '.go', '.rs'}:
                    changed.add(p)

    return changed


def scan_file_for_residues(file_path: Path) -> list[tuple[int, str, str]]:
    """Escanea un archivo buscando residuos de depuración."""
    residues = []
    # No auditar archivos de pruebas si usan console.log intencionalmente
    name_lower = file_path.name.lower()
    is_test_file = any(name_lower.endswith(ext) for ext in TEST_EXTENSIONS) or 'test' in file_path.parts

    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        lines = content.splitlines()
        for idx, line in enumerate(lines, start=1):
            for pattern, desc in DEBUG_PATTERNS:
                # Omitir console.log en archivos de test
                if is_test_file and 'console.log' in desc:
                    continue
                if pattern.search(line):
                    residues.append((idx, desc, line.strip()))
    except Exception:
        pass
    return residues


def detect_test_runner(target_dir: Path) -> tuple[str, list[str]]:
    """Detecta el ejecutor de pruebas disponible en el proyecto."""
    # Node.js
    pkg_json = target_dir / "package.json"
    if pkg_json.exists():
        try:
            content = pkg_json.read_text(encoding='utf-8', errors='ignore').lower()
            if 'vitest' in content:
                return 'Vitest', ['npx', 'vitest', 'run']
            if 'jest' in content:
                return 'Jest', ['npx', 'jest']
            if '"test":' in content and 'no test specified' not in content:
                return 'npm test', ['npm', 'test']
        except Exception:
            pass

    # Python
    if (target_dir / "pytest.ini").exists() or (target_dir / "tests").exists() or any(target_dir.glob("test_*.py")):
        return 'Pytest', ['pytest']

    # Go
    if (target_dir / "go.mod").exists():
        return 'Go test', ['go', 'test', './...']

    # Rust
    if (target_dir / "Cargo.toml").exists():
        return 'Cargo test', ['cargo', 'test']

    return 'None', []


def check_debug_health(target_dir: Path, run_tests_flag: bool = False) -> int:
    """Ejecuta la auditoría de calidad de depuración y testing."""
    target_dir = target_dir.resolve()
    print(f"\n🔍 [Debug-Guardian] Auditando calidad e higiene de código en: {target_dir}")

    changed_files = get_changed_files(target_dir)
    print(f"📌 Archivos analizados: {len(changed_files)}")

    found_residues = []
    source_files_changed = []
    test_files_changed = []

    for f in changed_files:
        name_lower = f.name.lower()
        is_test = any(name_lower.endswith(ext) for ext in TEST_EXTENSIONS) or 'tests' in f.parts
        if is_test:
            test_files_changed.append(f)
        else:
            source_files_changed.append(f)

        file_residues = scan_file_for_residues(f)
        if file_residues:
            found_residues.append((f, file_residues))

    runner_name, runner_cmd = detect_test_runner(target_dir)

    alerts = []
    warnings = []
    ok_items = []

    # 1. Auditoría de Residuos de Debug
    if found_residues:
        alerts.append(f"❌ Se encontraron {len(found_residues)} archivo(s) con residuos de depuración:")
        for file_path, items in found_residues:
            alerts.append(f"   📄 {file_path.name}:")
            for line_no, desc, snippet in items[:3]:
                alerts.append(f"      ├─ L{line_no}: {desc} -> `{snippet[:60]}`")
            if len(items) > 3:
                alerts.append(f"      └─ ... y {len(items) - 3} ocurrencias más.")
    else:
        ok_items.append("✅ Cero residuos de depuración: Sin prints temporales, console.log ni breakpoints.")

    # 2. Auditoría de Tests
    if runner_name != 'None':
        ok_items.append(f"✅ Runner de pruebas detectado: {runner_name}")
        if source_files_changed and not test_files_changed:
            warnings.append(
                f"⚠️ Se modificaron {len(source_files_changed)} archivo(s) de lógica, pero ningún test. Se recomienda añadir tests de regresión."
            )
        elif test_files_changed:
            ok_items.append(f"✅ Tests actualizados o creados: {[t.name for t in test_files_changed]}")
    else:
        warnings.append("⚠️ No se detectó un test runner configurado (pytest, vitest, cargo test, etc.).")

    # 3. Ejecución de Tests (si se solicita)
    test_failed = False
    if run_tests_flag and runner_cmd:
        print(f"\n🏃 Ejecutando pruebas con '{' '.join(runner_cmd)}'...")
        try:
            res = subprocess.run(runner_cmd, cwd=target_dir, capture_output=True, text=True)
            if res.returncode == 0:
                ok_items.append(f"✅ Suite de tests ejecutada exitosamente (Código 0).")
            else:
                test_failed = True
                alerts.append(f"❌ La suite de pruebas falló (Código {res.returncode}):\n{res.stdout[-400:]}\n{res.stderr[-400:]}")
        except Exception as e:
            warnings.append(f"⚠️ No se pudo ejecutar el runner de pruebas: {e}")

    # Reporte
    print("\n" + "="*60)
    print("📊 REPORTE DE CALIDAD, TESTING E HIGIENE (DEBUG-GUARDIAN)")
    print("="*60)

    if ok_items:
        print("\n[Puntos Verificados]")
        for item in ok_items:
            print(f"  {item}")

    if warnings:
        print("\n[Advertencias / Oportunidades de Mejora]")
        for w in warnings:
            print(f"  {w}")

    if alerts:
        print("\n[Acciones Críticas Requeridas]")
        for a in alerts:
            print(f"  {a}")
        print("\n💡 RECOMENDACIÓN: Limpia los residuos de debug y asegura que las pruebas pasen en verde.")
        print("="*60 + "\n")
        return 1
    else:
        print("\n✨ ¡Código limpio, profesional e higiénico!")
        print("="*60 + "\n")
        return 0


def clean_residues(target_dir: Path):
    """Elimina residuos obvios de depuración en archivos fuente."""
    target_dir = target_dir.resolve()
    print(f"\n🧹 [Debug-Guardian] Limpiando residuos de depuración en: {target_dir}")
    changed_files = get_changed_files(target_dir)
    cleaned_count = 0

    clean_patterns = [
        re.compile(r'^\s*debugger\s*;\s*\n?', re.MULTILINE),
        re.compile(r'^\s*breakpoint\s*\(\s*\)\s*\n?', re.MULTILINE),
        re.compile(r'^\s*import\s+pdb;\s*pdb\.set_trace\(\)\s*\n?', re.MULTILINE),
        re.compile(r'^\s*print\s*\(\s*f?[\'"](?:DEBUG|TEST|AQUI|LLEGO)[^\n]*\)\s*\n?', re.MULTILINE | re.IGNORECASE),
    ]

    for f in changed_files:
        if not f.is_file():
            continue
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
            new_content = content
            for pat in clean_patterns:
                new_content = pat.sub('', new_content)
            if new_content != content:
                f.write_text(new_content, encoding='utf-8')
                print(f"  ✅ Limpiado: {f.name}")
                cleaned_count += 1
        except Exception:
            pass

    print(f"\n🎉 Limpieza finalizada. {cleaned_count} archivo(s) saneados.")


def init_rules(target_dir: Path):
    """Inyecta directivas de Debug-Guardian en AGENTS.md y GEMINI.md del proyecto."""
    rule_content = """# Reglas de Proyecto: Calidad de Depuración y Testing (Debug-Guardian)

## Mandato para Agentes de IA y Asistentes de Código
Cada vez que soluciones un error, refactorices o agregues código:
1. **Análisis de Causa Raíz**: Identifica la causa real; PROHIBIDO aplicar parches que silencien errores (`except: pass`, `as any`, null-checks superficiales).
2. **Reproducción Previa**: Escribe un test automatizado que falle reproduciendo el fallo antes de modificar la lógica de negocio.
3. **Cero Regresiones**: Ejecuta la suite de pruebas del proyecto y confirma que pase en verde.
4. **Higiene Estricta**: Elimina todo `console.log`, `print` de diagnóstico, `breakpoint()`, `debugger;` y código muerto antes de concluir.
5. **Reporte Obligatorio**: Concluye tu respuesta con la sección `### 🐞 Depuración, Testing e Higiene`.
"""
    for fname in ["AGENTS.md", "GEMINI.md"]:
        target_file = target_dir / fname
        if not target_file.exists():
            target_file.write_text(rule_content, encoding='utf-8')
            print(f"✅ Creado archivo de reglas para agentes en: {fname}")
        else:
            content = target_file.read_text(encoding='utf-8', errors='ignore')
            if "Debug-Guardian" not in content:
                target_file.write_text(content.rstrip() + "\n\n" + rule_content, encoding='utf-8')
                print(f"✅ Anexadas reglas de Debug-Guardian en: {fname}")
            else:
                print(f"ℹ️ {fname} ya contiene reglas de Debug-Guardian.")


def main():
    parser = argparse.ArgumentParser(description="Debug-Guardian: Calidad de depuración, prevención de regresiones e higiene de código.")
    parser.add_argument("action", choices=["check", "clean", "init"], default="check", nargs="?",
                        help="check: audita residuos y tests; clean: remueve prints/breakpoints; init: inyecta reglas")
    parser.add_argument("--path", "-p", default=".", help="Ruta del proyecto a evaluar (por defecto: actual)")
    parser.add_argument("--run-tests", action="store_true", help="Ejecuta automáticamente la suite de tests detectada")

    args = parser.parse_args()
    target_path = Path(args.path).resolve()

    if args.action == "check":
        sys.exit(check_debug_health(target_path, run_tests_flag=args.run_tests))
    elif args.action == "clean":
        clean_residues(target_path)
        sys.exit(0)
    elif args.action == "init":
        init_rules(target_path)
        sys.exit(0)


if __name__ == "__main__":
    main()
