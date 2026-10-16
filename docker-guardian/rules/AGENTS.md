# Regla de Containerización y Portabilidad Universal (Docker-Guardian)

## Mandato Obligatorio para Agentes y Modelos de IA
Cada vez que crees, desarrolles, clones o refactorices un proyecto de software, **es obligatorio garantizar que el proyecto esté 100% containerizado y listo para correr con Docker y Docker Compose antes de concluir tu respuesta**.

Cualquier persona que clone el repositorio desde GitHub debe poder ejecutar el proyecto en cualquier máquina (Linux, macOS Apple Silicon o Intel, Windows con WSL2 o Docker Desktop) mediante un único comando (`docker compose up --build`), sin tener que instalar lenguajes, gestores de paquetes, bases de datos o dependencias locales en su sistema operativo.

---

## 1. Disparadores Automáticos (Cuándo es OBLIGATORIO verificar/crear la containerización)
Revisa, crea o actualiza los archivos de containerización si has realizado:
- **Creación de Proyecto o Servicio**: Se inicia un nuevo proyecto, microservicio, aplicación web, API, script CLI o worker.
- **Nuevas Dependencias o Manifiestos**: Se agregaron o cambiaron dependencias en `package.json`, `requirements.txt`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `pom.xml`, etc., especialmente paquetes que requieran compilación C/C++, librerías nativas (`ffmpeg`, `libpq-dev`, `python3-dev`, `build-essential`, etc.).
- **Variables de Entorno o Puertos**: Se agregaron claves de configuración (`process.env`, `os.getenv`, etc.) o cambiaron puertos de escucha (ej. 3000, 8000, 5173). Deben reflejarse en `docker-compose.yml` y `.env.example`.
- **Servicios de Infraestructura**: El proyecto requiere bases de datos (PostgreSQL, MySQL, MongoDB), caché (Redis), colas (RabbitMQ) u otros servicios auxiliares. Deben incluirse como servicios coordinados en `docker-compose.yml`.
- **Scripts de Entrada**: Se cambió el punto de entrada o comando de ejecución (`npm start`, `python main.py`, `cargo run`, etc.).

---

## 2. Los Cuatro Pilares Obligatorios de Docker-Guardian
Cada repositorio o proyecto debe contener como mínimo estos cuatro componentes:

1. **`Dockerfile` optimizado y multi-stage**:
   - Uso de etapas separadas (`builder` y `runner`/`production`) para mantener la imagen final mínima y segura.
   - Cacheo eficiente de capas de dependencias (copiar primero lockfiles/manifiestos antes de copiar todo el código fuente).
   - Uso de usuario no privilegiado (`USER node`, `USER appuser`, etc.) en lugar de `root`.
   - Compatibilidad multi-arquitectura (`linux/amd64` y `linux/arm64` sin binarios atados a una sola CPU).
   - `HEALTHCHECK` configurado siempre que se trate de un servicio web o API.

2. **`docker-compose.yml` listo para "1-Click Run"**:
   - Servicio principal configurado con `build: .`, mapeo de puertos (`ports: ["HOST:CONTAINER"]`), y archivo de entorno (`env_file: [.env]`).
   - Volúmenes para persistencia de datos (ej. bases de datos) o montaje de código para desarrollo local.
   - Declaración de dependencias entre servicios (`depends_on` con `condition: service_healthy` cuando aplique).

3. **`.dockerignore` estricto**:
   - Excluir obligatoriamente: `node_modules`, `.venv`, `venv`, `__pycache__`, `.git`, `.env`, `.env.local`, `dist/`, `build/`, `.agents/`, `.gemini/`, logs y archivos temporales del SO (`.DS_Store`, `Thumbs.db`).
   - Evita enviar contextos gigantecos al daemon de Docker y previene fugas accidentales de secretos o incompatibilidad de binarios compilados en el host.

4. **Instrucciones en `README.md` ("🐳 Ejecución con Docker")**:
   - Sección destacada con el paso a paso exacto para cualquier persona que clone el repo:
     ```bash
     git clone <repo-url>
     cd <repo-name>
     cp .env.example .env
     docker compose up --build
     ```
   - Indicación clara de la URL local resultante (ej. `http://localhost:3000` o `http://localhost:8000`).

---

## 3. Principios de Portabilidad Universal (GitHub Ready)
Para que cualquier usuario en GitHub pueda clonar y correr el proyecto sin fricción:
- **Cero Rutas Absolutas**: Nunca uses rutas locales del anfitrión (`C:\...` o `/home/usuario/...`) en Dockerfiles o scripts.
- **Fin de Línea Unix (LF)**: Si incluyes scripts `entrypoint.sh` o scripts de arranque, asegúrate de que tengan saltos de línea LF (Unix), nunca CRLF de Windows, para que no fallen al ejecutarse en contenedores Linux.
- **Manejo de Secretos y `.env`**: Provee siempre un `.env.example` funcional con valores por defecto listos para desarrollo local inmediato dentro de Docker.
- **Soporte Dev Containers (Opcional pero recomendado)**: Cuando sea apropiado, provee o actualiza `.devcontainer/devcontainer.json` para permitir que el proyecto se ejecute directamente en GitHub Codespaces o VS Code Dev Containers en la nube.

---

## 4. Protocolo de Ejecución Silenciosa y Reporte Bajo Demanda (`/report`)
Antes de dar por terminada tu intervención:
1. **Verifica en silencio la existencia y validez de la tríada**: `Dockerfile`, `docker-compose.yml` y `.dockerignore`.
2. **Sincroniza los puertos y variables** entre el código, `docker-compose.yml` y `README.md`.
3. **Ejecución Silenciosa por Defecto**: Mantén la containerización al día **SIN imprimir el bloque de reporte en respuestas normales**.
4. **Reporte Bajo Demanda (`/report`)**: Únicamente cuando el usuario escriba `/report` o pida explícitamente el reporte de los guardianes, incluye el bloque:
   ```markdown
   ### 🐳 Containerización y Portabilidad (Docker-Guardian)
   - **`Dockerfile`**: [Creado/Actualizado] Multi-stage para [Stack], usuario sin privilegios configurado.
   - **`docker-compose.yml`**: [Creado/Actualizado] Puerto mapeado [XXXX:XXXX], servicios auxiliares [DB/Redis si aplica].
   - **`.dockerignore`**: Optimizado para evitar copias del host.
   - **Ejecución rápida**: `docker compose up --build` -> `http://localhost:XXXX`.
   ```
