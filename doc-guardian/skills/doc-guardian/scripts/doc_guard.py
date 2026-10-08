#!/usr/bin/env python3
"""
doc_guard.py - Asistente de Integridad y Sincronización de Documentación
Audita cambios de código en cualquier repositorio y verifica si el README.md
y la documentación reflejan las nuevas dependencias, variables de entorno y scripts.
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

ENV_VAR_PATTERNS = [
    re.compile(r'process\.env\.([A-Z0-9_]{3,})'),
    re.compile(r'os\.getenv\([\'"]([A-Z0-9_]{3,})[\'"]'),
    re.compile(r'os\.environ(?:\.get)?\[?[\'"]([A-Z0-9_]{3,})[\'"]'),
    re.compile(r'env::var\([\'"]([A-Z0-9_]{3,})[\'"]'),
    re.compile(r'System\.getenv\([\'"]([A-Z0-9_]{3,})[\'"]'),
    re.compile(r'\$_ENV\[[\'"]([A-Z0-9_]{3,})[\'"]\]'),
    re.compile(r'ENV\[[\'"]([A-Z0-9_]{3,})[\'"]\]'),
]

MANIFEST_FILES = {
    'package.json': 'Node.js / npm',
    'package-lock.json': 'Node.js lock',
    'requirements.txt': 'Python pip',
    'pyproject.toml': 'Python Poetry/Flit/UV',
    'Pipfile': 'Pipenv',
    'Cargo.toml': 'Rust Cargo',
    'go.mod': 'Go Modules',
    'composer.json': 'PHP Composer',
    'Gemfile': 'Ruby Bundler',
    'pom.xml': 'Java Maven',
    'build.gradle': 'Gradle',
}

DOC_EXTENSIONS = {'.md', '.rst', '.adoc', '.txt'}
DOC_FILENAMES = {'readme.md', 'readme', 'readme.txt', 'readme.rst', 'agents.md', 'gemini.md'}

CODE_EXTENSIONS = {
    '.js', '.jsx', '.ts', '.tsx', '.py', '.go', '.rs', '.java',
    '.c', '.cpp', '.h', '.hpp', '.cs', '.php', '.rb', '.sh',
    '.ps1', '.html', '.css', '.scss', '.vue', '.svelte'
}


def is_git_repo(path: Path) -> bool:
    try:
        res = subprocess.run(
            ['git', 'rev-parse', '--is-inside-work-tree'],
            cwd=path,
            capture_output=True,
            text=True
        )
        return res.returncode == 0
    except Exception:
        return False


def get_git_changes(path: Path):
    """Obtiene los archivos modificados según git status y git diff."""
    modified_files = set()
    staged_files = set()
    untracked_files = set()

    try:
        status_res = subprocess.run(
            ['git', 'status', '--porcelain'],
            cwd=path,
            capture_output=True,
            text=True,
            check=True
        )
        for line in status_res.stdout.splitlines():
            if not line:
                continue
            status_code = line[:2]
            filename = line[3:].strip()
            # Handle rename syntax 'old -> new'
            if ' -> ' in filename:
                filename = filename.split(' -> ')[1]
            
            p = path / filename
            if '?' in status_code:
                untracked_files.add(p)
            elif status_code[0] in 'MADRC':
                staged_files.add(p)
            if status_code[1] in 'MADRC':
                modified_files.add(p)
    except Exception as e:
        pass

    all_changed = modified_files.union(staged_files).union(untracked_files)
    return all_changed


def scan_recent_files(path: Path, max_hours: float = 2.0):
    """Escaneo alternativo para directorios que no usan git."""
    changed = set()
    now = Path(__file__).stat().st_mtime if Path(__file__).exists() else 0
    import time
    current_time = time.time()
    threshold = current_time - (max_hours * 3600)

    for root, dirs, files in os.walk(path):
        # Ignorar carpetas comunes pesadas
        dirs[:] = [d for d in dirs if d not in {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build', '.agents'}]
        for f in files:
            full = Path(root) / f
            try:
                if full.stat().st_mtime >= threshold:
                    changed.add(full)
            except Exception:
                pass
    return changed


def extract_env_vars_from_file(file_path: Path):
    found = set()
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        for pattern in ENV_VAR_PATTERNS:
            for match in pattern.finditer(content):
                var_name = match.group(1)
                # Filter out standard generic names like NODE_ENV if desired, or keep all
                if len(var_name) > 2:
                    found.add(var_name)
    except Exception:
        pass
    return found


def check_docs(target_dir: Path):
    target_dir = target_dir.resolve()
    print(f"\n🔍 [Doc-Guardian] Auditando proyecto en: {target_dir}")

    in_git = is_git_repo(target_dir)
    if in_git:
        changed_files = get_git_changes(target_dir)
        mode_str = "Git status / diff"
    else:
        changed_files = scan_recent_files(target_dir)
        mode_str = "Detección de archivos modificados recientemente"

    print(f"📌 Modo de inspección: {mode_str} ({len(changed_files)} archivos detectados)")

    readme_files = [
        f for f in target_dir.glob("README*") if f.is_file()
    ]
    has_readme = len(readme_files) > 0
    main_readme = readme_files[0] if has_readme else None

    # Separar tipos de archivos modificados
    code_changes = []
    doc_changes = []
    manifest_changes = []
    detected_env_vars = set()

    for file_path in changed_files:
        name_lower = file_path.name.lower()
        ext_lower = file_path.suffix.lower()

        if name_lower in DOC_FILENAMES or (file_path.parent.name.lower() == 'docs' and ext_lower in DOC_EXTENSIONS):
            doc_changes.append(file_path)
        elif name_lower in MANIFEST_FILES:
            manifest_changes.append((file_path, MANIFEST_FILES[name_lower]))
        elif ext_lower in CODE_EXTENSIONS:
            code_changes.append(file_path)
            vars_in_file = extract_env_vars_from_file(file_path)
            detected_env_vars.update(vars_in_file)

    # Revisar si las variables detectadas están documentadas en README o archivos .env.*.example
    env_examples = list(target_dir.glob(".env*.example")) + list(target_dir.glob(".env*.sample")) + list(target_dir.glob(".env*.template"))
    documented_vars = set()
    
    if main_readme and main_readme.exists():
        try:
            readme_text = main_readme.read_text(encoding='utf-8', errors='ignore')
            for var in detected_env_vars:
                if var in readme_text:
                    documented_vars.add(var)
        except Exception:
            pass

    for example_file in env_examples:
        if example_file.exists():
            try:
                env_text = example_file.read_text(encoding='utf-8', errors='ignore')
                for line in env_text.splitlines():
                    if '=' in line and not line.strip().startswith('#'):
                        var_name = line.split('=')[0].strip()
                        documented_vars.add(var_name)
            except Exception:
                pass

    undocumented_vars = detected_env_vars - documented_vars

    # Diagnóstico y Evaluación
    alerts = []
    warnings = []
    ok_items = []

    if not has_readme:
        alerts.append("❌ NO SE ENCONTRÓ `README.md` en la raíz del proyecto. Debe crearse de inmediato.")
    else:
        ok_items.append(f"✅ README principal detectado: {main_readme.name}")

    if code_changes and not doc_changes:
        alerts.append(
            f"⚠️ Se modificaron {len(code_changes)} archivo(s) de código, pero NO se ha modificado ningún archivo de documentación (README.md)."
        )
    elif doc_changes:
        ok_items.append(f"✅ Documentación modificada en este turno: {[f.name for f in doc_changes]}")

    if manifest_changes:
        manifest_names = ", ".join([f"{f.name} ({m})" for f, m in manifest_changes])
        warnings.append(
            f"📦 Se modificaron manifiestos de dependencias: {manifest_names}. Asegúrate de que las instrucciones de instalación en el README sigan vigentes."
        )

    if undocumented_vars:
        vars_str = ", ".join(sorted(undocumented_vars))
        alerts.append(
            f"🔑 Se detectaron variables de entorno en código que NO están en README ni en .env.example: {vars_str}"
        )

    # Reporte
    print("\n" + "="*60)
    print("📊 REPORTE DE AUDITORÍA DOCUMENTAL")
    print("="*60)

    if ok_items:
        print("\n[Puntos Positivos]")
        for item in ok_items:
            print(f"  {item}")

    if warnings:
        print("\n[Advertencias / Atención]")
        for w in warnings:
            print(f"  {w}")

    if alerts:
        print("\n[Acciones Críticas Requeridas]")
        for a in alerts:
            print(f"  {a}")
        print("\n💡 RECOMENDACIÓN: Actualiza el README.md y .env.example antes de concluir la tarea.")
        print("="*60 + "\n")
        return 1
    else:
        print("\n✨ ¡Todo en orden! La documentación parece sincronizada con los cambios de código.")
        print("="*60 + "\n")
        return 0


def init_rules(target_dir: Path):
    """Inyecta las directivas de documentación y estándares de código en AGENTS.md y GEMINI.md del proyecto."""
    rule_content = """# Reglas de Proyecto: Documentación y Estándares de Código (Doc-Guardian)

