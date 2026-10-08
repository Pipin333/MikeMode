#!/usr/bin/env python3
"""
docker_guard.py - Asistente de Containerización y Portabilidad Universal (Docker-Guardian)
Audita, valida y genera la infraestructura de Docker y Docker Compose para cualquier proyecto,
garantizando que pueda clonarse desde GitHub y ejecutarse en cualquier sistema operativo.
"""

import sys
import os
import re
import argparse
from pathlib import Path

# Safe encoding for Windows consoles (cp1252 / cmd / powershell)
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass


STACK_DETECT_FILES = [
    ('package.json', 'node'),
    ('requirements.txt', 'python'),
    ('pyproject.toml', 'python'),
    ('Pipfile', 'python'),
    ('go.mod', 'go'),
    ('Cargo.toml', 'rust'),
    ('pom.xml', 'java'),
    ('build.gradle', 'java'),
    ('index.html', 'static')
]

ESSENTIAL_DOCKERIGNORE_ENTRIES = {
    '.git',
    'node_modules',
    '.venv',
    'venv',
    '__pycache__',
    '.env',
    'dist',
    'build'
}


def detect_stack(target_dir: Path) -> tuple[str, int]:
    """Detecta el stack tecnológico predominante y el puerto sugerido."""
    for filename, stack in STACK_DETECT_FILES:
        target_file = target_dir / filename
        if target_file.exists():
            if stack == 'node':
                try:
                    content = target_file.read_text(encoding='utf-8', errors='ignore').lower()
                    if 'next' in content:
                        return 'nextjs', 3000
                    if 'vite' in content:
                        return 'vite', 5173
                    return 'node', 3000
                except Exception:
                    return 'node', 3000
            elif stack == 'python':
                port = 8000
                try:
                    for f in target_dir.glob("*.py"):
                        txt = f.read_text(encoding='utf-8', errors='ignore')
                        if '5000' in txt:
                            port = 5000
                            break
                        if '8080' in txt:
                            port = 8080
                            break
                except Exception:
                    pass
                return 'python', port
            elif stack == 'go':
                return 'go', 8080
            elif stack == 'rust':
                return 'rust', 8080
            elif stack == 'java':
                return 'java', 8080
            elif stack == 'static':
                return 'static', 8080

    return 'unknown', 3000


