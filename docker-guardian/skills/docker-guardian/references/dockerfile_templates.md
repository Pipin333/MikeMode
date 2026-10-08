# 🐳 Plantillas Multi-Stage de Dockerfile por Stack

Colección de plantillas de `Dockerfile` diseñadas bajo los principios de **Docker-Guardian**:
- **Multi-Stage Builds**: Separación estricta entre entorno de compilación y runtime.
- **Seguridad**: Ejecución bajo usuario sin privilegios (`non-root`).
- **Cacheo Inteligente**: Copia de manifiestos y lockfiles antes del código fuente.
- **Ligereza**: Imágenes base Alpine o Debian-Slim con tamaño mínimo.
- **Multi-Arquitectura**: Compatibles con AMD64 y ARM64 (Apple Silicon).

---

## 1. Node.js / TypeScript (Express, NestJS, Fastify, APIs)

```dockerfile
# syntax=docker/dockerfile:1
# 1. Base image con versión fijada
FROM node:20-alpine AS base
WORKDIR /app
RUN apk add --no-cache libc6-compat
ENV NODE_ENV=production

# 2. Stage de Dependencias
FROM base AS deps
WORKDIR /app
COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./
RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i --frozen-lockfile; \
  else npm install; \
  fi

# 3. Stage de Compilación (TypeScript / Assets)
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
# Descomentar si requiere compilación (build script en package.json):
# RUN npm run build

# 4. Stage de Producción / Runtime
FROM base AS runner
WORKDIR /app
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# Crear usuario seguro sin privilegios
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 appuser
USER appuser

# Copiar artefactos mínimos
COPY --from=deps --chown=appuser:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:nodejs /app ./

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

CMD ["node", "dist/index.js"] # O ["npm", "start"]
```

---

## 2. Next.js (SSR / API Routes con Output Standalone)

*Nota: Requiere `output: 'standalone'` en `next.config.js` para crear una imagen ultraligera (<150MB).*

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS base

# 1. Dependencias
FROM base AS deps
WORKDIR /app
RUN apk add --no-cache libc6-compat
COPY package.json package-lock.json* pnpm-lock.yaml* yarn.lock* ./
RUN \
  if [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f package-lock.json ]; then npm ci; \
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i --frozen-lockfile; \
  else npm install; \
  fi

# 2. Builder
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# 3. Runner
FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/api/health || exit 1

CMD ["node", "server.js"]
```

---

## 3. Python (FastAPI / Flask / Django / Worker)

```dockerfile
# syntax=docker/dockerfile:1
# 1. Builder con herramientas de compilación
FROM python:3.12-slim AS builder
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear entorno virtual aislado
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt* pyproject.toml* ./
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; \
    elif [ -f pyproject.toml ]; then pip install --no-cache-dir .; \
    fi

# 2. Runtime ultraligero
FROM python:3.12-slim AS runner
WORKDIR /app

# Variables de entorno críticas para Python en contenedores
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    PORT=8000

# Usuario sin privilegios
RUN useradd -m -u 1001 -s /bin/bash appuser

# Copiar entorno virtual y código
COPY --from=builder /opt/venv /opt/venv
COPY --chown=appuser:appuser . /app

USER appuser
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health', timeout=2)" || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 4. Go (Binario Estático Ultraligero en Scratch o Alpine)

```dockerfile
# syntax=docker/dockerfile:1
# 1. Builder
FROM golang:1.23-alpine AS builder
WORKDIR /app
RUN apk add --no-cache git ca-certificates tzdata

COPY go.mod go.sum* ./
RUN go mod download

COPY . .
# Compilación estática sin dependencias C (CGO_ENABLED=0)
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o /app/server .

# 2. Runtime mínimo (Scratch o Alpine)
FROM alpine:3.20 AS runner
WORKDIR /app
RUN apk --no-cache add ca-certificates tzdata && \
    addgroup -S -g 1001 appgroup && \
    adduser -S -u 1001 -G appgroup appuser

COPY --from=builder /app/server /app/server
USER appuser
EXPOSE 8080

CMD ["/app/server"]
```

---

## 5. Rust (Multi-Stage Cargo)

```dockerfile
# syntax=docker/dockerfile:1
# 1. Builder
FROM rust:1.80-alpine AS builder
WORKDIR /app
RUN apk add --no-cache musl-dev

COPY Cargo.toml Cargo.lock* ./
# Precompilar dependencias dummy para cachear capas
RUN mkdir src && echo "fn main() {}" > src/main.rs && \
    cargo build --release && \
    rm -rf src

COPY . .
RUN cargo build --release

# 2. Runner
FROM alpine:3.20 AS runner
WORKDIR /app
RUN addgroup -S -g 1001 appgroup && \
    adduser -S -u 1001 -G appgroup appuser

COPY --from=builder /app/target/release/app /app/server
USER appuser
EXPOSE 8080

CMD ["/app/server"]
```

---

## 6. Frontend Estático (Vite / React / Vue / HTML con Nginx)

```dockerfile
# syntax=docker/dockerfile:1
# 1. Builder
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# 2. Nginx no root
FROM nginxinc/nginx-unprivileged:alpine AS runner
COPY --from=builder /app/dist /usr/share/nginx/html
EXPOSE 8080

CMD ["nginx", "-g", "daemon off;"]
```
