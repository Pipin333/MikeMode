# 🐳 Docker-Guardian: Plugin de Containerización y Portabilidad Universal

> Hermano y complemento de **Doc-Guardian**. Garantiza que cada proyecto desarrollado o modificado por IA esté preparado para ser clonado desde GitHub y ejecutado en cualquier computadora o sistema operativo sin fricciones ni pasos manuales.

---

## 🎯 ¿Qué problema resuelve?

Cuando un proyecto se comparte en GitHub, los nuevos desarrolladores suelen encontrarse con problemas como:
- Versiones incompatibles de Node, Python, Java o Go instaladas localmente.
- Fallos en Windows por saltos de línea CRLF en scripts de inicio (`/bin/sh^M: bad interpreter`).
- Fallos en Mac Apple Silicon (M1/M2/M3/M4) por arquitecturas CPU ARM64 vs AMD64.
- Faltan bases de datos (Postgres, Redis) que deben instalarse y configurarse a mano.
- Copias accidentales de `node_modules` o `.venv` del host dentro del contenedor rompiendo binarios.

**Docker-Guardian** resuelve esto imponiendo un estándar obligatorio a los agentes de IA y proporcionando herramientas automáticas para generar configuraciones de Docker robustas, seguras y portables.

---

## ✨ Características Principales

1. **Regla de Agente Obligatoria (`rules/AGENTS.md`)**:
   - Cada vez que un agente de IA crea o refactoriza un proyecto, debe verificar y garantizar la tríada: `Dockerfile`, `docker-compose.yml` y `.dockerignore`.
2. **Plantillas Multi-Stage Optimizadas**:
   - Imágenes base Alpine y Slim.
   - Cacheo eficiente de capas de dependencias.
   - Seguridad: usuarios sin privilegios (`USER appuser`).
3. **Orquestación en 1 Clic (`docker-compose.yml`)**:
   - Arranque universal con `docker compose up --build`.
   - Mapeo de puertos, interpolación de variables `.env` y healthchecks.
4. **Blindaje de Portabilidad Multiplataforma**:
   - `.dockerignore` estricto que protege binarios del sistema anfitrión.
   - `.gitattributes` para forzar terminaciones LF en scripts Unix en Windows y Git.
   - Variables de entorno con `.env.example` listo para desarrollo.
5. **Herramienta CLI Integrada (`docker_guard.py`)**:
   - Detección automática del stack tecnológico (Node, Python, Next.js, Go, Rust, Java, Web estática).
   - Comandos de auditoría (`check`), andamiaje (`scaffold`) e inyección de reglas (`init`).

---

## 🛠️ Uso de la Herramienta CLI

El plugin incluye el script `docker_guard.py` que puede ejecutarse directamente en cualquier proyecto:

```bash
# 1. Auditar si el proyecto actual cumple los estándares de Docker:
python C:/Users/Petiso/.gemini/config/plugins/docker-guardian/skills/docker-guardian/scripts/docker_guard.py check

# 2. Generar automáticamente la configuración completa (Dockerfile, Compose, .dockerignore, README):
python C:/Users/Petiso/.gemini/config/plugins/docker-guardian/skills/docker-guardian/scripts/docker_guard.py scaffold

# 3. Inyectar las reglas para agentes en AGENTS.md / GEMINI.md del proyecto:
python C:/Users/Petiso/.gemini/config/plugins/docker-guardian/skills/docker-guardian/scripts/docker_guard.py init
```

### Opciones avanzadas:
- `--path <ruta>`: Especifica la carpeta del proyecto a auditar o configurar.
- `--stack <node|nextjs|vite|python|go|rust|java|static>`: Fuerza un stack específico.
- `--port <número>`: Asigna un puerto específico de escucha.

---

## 📁 Estructura del Plugin

```text
~/.gemini/config/plugins/docker-guardian/
├── plugin.json                                 # Manifiesto del plugin
├── README.md                                   # Esta documentación
├── rules/
│   └── AGENTS.md                               # Regla obligatoria para modelos y agentes de IA
└── skills/
    └── docker-guardian/
        ├── SKILL.md                            # Protocolo y guía de containerización
        ├── references/
        │   ├── dockerfile_templates.md         # Plantillas multi-stage por stack
        │   ├── compose_templates.md            # Recetas de Docker Compose
        │   ├── portability_guide.md            # Guía contra trampas de portabilidad
        │   └── devcontainer_template.md        # Soporte para GitHub Codespaces
        └── scripts/
            └── docker_guard.py                 # Herramienta CLI multiplataforma en Python
```

---

## 🚀 Flujo para Cualquier Persona que Clone el Repositorio

Cualquier persona que encuentre un proyecto protegido por Docker-Guardian en GitHub solo necesita ejecutar:

```bash
git clone <URL_DEL_REPOSITORIO>
cd <nombre-del-proyecto>
cp .env.example .env
docker compose up --build
```

Y la aplicación estará corriendo de inmediato en su navegador sin requerir instalar nada más.