def check_containerization(target_dir: Path) -> int:
    """Audita el estado de containerización del proyecto."""
    target_dir = target_dir.resolve()
    print(f"\n🔍 [Docker-Guardian] Auditando containerización en: {target_dir}")

    stack, default_port = detect_stack(target_dir)
    print(f"📌 Stack detectado: {stack.upper()} (Puerto sugerido: {default_port})")

    dockerfile_candidates = [
        target_dir / "Dockerfile",
        target_dir / "dockerfile",
        target_dir / "Dockerfile.prod"
    ]
    dockerfile = next((f for f in dockerfile_candidates if f.exists()), None)

    compose_candidates = [
        target_dir / "docker-compose.yml",
        target_dir / "docker-compose.yaml",
        target_dir / "compose.yml",
        target_dir / "compose.yaml"
    ]
    compose_file = next((f for f in compose_candidates if f.exists()), None)

    dockerignore = target_dir / ".dockerignore"
    gitattributes = target_dir / ".gitattributes"
    env_example = target_dir / ".env.example"

    readme_files = [f for f in target_dir.glob("README*") if f.is_file()]
    readme = readme_files[0] if readme_files else None

    alerts = []
    warnings = []
    ok_items = []

    # 1. Auditoría de Dockerfile
    if not dockerfile:
        alerts.append("❌ Falta `Dockerfile` en el proyecto. No es posible construir la imagen.")
    else:
        ok_items.append(f"✅ Dockerfile presente: {dockerfile.name}")
        try:
            content = dockerfile.read_text(encoding='utf-8', errors='ignore')
            stages = len(re.findall(r'^FROM\s+', content, re.MULTILINE | re.IGNORECASE))
            if stages > 1:
                ok_items.append(f"  ├─ Multi-stage build detectado ({stages} etapas)")
            else:
                warnings.append("  ├─ ⚠️ Se recomienda usar multi-stage build para reducir tamaño y riesgos de seguridad.")

            if re.search(r'^USER\s+(?!root\b)', content, re.MULTILINE | re.IGNORECASE):
                ok_items.append("  ├─ Usuario no privilegiado (non-root) configurado correctamente.")
            else:
                warnings.append("  ├─ ⚠️ El Dockerfile parece ejecutarse como root. Configura un usuario sin privilegios (`USER appuser`).")

            if "HEALTHCHECK" in content.upper():
                ok_items.append("  └─ Directiva HEALTHCHECK configurada.")
            else:
                warnings.append("  └─ Sugerencia: Añadir directiva HEALTHCHECK para monitoreo de contenedor.")
        except Exception:
            pass

    # 2. Auditoría de Docker Compose
    if not compose_file:
        alerts.append("❌ Falta `docker-compose.yml` (o compose.yaml). Impide levantar el entorno con un solo comando.")
    else:
        ok_items.append(f"✅ Docker Compose presente: {compose_file.name}")
        try:
            content = compose_file.read_text(encoding='utf-8', errors='ignore')
            if "ports:" in content:
                ok_items.append("  ├─ Mapeo de puertos configurado.")
            else:
                warnings.append("  ├─ ⚠️ No se detectó mapeo explícito de puertos en docker-compose.yml.")

            if "env_file" in content or "environment:" in content:
                ok_items.append("  └─ Configuración de variables de entorno detectada.")
        except Exception:
            pass

    # 3. Auditoría de .dockerignore
    if not dockerignore.exists():
        alerts.append("❌ Falta `.dockerignore`. Esto puede provocar la copia de node_modules/.venv del host, causando errores de binarios.")
    else:
        ok_items.append("✅ `.dockerignore` presente.")
        try:
            ignore_content = dockerignore.read_text(encoding='utf-8', errors='ignore')
            missing_ignores = []
            for item in ['.git', 'node_modules', '.venv', 'venv', '.env']:
                if item not in ignore_content:
                    missing_ignores.append(item)
            if missing_ignores:
                warnings.append(f"  └─ ⚠️ `.dockerignore` no excluye: {', '.join(missing_ignores)}.")
            else:
                ok_items.append("  └─ Excluye correctamente .git, entornos virtuales y dependencias del host.")
        except Exception:
            pass

    # 4. Auditoría de README con sección Docker
    if not readme:
        alerts.append("❌ Falta `README.md`. Los usuarios que clonen de GitHub no sabrán cómo ejecutar el proyecto.")
    else:
        try:
            readme_text = readme.read_text(encoding='utf-8', errors='ignore').lower()
            if "docker compose" in readme_text or "docker-compose" in readme_text or "docker run" in readme_text:
                ok_items.append(f"✅ Instrucciones de Docker documentadas en {readme.name}.")
            else:
                alerts.append(f"⚠️ El archivo {readme.name} NO contiene instrucciones de ejecución con Docker (`docker compose up`).")
        except Exception:
            pass

    # 5. Auditoría de Git & Entorno
    if not env_example.exists():
        warnings.append("⚠️ Se recomienda un `.env.example` para que quien clone tenga las variables de entorno preconfiguradas.")
    else:
        ok_items.append("✅ `.env.example` disponible para clonadores de GitHub.")

    if not gitattributes.exists():
        warnings.append("💡 Sugerencia: Añadir `.gitattributes` para forzar terminaciones LF en scripts y evitar fallos al clonar en Windows.")
    else:
        ok_items.append("✅ `.gitattributes` presente para normalización de saltos de línea LF.")

    # Reporte
    print("\n" + "="*60)
    print("📊 REPORTE DE CONTAINERIZACIÓN Y PORTABILIDAD")
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
        print("\n💡 RECOMENDACIÓN: Ejecuta `docker_guard.py scaffold` para generar la configuración automáticamente.")
        print("="*60 + "\n")
        return 1
    else:
        print("\n✨ ¡Proyecto perfectamente containerizado y listo para GitHub!")
        print("="*60 + "\n")
        return 0


