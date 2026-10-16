# Antigravity Global Plugins & Skills Suite

Repositorio centralizado con los plugins y skills globales para **Google Antigravity** y agentes de codificación compatibles.

---

## 📦 Plugins Incluidos

| Plugin | Descripción | Componentes Clave |
| :--- | :--- | :--- |
| **`doc-guardian`** | Guardián de documentación técnica y estándares de código (PEP 8, PEP 257 o equivalentes). | Reglas obligatorias (`AGENTS.md`), estándares de docstrings y estilo, scripts (`doc_guard.py`). |
| **`docker-guardian`** | Guardián de containerización y portabilidad universal con Docker/Compose para GitHub. | Reglas obligatorias (`AGENTS.md`), plantillas multi-stage, devcontainer, scripts (`docker_guard.py`). |
| **`debug-guardian`** | Guardián de depuración rigurosa (RCA), testing (TDD), no-regresiones e higiene de código. | Reglas obligatorias (`AGENTS.md`), metodología RCA, patrones de test, scripts (`debug_guard.py`). |
| **`architect-guardian`** | Guardián de arquitectura de software, módulos profundos, DDD/ADRs, grafos DAG, revisión en dos ejes, relevo de sesión (`/handover`, `/pickup`), convergencia de PRs (`/babysit`) y reporte consolidado (`/report`). | Reglas (`AGENTS.md`), principios Ousterhout/Pocock/pstack, `HANDOVER.md`, orquestador (`architect_guard.py`). |
| **`frontend-guardian`** | Guardián de excelencia frontend: accesibilidad (a11y/WCAG 2.2), diseño por tokens, microinteracciones fluidas, regla de los 5 estados y Core Web Vitals. | Reglas obligatorias (`AGENTS.md`), estándares de accesibilidad y tokens, scripts (`frontend_guard.py`). |
| **`hermes-auto-learner`** | Motor de auto-aprendizaje procedural, destilación en 1 solo turno (`/learn`) y auto-mutación conducida por fallos (*Failure-Driven Mutation*) inspirado en NousResearch Hermes Agent. | Protocolo `SKILL.md`, estándares Hardline ($\le 60$ chars), salvaguardas MAGI Balthasar-2, validador determinista (`validate_skill.py`). |
| **`security-auditor`** | Auditoría estática formal y detección determinista de vulnerabilidades (CVEs, OWASP Top 10, secretos) basada en Semgrep y reglas de Trail of Bits. | Protocolo `SKILL.md`, perfiles (`default`, `audit`, `secrets`), telemetría desactivada (`--metrics=off`), runner (`run_audit.py`). |
| **`graphify`** | Generador de grafos de conocimiento interactivos (`graph.html`) y topología arquitectónica (`GRAPH_REPORT.md`) mediante AST determinista con Tree-sitter y detección de comunidades. | Protocolo `SKILL.md`, análisis de *blast radius* y comunidades Louvain/Leiden, runner (`run_graphify.py`). |
| **`office-forge`** | Motor programático de documentos corporativos Excel (`.xlsx` con fórmulas vivas), Word (`.docx`), PowerPoint (`.pptx`) y PDF con estética de banca de inversión y defensas anti-XXE / anti-Zip-bomb. | Protocolo `SKILL.md`, clases `ExcelForge`, `WordForge`, `PdfForge`, `PresentationForge` (`office_engine.py`). |
| **`impeccable`** | Kit de diseño frontend y estándares de calidad visual anti-slop (por Paul Bakaus). | Skills de auditoría visual (`critique`, `audit`, `polish`), diseño, reglas UI. |
| **`six-hats-council`** | Deliberación técnica profunda combinando los Seis Sombreros de Bono y el consenso democrático estilo MAGI de Evangelion (Melchior, Balthasar, Caspar) con subagentes concurrentes. | Protocolo MAGI (`magi_protocol.md`), plantillas de prompts y runner (`six_hats.py`). |

---

## ⚡ Modo Mike™: Ejecución Silenciosa y Comandos Bajo Demanda

Por defecto, los **5 Guardianes** (`architect`, `debug`, `doc`, `docker`, `frontend`) operan en **modo silencioso**: aplican todas sus reglas y verificaciones internamente sin ensuciar el chat con plantillas de reporte repetitivas. Puedes invocar los siguientes flujos bajo demanda:

| Comando en Chat | Qué hace |
| :--- | :--- |
| **`/report`** | Ejecuta los 5 scripts de auditoría determinista (`architect_guard.py --report`) y muestra el bloque ejecutivo completo de los 5 Guardianes. |
| **`/handover`** | (`pause-safely`) Guarda un snapshot determinista en `.scratch/HANDOVER.md` con la rama, commit `HEAD`, lo completado, el próximo paso del DAG y los callejones sin salida (*dead-ends*) antes de cerrar una sesión. |
| **`/pickup`** | (`session-pickup`) Lee `.scratch/HANDOVER.md` en una sesión nueva, verifica el estado de Git y retoma el trabajo exactamente donde quedó sin repetir errores. |
| **`/babysit`** | Inspecciona conflictos de merge contra la rama base, estado del árbol y pruebas locales/CI (`architect_guard.py --babysit`) hasta dejar la rama lista para mergear. |
| **`/learn`** | Destila en 1 solo turno una solución o sesión en un nuevo skill validado con `hermes-auto-learner`. |

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