## Mandato para Agentes de IA y Asistentes de Código
Cada vez que realices cambios, adiciones o refactorizaciones en este proyecto:
1. **Estándares de Código y Docstrings**:
   - En Python: Es OBLIGATORIO cumplir con PEP 8 (estilo, tipado, nomenclatura snake_case) y PEP 257 (docstrings detallados con triples comillas en toda función, clase y módulo público).
   - En otros lenguajes: Cumplir con sus equivalentes oficiales (TSDoc/JSDoc en TypeScript/JS, rustdoc en Rust, godoc en Go, Javadoc en Java).
2. **Auditoría de Impacto**: Verifica si tus cambios modifican dependencias, variables de entorno (.env), comandos de ejecución, scripts de package.json o endpoints de API.
3. **Actualización del README**: Es OBLIGATORIO actualizar el `README.md` (y `docs/` si corresponde) en el mismo turno en el que se modifica el código.
4. **Sincronización de Variables**: Si usas nuevas variables de entorno en código, añádelas con valores descriptivos a `.env.example` y a la tabla de configuración en `README.md`.
5. **Cero Deuda Documental**: No concluyas tu respuesta sin reportar las secciones del README actualizadas y confirmar cumplimiento de estándares bajo el título `### 📝 Documentación Actualizada y Estándares`.
"""
    agents_file = target_dir / "AGENTS.md"
    gemini_file = target_dir / "GEMINI.md"

    for target_file in [agents_file, gemini_file]:
        if not target_file.exists():
            target_file.write_text(rule_content, encoding='utf-8')
            print(f"✅ Creado archivo de reglas para agentes en: {target_file.name}")
        else:
            current = target_file.read_text(encoding='utf-8', errors='ignore')
            if "Doc-Guardian" not in current:
                target_file.write_text(current.rstrip() + "\n\n" + rule_content, encoding='utf-8')
                print(f"✅ Anexadas reglas de documentación en: {target_file.name}")
            else:
                print(f"ℹ️ {target_file.name} ya contiene las reglas de Doc-Guardian.")


def scaffold_readme(target_dir: Path):
    """Genera un README.md inicial inteligente basado en los archivos del proyecto."""
    readme_path = target_dir / "README.md"
    if readme_path.exists():
        print(f"ℹ️ El archivo README.md ya existe en: {readme_path.name}. No se sobreescribirá.")
        return

    proj_name = target_dir.name
    description = "Proyecto desarrollado con sincronización continua de documentación."
    scripts_section = ""
    install_cmd = "npm install"
    start_cmd = "npm run dev"
    is_node = (target_dir / "package.json").exists()
    is_python = (target_dir / "requirements.txt").exists() or (target_dir / "pyproject.toml").exists()

    if is_node:
        try:
            import json
            pkg = json.loads((target_dir / "package.json").read_text(encoding='utf-8'))
            proj_name = pkg.get("name", proj_name)
            description = pkg.get("description") or description
            scripts = pkg.get("scripts", {})
            if scripts:
                scripts_lines = [f"- `npm run {s}`: {s} script" for s in scripts.keys()]
                scripts_section = "\n".join(scripts_lines)
        except Exception:
            pass
    elif is_python:
        install_cmd = "pip install -r requirements.txt"
        start_cmd = "python main.py"

    # Buscar variables de entorno
    env_vars = set()
    for env_f in target_dir.glob(".env*"):
        try:
            for line in env_f.read_text(encoding='utf-8', errors='ignore').splitlines():
                if '=' in line and not line.strip().startswith('#'):
                    env_vars.add(line.split('=')[0].strip())
        except Exception:
            pass

    env_table = ""
    if env_vars:
        env_table = "\n| Variable | Descripción | Valor por Defecto |\n| :--- | :--- | :--- |\n"
        for v in sorted(env_vars):
            env_table += f"| `{v}` | Configuración para {v} | - |\n"
    else:
        env_table = "\n*No se detectaron variables de entorno requeridas actualmente.*\n"

    readme_content = f"""# 📦 {proj_name}