def generate_dockerfile(stack: str, port: int) -> str:
    """Genera el contenido de Dockerfile multi-stage óptimo según el stack."""
    if stack in ('node', 'vite'):
        return f"""# syntax=docker/dockerfile:1
FROM node:20-alpine AS base
WORKDIR /app
RUN apk add --no-cache libc6-compat
ENV NODE_ENV=production

FROM base AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --omit=dev || npm install

FROM base AS runner
WORKDIR /app
ENV PORT={port}
ENV HOSTNAME="0.0.0.0"

RUN addgroup --system --gid 1001 nodejs && \\
    adduser --system --uid 1001 appuser

COPY --from=deps --chown=appuser:nodejs /app/node_modules ./node_modules
COPY --chown=appuser:nodejs . .

USER appuser
EXPOSE {port}

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \\
  CMD wget --no-verbose --tries=1 --spider http://localhost:{port}/health || exit 1

CMD ["npm", "start"]
"""
    elif stack == 'nextjs':
        return f"""# syntax=docker/dockerfile:1
FROM node:20-alpine AS base

FROM base AS deps
WORKDIR /app
RUN apk add --no-cache libc6-compat
COPY package*.json ./
RUN npm ci

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT={port}
ENV HOSTNAME="0.0.0.0"

RUN addgroup --system --gid 1001 nodejs && \\
    adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE {port}

CMD ["node", "server.js"]
"""
    elif stack == 'python':
        return f"""# syntax=docker/dockerfile:1
FROM python:3.12-slim AS builder
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt* pyproject.toml* ./
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; \\
    elif [ -f pyproject.toml ]; then pip install --no-cache-dir .; \\
    fi

FROM python:3.12-slim AS runner
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \\
    PYTHONUNBUFFERED=1 \\
    PATH="/opt/venv/bin:$PATH" \\
    PORT={port}

RUN useradd -m -u 1001 -s /bin/bash appuser

COPY --from=builder /opt/venv /opt/venv
COPY --chown=appuser:appuser . /app

USER appuser
EXPOSE {port}

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \\
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:{port}/health', timeout=2)" || exit 1

CMD ["python", "main.py"]
"""
    elif stack == 'go':
        return f"""# syntax=docker/dockerfile:1
FROM golang:1.23-alpine AS builder
WORKDIR /app
RUN apk add --no-cache git ca-certificates tzdata

COPY go.mod go.sum* ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o /app/server .

FROM alpine:3.20 AS runner
WORKDIR /app
RUN apk --no-cache add ca-certificates tzdata && \\
    addgroup -S -g 1001 appgroup && \\
    adduser -S -u 1001 -G appgroup appuser

COPY --from=builder /app/server /app/server
USER appuser
EXPOSE {port}

CMD ["/app/server"]
"""
    elif stack == 'rust':
        return f"""# syntax=docker/dockerfile:1
FROM rust:1.80-alpine AS builder
WORKDIR /app
RUN apk add --no-cache musl-dev

COPY Cargo.toml Cargo.lock* ./
RUN mkdir src && echo "fn main() {{}}" > src/main.rs && \\
    cargo build --release && \\
    rm -rf src

COPY . .
RUN cargo build --release

FROM alpine:3.20 AS runner
WORKDIR /app
RUN addgroup -S -g 1001 appgroup && \\
    adduser -S -u 1001 -G appgroup appuser

COPY --from=builder /app/target/release/app /app/server
USER appuser
EXPOSE {port}

CMD ["/app/server"]
"""
    else: # static / default
        return f"""# syntax=docker/dockerfile:1
FROM nginxinc/nginx-unprivileged:alpine AS runner
COPY . /usr/share/nginx/html
EXPOSE {port}
CMD ["nginx", "-g", "daemon off;"]
"""


def generate_compose(project_name: str, port: int) -> str:
    """Genera el contenido de docker-compose.yml estándar."""
    return f"""version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: {project_name}-app
    restart: unless-stopped
    ports:
      - "${{PORT:-{port}}}:{port}"
    env_file:
      - .env
    environment:
      - PORT={port}
    healthcheck:
      test: ["CMD-SHELL", "wget --spider -q http://localhost:{port}/health || exit 0"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 10s
"""


