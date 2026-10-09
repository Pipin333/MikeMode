# syntax=docker/dockerfile:1
FROM mcr.microsoft.com/playwright/python:v1.49.0-noble AS runner

WORKDIR /app

# Instalar dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Configurar usuario sin privilegios
RUN useradd -m -u 1001 appuser && chown -R appuser:appuser /app
USER appuser

# Copiar contenido del plugin
COPY --chown=appuser:appuser . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "skills/doc-guardian/scripts/doc_guard.py", "check"]
