# Antigravity Global Plugins & Skills Suite

Repositorio centralizado con los plugins y skills globales para **Google Antigravity** y agentes de codificación compatibles.

---

## 📦 Plugins Incluidos

| Plugin | Descripción | Componentes Clave |
| :--- | :--- | :--- |
| **`impeccable`** | Kit de diseño frontend y estándares de calidad visual anti-slop (por Paul Bakaus). | Skills de auditoría visual (`critique`, `audit`, `polish`), diseño, reglas UI. |
| **`doc-guardian`** | Guardián de integridad y sincronización continua de documentación técnica. | Reglas obligatorias de sincronización (`AGENTS.md`), scripts de auditoría (`doc_guard.py`). |
| **`six-hats-council`** | Metodología de los Seis Sombreros de Bono adaptada para deliberación técnica y arquitectura de software. | Skills de análisis multidimensional previo a planes complejos. |
| **`science`** | Colección exhaustiva de herramientas y skills científicas y biomédicas. | Conectores a PDB, ChEMBL, AlphaFold, PubMed, Ensembl, UniProt, etc. |
| **`chrome-devtools-plugin`** | Herramientas de integración y diagnóstico con Chrome DevTools. | Conector de depuración web. |
| **`firebase`** | Reglas y herramientas para proyectos Firebase. | Soporte y directrices para Firebase. |
| **`google-antigravity-sdk`** | Referencias y herramientas para el SDK de Antigravity. | Herramientas de extensión del agente. |
| **`modern-web-guidance-plugin`** | Pautas modernas de mejores prácticas web y frontend. | Reglas de desarrollo frontend moderno. |

---

## 🚀 Cómo instalar este repositorio en un PC nuevo

Para disponer de todos estos plugins y skills globales en cualquier otro ordenador:

### En Windows (PowerShell)
```powershell
# 1. Asegurar que existe la carpeta de configuración de Gemini / Antigravity
New-Item -ItemType Directory -Force -Path "$HOME\.gemini\config"

# 2. Clonar este repositorio como la carpeta 'plugins'
git clone https://github.com/Pipin333/agent-plugins.git "$HOME\.gemini\config\plugins"
```

### En Linux / macOS (Bash / Zsh)
```bash
# 1. Crear el directorio de configuración si no existe
mkdir -p ~/.gemini/config

# 2. Clonar el repositorio
git clone https://github.com/Pipin333/agent-plugins.git ~/.gemini/config/plugins
```

Antigravity detecta y carga de forma automática los plugins y sus skills asociadas al iniciarse en la nueva máquina.

---

## 🔄 Sincronización de Actualizaciones

### Subir cambios desde cualquier PC
```bash
cd ~/.gemini/config/plugins   # (o "$HOME\.gemini\config\plugins" en Windows)
git add .
git commit -m "update: sincronizar nuevas skills o ajustes"
git push
```

### Recibir actualizaciones en tus otros PCs
```bash
cd ~/.gemini/config/plugins
git pull
```
