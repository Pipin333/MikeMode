# 🚀 Integración con Dev Containers (GitHub Codespaces / VS Code)

Para máxima portabilidad, un repositorio clonado de GitHub puede incluir soporte para **Dev Containers**. Esto permite a cualquier persona abrir el repositorio en **GitHub Codespaces** en la nube con un solo clic en su navegador, o en **VS Code con la extensión Remote - Containers**, sin instalar absolutamente nada en su equipo.

---

## Estructura de Directorios

```text
mi-proyecto/
├── .devcontainer/
│   └── devcontainer.json
├── Dockerfile
├── docker-compose.yml
└── ...
```

---

## 1. `devcontainer.json` basado en `docker-compose.yml` (Recomendado)

Si el proyecto ya tiene un `docker-compose.yml`, este devcontainer se monta encima de los servicios existentes:

```json
{
  "name": "Dev Container (Docker-Guardian)",
  "dockerComposeFile": ["../docker-compose.yml"],
  "service": "app",
  "workspaceFolder": "/app",
  "customizations": {
    "vscode": {
      "settings": {
        "editor.formatOnSave": true
      },
      "extensions": [
        "ms-azuretools.vscode-docker",
        "dbaeumer.vscode-eslint"
      ]
    }
  },
  "remoteUser": "appuser"
}
```

---

## 2. `devcontainer.json` basado directamente en `Dockerfile`

```json
{
  "name": "Dev Container Standalone",
  "build": {
    "dockerfile": "../Dockerfile",
    "target": "builder"
  },
  "forwardPorts": [3000],
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-azuretools.vscode-docker"
      ]
    }
  }
}
```
