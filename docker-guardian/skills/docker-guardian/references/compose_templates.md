# 🐙 Plantillas de Docker Compose para Diversos Escenarios

Configuraciones estándar de `docker-compose.yml` preparadas para ejecución en un solo paso (`docker compose up --build`).

---

## 1. Aplicación Web Independiente (Node.js, Python, Go, etc.)

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: my-app
    restart: unless-stopped
    ports:
      - "${PORT:-3000}:${PORT:-3000}"
    env_file:
      - .env
    environment:
      - NODE_ENV=production
    healthcheck:
      test: ["CMD-SHELL", "wget --spider http://localhost:${PORT:-3000}/health || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
```

---

## 2. Aplicación Full-Stack con Base de Datos (PostgreSQL) y Caché (Redis)

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: web-app
    restart: unless-stopped
    ports:
      - "${PORT:-3000}:${PORT:-3000}"
    env_file:
      - .env
    environment:
      DATABASE_URL: postgresql://${POSTGRES_USER:-postgres}:${POSTGRES_PASSWORD:-postgres}@postgres:5432/${POSTGRES_DB:-app_db}
      REDIS_URL: redis://redis:6379
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - app-network

  postgres:
    image: postgres:16-alpine
    container_name: app-postgres
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-app_db}
      POSTGRES_USER: ${POSTGRES_USER:-postgres}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-postgres}
    ports:
      - "${POSTGRES_PORT:-5432}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-postgres} -d ${POSTGRES_DB:-app_db}"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

  redis:
    image: redis:7-alpine
    container_name: app-redis
    restart: unless-stopped
    ports:
      - "${REDIS_PORT:-6379}:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - app-network

volumes:
  postgres_data:
  redis_data:

networks:
  app-network:
    driver: bridge
```

---

## 3. Modo Dual: Desarrollo con Hot-Reloading vs Producción

Permite correr `docker compose -f docker-compose.dev.yml up` para desarrollo activo con recarga en caliente de código sin recompilar:

```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: deps # O builder
    container_name: dev-app
    ports:
      - "3000:3000"
    volumes:
      # Monta el código del anfitrión para hot-reload
      - .:/app
      # Evita sobreescribir los node_modules del contenedor con los del host
      - /app/node_modules
    env_file:
      - .env
    environment:
      - NODE_ENV=development
    command: ["npm", "run", "dev"]
```