def scaffold_containerization(target_dir: Path, stack_override: str = None, port_override: int = None):
    """Genera la infraestructura completa de Docker en el proyecto."""
    target_dir = target_dir.resolve()
    print(f"\n🚀 [Docker-Guardian] Creando infraestructura de containerización en: {target_dir}")

    detected_stack, detected_port = detect_stack(target_dir)
    stack = stack_override or detected_stack
    port = port_override or detected_port
    proj_name = re.sub(r'[^a-zA-Z0-9_\-]', '-', target_dir.name.lower())

    print(f"📦 Configuración: Stack={stack}, Puerto={port}, Proyecto={proj_name}")

    # 1. Dockerfile
    dockerfile_path = target_dir / "Dockerfile"
    if not dockerfile_path.exists():
        dockerfile_content = generate_dockerfile(stack, port)
        dockerfile_path.write_text(dockerfile_content, encoding='utf-8')
        print(f"  ✅ Creado: {dockerfile_path.name} (Multi-stage para {stack})")
    else:
        print(f"  ℹ️ {dockerfile_path.name} ya existe. Preservado sin sobreescribir.")

    # 2. docker-compose.yml
    compose_path = target_dir / "docker-compose.yml"
    if not compose_path.exists():
        compose_content = generate_compose(proj_name, port)
        compose_path.write_text(compose_content, encoding='utf-8')
        print(f"  ✅ Creado: {compose_path.name} (Mapeo puerto {port})")
    else:
        print(f"  ℹ️ {compose_path.name} ya existe. Preservado.")

    # 3. .dockerignore
    dockerignore_path = target_dir / ".dockerignore"
    dockerignore_content = """.git
.gitignore
node_modules/
.venv/
venv/
__pycache__/
*.pyc
dist/
build/
.next/
out/
.env
.env.local
.DS_Store
Thumbs.db
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.idea/
.vscode/
"""
    if not dockerignore_path.exists():
        dockerignore_path.write_text(dockerignore_content, encoding='utf-8')
        print("  ✅ Creado: .dockerignore (Protección de módulos del host y secretos)")
    else:
        print("  ℹ️ .dockerignore ya existe.")

    # 4. .gitattributes (Normalización LF para evitar errores CRLF en scripts)
    gitattrs_path = target_dir / ".gitattributes"
    gitattrs_content = """# Normalización de saltos de línea para portabilidad multiplataforma
* text=auto
*.sh text eol=lf
Dockerfile text eol=lf
docker-compose*.yml text eol=lf
.env* text eol=lf
"""
    if not gitattrs_path.exists():
        gitattrs_path.write_text(gitattrs_content, encoding='utf-8')
        print("  ✅ Creado: .gitattributes (Garantiza terminaciones LF en Linux/Docker)")
    else:
        print("  ℹ️ .gitattributes ya existe.")

    # 5. .env.example y .env
    env_example_path = target_dir / ".env.example"
    env_path = target_dir / ".env"
    env_content = f"""# Configuración local de desarrollo
PORT={port}
NODE_ENV=production
"""
    if not env_example_path.exists():
        env_example_path.write_text(env_content, encoding='utf-8')
        print("  ✅ Creado: .env.example")
    if not env_path.exists():
        env_path.write_text(env_content, encoding='utf-8')
        print("  ✅ Creado: .env local por defecto")

    # 6. Actualizar README.md con la sección Docker
    readme_path = target_dir / "README.md"
    docker_section = f"""
## 🐳 Ejecución con Docker (Portabilidad Universal)

Cualquier persona puede ejecutar este proyecto en su máquina sin necesidad de instalar dependencias ni runtimes locales:

### 1. Requisitos Previos
- [Docker](https://docs.docker.com/get-docker/) y [Docker Compose](https://docs.docker.com/compose/) instalados en tu sistema (Linux, macOS o Windows).

### 2. Clonar y Ejecutar con un Solo Comando

```bash
# 1. Clonar el repositorio
git clone <URL_DEL_REPOSITORIO>
cd {target_dir.name}

# 2. Copiar variables de entorno base
cp .env.example .env

# 3. Construir e iniciar el contenedor
docker compose up --build
```

La aplicación estará disponible inmediatamente en:
👉 **`http://localhost:{port}`**

### Comandos Útiles

- **Detener servicios**: `docker compose down`
- **Ver logs en tiempo real**: `docker compose logs -f`
- **Reconstruir sin caché**: `docker compose build --no-cache`
"""
    if readme_path.exists():
        readme_content = readme_path.read_text(encoding='utf-8', errors='ignore')
        if "docker compose" not in readme_content.lower():
            readme_path.write_text(readme_content.rstrip() + "\n\n" + docker_section.lstrip(), encoding='utf-8')
            print("  ✅ Anexada sección de Docker Quickstart en README.md")
        else:
            print("  ℹ️ README.md ya contiene instrucciones de Docker.")
    else:
        initial_readme = f"# 🚀 {target_dir.name}\n\nProyecto listo para despliegue y desarrollo portátil.\n" + docker_section
        readme_path.write_text(initial_readme, encoding='utf-8')
        print("  ✅ Creado: README.md con guía de Docker")

    print("\n🎉 ¡Infraestructura de containerización completada con éxito!")