> {description}

---

## 📋 Requisitos Previos
- **Runtime**: {'Node.js >= 18.x' if is_node else 'Python >= 3.10' if is_python else 'Consulte la configuración del proyecto'}
- **Gestor de paquetes**: {'npm / pnpm / yarn' if is_node else 'pip / uv' if is_python else 'N/A'}

---

## 🛠️ Instalación y Configuración

1. **Clonar e ingresar al proyecto**:
   ```bash
   cd {target_dir.name}
   ```

2. **Instalar dependencias**:
   ```bash
   {install_cmd}
   ```

3. **Configurar variables de entorno**:
   ```bash
   cp .env.example .env
   # Edita .env con tus credenciales
   ```

4. **Iniciar en modo desarrollo**:
   ```bash
   {start_cmd}
   ```

---

## ⚙️ Variables de Entorno
{env_table}

---

## 📜 Scripts Disponibles
{scripts_section if scripts_section else f"- `{start_cmd}`: Inicia el proyecto en modo desarrollo."}

---

## 🛡️ Mantenimiento de Documentación
Este proyecto utiliza **Doc-Guardian**. Cualquier cambio en dependencias, variables de entorno, rutas o scripts debe documentarse en este archivo en el mismo turno de desarrollo.
"""
    readme_path.write_text(readme_content, encoding='utf-8')
    print(f"✅ Generado README.md base en: {readme_path.name}")


def main():
    parser = argparse.ArgumentParser(description="Doc-Guardian: Auditoría y sincronización de documentación para agentes de IA.")
    parser.add_argument("action", choices=["check", "init", "scaffold"], default="check", nargs="?", help="check: audita el estado; init: inyecta reglas de agente; scaffold: genera README.md base")
    parser.add_argument("--path", "-p", default=".", help="Ruta del proyecto a evaluar (por defecto: actual)")

    args = parser.parse_args()
    target_path = Path(args.path).resolve()

    if args.action == "check":
        sys.exit(check_docs(target_path))
    elif args.action == "init":
        init_rules(target_path)
        sys.exit(0)
    elif args.action == "scaffold":
        scaffold_readme(target_path)
        sys.exit(0)


if __name__ == "__main__":
    main()
