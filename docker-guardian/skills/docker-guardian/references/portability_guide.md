# 🌍 Guía de Portabilidad Universal Multiplataforma

El objetivo supremo de **Docker-Guardian** es: **Cualquier persona en el mundo clona el repositorio desde GitHub en cualquier máquina (Linux, macOS Apple Silicon/Intel, Windows WSL2/Docker Desktop) y el proyecto arranca sin errores.**

A continuación se detallan las 6 trampas de portabilidad más comunes y cómo Docker-Guardian las previene.

---

## 1. Trampa del Fin de Línea (CRLF vs LF en Windows y GitHub)

### El Problema:
Si un desarrollador en Windows crea un script `entrypoint.sh` o `start.sh`, Git en Windows suele guardarlo con retornos de carro Windows (`\r\n` / CRLF). Al clonar en otra máquina o al montarlo/copiarlo en un contenedor Linux, Docker falla con:
```text
/bin/sh: ./entrypoint.sh: /bin/sh^M: bad interpreter: No such file or directory
```

### La Solución Obligatoria:
1. Incluir un archivo `.gitattributes` en la raíz del proyecto:
   ```gitattributes
   # Normalizar finales de línea
   * text=auto
   *.sh text eol=lf
   Dockerfile text eol=lf
   docker-compose*.yml text eol=lf
   .env* text eol=lf
   ```
2. Si un Dockerfile copia un script shell, asegurar que ejecute `dos2unix` o sustituya `\r`:
   ```dockerfile
   COPY entrypoint.sh .
   RUN sed -i 's/\r$//' entrypoint.sh && chmod +x entrypoint.sh
   ```

---

## 2. Trampa de Módulos Compilados en el Host (`node_modules`, `.venv`)

### El Problema:
Si un usuario corre `npm install` o `pip install` en Windows o macOS y no existe un `.dockerignore`, el comando `COPY . .` copia los binarios de Windows/Mac al contenedor Linux. Resultado:
```text
Error: .../node_modules/sharp: invalid ELF header
ModuleNotFoundError: compiled C-extensions are missing
```

### La Solución Obligatoria:
Un archivo `.dockerignore` estricto en la raíz del proyecto:
```dockerignore
.git
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
```

---

## 3. Trampa de Arquitectura CPU (AMD64 vs ARM64 / Apple Silicon)

### El Problema:
Equipos Apple Silicon (M1/M2/M3/M4) usan ARM64 (`aarch64`), mientras que la mayoría de PCs y servidores Linux usan x86_64 (`amd64`). Si el `Dockerfile` descarga binarios directamente vía `curl` con nombres estáticos (p.ej. `curl -o tool https://.../tool-linux-amd64`), fallará al compilar en Mac M-series o AWS Graviton.

### La Solución Obligatoria:
1. Usar imágenes base multi-arquitectura oficiales (`node:alpine`, `python:slim`, `golang:alpine`, etc.), las cuales Docker resuelve automáticamente para la arquitectura nativa del anfitrión.
2. Si se deben descargar herramientas binarias externas, utilizar la sintaxis de Buildx con `ARG TARGETARCH`:
   ```dockerfile
   ARG TARGETARCH
   RUN curl -fsSL "https://example.com/binary-linux-${TARGETARCH}.tar.gz" | tar -xz
   ```

---

## 4. Trampa de Permisos y Usuario Root

### El Problema:
Ejecutar contenedores como `root` es un riesgo de seguridad crítico. Además, en Linux nativo, cualquier archivo generado por el contenedor en un volumen montado queda con propietario `root:root`, impidiendo que el desarrollador en el host pueda editar o borrar esos archivos sin `sudo`.

### La Solución Obligatoria:
1. Crear siempre un usuario sin privilegios en el stage final del Dockerfile:
   ```dockerfile
   RUN addgroup --system --gid 1001 appgroup && \
       adduser --system --uid 1001 --ingroup appgroup appuser
   USER appuser
   ```
2. Asegurar que los directorios donde la app escriba (ej. `/app/uploads`, `/app/cache`) tengan permisos asignados con `chown` antes de cambiar al usuario:
   ```dockerfile
   RUN mkdir -p /app/data && chown -R appuser:appgroup /app/data
   ```

---

## 5. Trampa de Variables de Entorno Faltantes (`.env`)

### El Problema:
El archivo `.env` nunca se debe subir a GitHub (por seguridad de claves). Pero si un nuevo usuario clona el repositorio y corre `docker compose up`, Compose fallará si las variables no tienen valores por defecto o si falta el archivo `.env`.

### La Solución Obligatoria:
1. Usar siempre sintaxis de interpolación con valores por defecto en `docker-compose.yml`:
   ```yaml
   ports:
     - "${PORT:-3000}:${PORT:-3000}"
   environment:
     - DATABASE_URL=${DATABASE_URL:-sqlite:///data/app.db}
   ```
2. Mantener un archivo `.env.example` en la raíz con valores listos para usar en local sin configuración manual.
3. Indicar en el `README.md` el comando `cp .env.example .env`.

---

## 6. Trampa de Direcciones de Red (`localhost` dentro del contenedor)

### El Problema:
Una aplicación dentro de un contenedor intenta conectarse a `localhost:5432` creyendo que accederá a Postgres, pero `localhost` dentro de un contenedor apunta al propio contenedor, no al host ni a otros servicios.

### La Solución Obligatoria:
En `docker-compose.yml`, usar los nombres de servicio de Compose para la resolución DNS interna (ej. `postgres:5432`, `redis:6379`), organizados bajo una red compartida (`networks: [app-network]`).