def init_rules(target_dir: Path):
    """Inyecta directivas de Docker-Guardian en AGENTS.md y GEMINI.md del proyecto."""
    rule_content = """# Reglas de Proyecto: Containerización Obligatoria (Docker-Guardian)

## Mandato para Agentes de IA y Asistentes de Código
Cada vez que crees, modifiques o refactorices código en este proyecto:
1. **Garantizar Portabilidad Universal**: Mantén el `Dockerfile`, `docker-compose.yml` y `.dockerignore` actualizados con cualquier cambio en dependencias, puertos o variables de entorno.
2. **Cero Dependencias en el Host**: Quien clone este proyecto desde GitHub debe poder correrlo con `docker compose up --build` de forma 100% garantizada.
3. **Multi-Stage y Seguridad**: Usa imágenes multi-stage y usuarios no privilegiados (`USER appuser`).
4. **Reporte Obligatorio**: Al concluir la respuesta, incluye un resumen bajo `### 🐳 Containerización y Portabilidad`.
"""
    for fname in ["AGENTS.md", "GEMINI.md"]:
        target_file = target_dir / fname
        if not target_file.exists():
            target_file.write_text(rule_content, encoding='utf-8')
            print(f"✅ Creado archivo de reglas para agentes en: {fname}")
        else:
            content = target_file.read_text(encoding='utf-8', errors='ignore')
            if "Docker-Guardian" not in content:
                target_file.write_text(content.rstrip() + "\n\n" + rule_content, encoding='utf-8')
                print(f"✅ Anexadas reglas de Docker-Guardian en: {fname}")
            else:
                print(f"ℹ️ {fname} ya contiene reglas de Docker-Guardian.")


def main():
    parser = argparse.ArgumentParser(description="Docker-Guardian: Auditoría y generación de containerización portable para repositorios.")
    parser.add_argument("action", choices=["check", "scaffold", "init"], default="check", nargs="?",
                        help="check: audita el estado; scaffold: genera archivos de Docker; init: inyecta reglas para agentes")
    parser.add_argument("--path", "-p", default=".", help="Ruta del proyecto a evaluar (por defecto: actual)")
    parser.add_argument("--stack", "-s", choices=["node", "nextjs", "vite", "python", "go", "rust", "java", "static"],
                        help="Fuerza un stack tecnológico específico")
    parser.add_argument("--port", type=int, help="Fuerza el puerto expuesto del contenedor")

    args = parser.parse_args()
    target_path = Path(args.path).resolve()

    if args.action == "check":
        sys.exit(check_containerization(target_path))
    elif args.action == "scaffold":
        scaffold_containerization(target_path, stack_override=args.stack, port_override=args.port)
        sys.exit(0)
    elif args.action == "init":
        init_rules(target_path)
        sys.exit(0)


if __name__ == "__main__":
    main()
