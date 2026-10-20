# MikeMode — Antigravity Global Plugins & Skills Suite

[![GitHub Repo](https://img.shields.io/badge/GitHub-Pipin333%2FMikeMode-1B4DD1?style=flat&logo=github)](https://github.com/Pipin333/MikeMode)
[![Status](https://img.shields.io/badge/Status-Public-success?style=flat)]()
[![Plugins](https://img.shields.io/badge/Plugins-13%20Active-blue?style=flat)]()

Repositorio público centralizado con los plugins, guardianes y skills globales para **Google Antigravity** y agentes de codificación compatibles (Gemini CLI, Claude Code, OpenCode, Codex).

Diseñado bajo la filosofía **Modo Mike™**: máxima profundidad modular, cero ruido en chat (*silent execution by default*), auditoría en dos ejes y continuidad determinista de sesiones.

---

## 📦 Plugins Incluidos

| Plugin | Tipo | Descripción | Componentes Clave |
| :--- | :---: | :--- | :--- |
| **`architect-guardian`** | Guardián | Arquitectura de software, módulos profundos (*Deep Modules*), DDD/ADRs, grafos de tareas (DAG), revisión en dos ejes, relevo de sesión (`/handover`, `/pickup`), convergencia de PRs (`/babysit`) y reporte consolidado (`/report`). | Reglas (`AGENTS.md`), principios Ousterhout, `HANDOVER.md`, orquestador (`architect_guard.py`). |
| **`security-auditor`** | Skill / Tool | Auditoría estática formal y detección determinista de vulnerabilidades (CVEs, OWASP Top 10, secretos) basada en Semgrep y reglas de Trail of Bits. | Protocolo `SKILL.md`, perfiles (`default`, `audit`, `secrets`, `all`), telemetría apagada (`--metrics=off`), runner (`run_audit.py`). |
| **`graphify`** | Skill / Tool | Grafo de conocimiento interactivo (`graph.html`) y topología arquitectónica (`GRAPH_REPORT.md`) mediante AST determinista con Tree-sitter y detección de comunidades Louvain/Leiden. | Protocolo `SKILL.md`, análisis de *blast radius*, dependencias circulares, runner (`run_graphify.py`). |
| **`office-forge`** | Skill / Tool | Motor programático de documentos corporativos Excel (`.xlsx` con fórmulas vivas), Word (`.docx`), PowerPoint (`.pptx`) y PDF con estética de banca de inversión y defensas anti-XXE / anti-Zip-bomb. | Protocolo `SKILL.md`, clases `ExcelForge`, `WordForge`, `PdfForge`, `PresentationForge` (`office_engine.py`). |
| **`six-hats-council`** | Skill / Agentes | Deliberación técnica profunda combinando los Seis Sombreros de Bono y el consenso democrático estilo MAGI de Evangelion (Melchior-1, Balthasar-2, Caspar-3) con subagentes concurrentes. | Protocolo MAGI (`magi_protocol.md`), prompts de sombreros/MAGI, runner (`six_hats.py`). |
| **`team-guardian`** | Guardián | Disciplina de equipo y honestidad de tests: Conventional Commits, ramas con prefijo, hook `commit-msg`, gate con perfiles (`prototype`/`product`) y bloqueo determinista ante cambios sensibles en tests sin justificación humana aprobada. | Reglas (`AGENTS.md`), validador de ramas/commits, detector de debilitamiento de tests, motor del gate (`team_guard.py`). |
| **`debug-guardian`** | Guardián | Depuración rigurosa (RCA), prevención de regresiones mediante TDD e higiene de código (cero prints, console.log o breakpoints residuales). | Reglas (`AGENTS.md`), metodología RCA, detector de frameworks de test, scripts (`debug_guard.py`). |
| **`doc-guardian`** | Guardián | Documentación técnica continua, sincronía del README y cumplimiento estricto de estándares de código (PEP 8, PEP 257 o equivalentes). Incluye compilador editorial a PDF. | Reglas (`AGENTS.md`), estándares de estilo/docstrings, scripts (`doc_guard.py`, `generate_perfect_pdf.py`). |
| **`docker-guardian`** | Guardián | Containerización y portabilidad universal con Docker y Docker Compose para despliegue y clonación "1-click run" desde GitHub. | Reglas (`AGENTS.md`), plantillas multi-stage, devcontainer, scripts (`docker_guard.py`). |
| **`frontend-guardian`** | Guardián | Excelencia frontend: accesibilidad radical (a11y/WCAG 2.2 AA), diseño por tokens, microinteracciones fluidas, regla de los 5 estados y Core Web Vitals (cero CLS). | Reglas (`AGENTS.md`), estándares a11y, tokens modulares, scripts (`frontend_guard.py`). |
| **`hermes-auto-learner`** | Skill / Tool | Motor de auto-aprendizaje procedural, destilación en 1 solo turno (`/learn`) y auto-mutación conducida por fallos (*Failure-Driven Mutation*) inspirado en NousResearch Hermes Agent. | Protocolo `SKILL.md`, estándares Hardline ($\le 60$ caracteres), salvaguardas Balthasar-2, validador (`validate_skill.py`). |
| **`impeccable`** | Skill Suite | Kit de diseño frontend y estándares de calidad visual anti-slop (creado por Paul Bakaus). | Skills de auditoría visual (`critique`, `audit`, `polish`, `bolder`, `quiet`), inspección live, design systems. |
| **`foreman`** | Playbook / Skill | Playbook de construcción y orquestación web para agentes (por Turki Alshuaibi). Entrevista de 8 compuertas, congelamiento de brief de diseño, verificación responsive (375px), despliegue DNS/SSL y metadatos (SEO, OpenGraph, sitemap, llms.txt). 100% Markdown puro. | Protocolo `SKILL.md`, compuertas 1 a 8, catálogo `vibe-coded-tells.md`, referencias y plantillas en `assets/`. |

---

## ⚡ Filosofía Operativa y Modo Mike™

Por defecto, los **5 Guardianes** operan bajo el **Modo Mike™ (Ejecución Silenciosa)**:
1. **Cero ruido en el chat**: Aplican todas las reglas arquitectónicas, de tipado, higiene y accesibilidad internamente sin imprimir plantillas repetitivas a menos que detecten un error o el usuario lo solicite explícitamente.
2. **Deep Modules (Ousterhout)**: Prohibido crear intermediarios vacíos (*middlemen*). Toda función o clase debe esconder complejidad relevante tras una interfaz limpia.
3. **Revisión en Dos Ejes Ciegos**:
   - **Eje 1**: Fowler Code Smells (Duplicación, Primitive Obsession, Feature Envy, Speculative Generality).
   - **Eje 2**: Fidelidad Estricta a la Especificación (cero omisiones, cero *scope creep*).
4. **Continuidad Operativa Determinista**: La memoria y el avance no se pierden entre sesiones gracias a `.scratch/HANDOVER.md`.

---

## 💬 Tabla Maestra de Comandos en Chat (Slash Commands / NLP)

Puedes invocar los siguientes flujos directamente escribiéndolos en el chat con tu agente:

| Comando / Frase en Chat | Plugin Responsable | Acción Realizada |
| :--- | :---: | :--- |
| **`/report`** | `architect-guardian` | Ejecuta los 5 guardianes de forma determinista y entrega un reporte ejecutivo consolidado del estado de la arquitectura, testing, docs, docker y frontend. |
| **`/handover`** o *"haz un handoff"* | `architect-guardian` | (`pause-safely`) Guarda un snapshot de alta fidelidad en `.scratch/HANDOVER.md` con la rama actual, commit `HEAD`, avances logrados, próximo corte vertical del DAG y callejones sin salida descartados. |
| **`/pickup`** o *"retoma la sesión"* | `architect-guardian` | (`session-pickup`) Lee `.scratch/HANDOVER.md`, verifica el estado del repositorio Git y retoma el trabajo exactamente en el próximo paso planificado sin amnesia ni repetir callejones sin salida. |
| **`/babysit`** o *"aterriza la rama"* | `architect-guardian` | (`babysit`) Verifica el árbol de trabajo, detecta y ayuda a resolver conflictos de merge contra la rama base y asegura que las pruebas queden en verde antes del merge. |
| **`/learn`** o *"aprende este patrón"* | `hermes-auto-learner` | Destila la solución o flujo recién completado en un skill autónomo, guardándolo en `skills/<nombre>/SKILL.md` y validándolo contra las directivas de NousResearch y Balthasar-2. |
| **`MAGI: <dilema>`** o *"consulta a MAGI"* | `six-hats-council` | Convoca a los 3 subagentes concurrentes del supercomputador MAGI (Melchior-1 Científica, Balthasar-2 Madre/Seguridad, Caspar-3 Mujer/Disruptora) para deliberar sobre decisiones arquitectónicas críticas. |
| **`/critique`**, **`/audit`**, **`/polish`** | `impeccable` | Ejecuta una auditoría de diseño frontend sobre la interfaz activa, evaluando jerarquía visual, espaciado, tipografía, accesibilidad y proponiendo mejoras concretas. |
| **"Ayúdame a construir mi portfolio"** / **"Crea una landing"** | `foreman` | Convierte al agente en capataz de obra web: ejecuta la entrevista de 8 pasos, congela el brief visual, audita responsive en 375px y guía el despliegue con dominio, SSL, 404 y SEO. |

---

## 💻 Guía Completa de Comandos CLI (Terminal)

Todos los scripts pueden ejecutarse desde la terminal utilizando Python. La ruta base de los plugins suele ser:
- **Windows**: `$HOME\.gemini\config\plugins` o `%USERPROFILE%\.gemini\config\plugins`
- **Linux / macOS**: `~/.gemini/config/plugins`

---

### 1. 🏛️ `architect-guardian` — Orquestador de Arquitectura y Continuidad

Script: `architect-guardian/skills/architect-guardian/scripts/architect_guard.py`

```bash
# Reporte consolidado de los 5 guardianes (/report)
python architect-guardian/skills/architect-guardian/scripts/architect_guard.py --report

# Pausar sesión de forma segura generando .scratch/HANDOVER.md
python architect-guardian/skills/architect-guardian/scripts/architect_guard.py --handover \
  --summary "Autenticación JWT implementada y probada" \
  --next-step "Crear endpoint POST /auth/refresh con test en rojo" \
  --dead-ends "No almacenar access token en localStorage por riesgo XSS"

# Retomar sesión validando Git y leyendo .scratch/HANDOVER.md
python architect-guardian/skills/architect-guardian/scripts/architect_guard.py --pickup

# Diagnóstico de convergencia de rama o PR (/babysit)
python architect-guardian/skills/architect-guardian/scripts/architect_guard.py --babysit

# Auditar arquitectura, DDD y Fowler smells en el diff actual
python architect-guardian/skills/architect-guardian/scripts/architect_guard.py

# Auditar todo el árbol completo del proyecto (no solo el diff de Git)
python architect-guardian/skills/architect-guardian/scripts/architect_guard.py --all-files [ruta/al/proyecto]
```

---

### 2. 🛡️ `security-auditor` — Auditoría Estática Formal con Trail of Bits

Script: `security-auditor/skills/security-auditor/scripts/run_audit.py`  
*(Requiere `semgrep` en PATH o instalado vía `uv tool install semgrep`)*

```bash
# Auditoría rápida con perfil por defecto (OWASP Top 10 + reglas clave)
python security-auditor/skills/security-auditor/scripts/run_audit.py

# Auditoría de seguridad profunda con reglas exhaustivas de Trail of Bits
python security-auditor/skills/security-auditor/scripts/run_audit.py --mode audit

# Detección determinista de credenciales, tokens y secretos expuestos
python security-auditor/skills/security-auditor/scripts/run_audit.py --mode secrets

# Escaneo completo (vulnerabilidades + auditoría Trail of Bits + secretos)
python security-auditor/skills/security-auditor/scripts/run_audit.py --mode all

# Auditar un directorio específico y exportar informe SARIF formal (para GitHub / CI)
python security-auditor/skills/security-auditor/scripts/run_audit.py --target ./src --mode all --sarif
```
> *Nota de privacidad*: El script corre con `--metrics=off` y telemetría completamente desactivada por diseño.

---

### 3. 🕸️ `graphify` — Grafo de Conocimiento y Topología AST

Script: `graphify/skills/graphify/scripts/run_graphify.py` o comando nativo `graphify`  
*(Requiere `graphifyy` en PATH o instalado vía `uv tool install graphifyy`)*

```bash
# Extracción AST determinista de alta velocidad (sin llamadas a LLM)
python graphify/skills/graphify/scripts/run_graphify.py --target ./mi-proyecto

# Modo semántico extendido con clustering adicional (si hay LLM configurado)
python graphify/skills/graphify/scripts/run_graphify.py --target ./mi-proyecto --full-semantic

# Uso directo con el binario oficial de Graphify (ignora archivos de tests/docs)
graphify extract ./mi-proyecto --code-only
```
**Artefactos generados en la raíz del proyecto analizado:**
- `graph.html`: Visualizador interactivo 2D/3D con comunidades Louvain/Leiden (abrir con doble clic en cualquier navegador).
- `GRAPH_REPORT.md`: Diagnóstico topológico con métricas de acoplamiento, dependencias circulares y cálculo de *blast radius*.

---

### 4. 📊 `office-forge` — Motor Programático de Documentos Corporativos

Script: `office-forge/skills/office-forge/scripts/office_engine.py`

#### A. Demostración y Generación desde CLI
```bash
# Generar todas las plantillas de demostración en un directorio de salida
python office-forge/skills/office-forge/scripts/office_engine.py --demo all --outdir ./reportes

# Generar solo modelo financiero Excel (.xlsx) con fórmulas vivas
python office-forge/skills/office-forge/scripts/office_engine.py --demo xlsx --outdir ./reportes

# Generar solo informe ejecutivo Word (.docx)
python office-forge/skills/office-forge/scripts/office_engine.py --demo docx --outdir ./reportes

# Generar solo presentación ejecutiva PowerPoint (.pptx)
python office-forge/skills/office-forge/scripts/office_engine.py --demo pptx --outdir ./reportes
```

#### B. Uso Programático en Scripts de Python o Herramientas de Agente
```python
from office_engine import ExcelForge, WordForge, PdfForge, PresentationForge

# 1. Crear un modelo financiero en Excel con fórmulas vivas y paleta corporativa
excel = ExcelForge("modelo_financiero.xlsx", palette="navy")
headers = ["Periodo", "Ingresos", "Costos", "Margen Bruto"]
data = [
    ["Q1 2026", 120000, 45000, "=B2-C2"],
    ["Q2 2026", 145000, 52000, "=B3-C3"],
    ["Total", "=SUM(B2:B3)", "=SUM(C2:C3)", "=B4-C4"]
]
excel.add_table_sheet("Finanzas", headers, data, has_totals=True)
excel.save()

# 2. Convertir un reporte Markdown a PDF seguro
pdf = PdfForge()
pdf.markdown_to_pdf("INFORME.md", "informe_final.pdf")
```

---

### 5. 🎩 `six-hats-council` — Deliberación y Consenso MAGI

Script: `six-hats-council/skills/six-hats-council/scripts/six_hats.py`

```bash
# Deliberación con los Seis Sombreros de Bono clásicos
python six-hats-council/skills/six-hats-council/scripts/six_hats.py "¿Conviene migrar de REST a gRPC en el gateway?"

# Protocolo de consenso democrático tripartito MAGI de Evangelion (-m / --magi)
# (Melchior-1 Científica vs Balthasar-2 Madre/Seguridad vs Caspar-3 Disruptora)
python six-hats-council/skills/six-hats-council/scripts/six_hats.py -m "¿Debemos adoptar SQLite embebido o PostgreSQL para el MVP?"

# Guardar el dictamen y votos formales en un archivo Markdown
python six-hats-council/skills/six-hats-council/scripts/six_hats.py -m "Adopción de Kafka vs Redis Streams" --output dictamen_magi.md
```

---

### 6. 🐞 `debug-guardian` — RCA, Testing e Higiene de Código

Script: `debug-guardian/skills/debug-guardian/scripts/debug_guard.py`

```bash
# Auditar residuos de depuración (prints, console.log, breakpoints) y configuración de tests
python debug-guardian/skills/debug-guardian/scripts/debug_guard.py check

# Auditar y ejecutar automáticamente la suite de pruebas del proyecto
python debug-guardian/skills/debug-guardian/scripts/debug_guard.py check --run-tests

# Limpiar automáticamente residuos de depuración temporales en el código
python debug-guardian/skills/debug-guardian/scripts/debug_guard.py clean

# Inyectar reglas locales de Debug-Guardian en un repositorio nuevo
python debug-guardian/skills/debug-guardian/scripts/debug_guard.py init
```

---

### 7. 📝 `doc-guardian` — Auditoría Documental y Compilador a PDF

Scripts: `doc-guardian/skills/doc-guardian/scripts/doc_guard.py` y `generate_perfect_pdf.py`

```bash
# Auditar si la documentación (README, .env.example, guías) está sincronizada con el código
python doc-guardian/skills/doc-guardian/scripts/doc_guard.py check

# Generar un README.md profesional estructurado (scaffold) si no existe
python doc-guardian/skills/doc-guardian/scripts/doc_guard.py scaffold

# Compilar un documento Markdown a PDF editorial de alta resolución con paginación limpia
python doc-guardian/skills/doc-guardian/scripts/doc_guard.py pdf README.md -o manual.pdf

# Compilación directa con Playwright (soporte completo para KaTeX, código y saltos de página)
python doc-guardian/skills/doc-guardian/scripts/generate_perfect_pdf.py documento.md salida.pdf
```

---

### 8. 🐳 `docker-guardian` — Containerización y "1-Click Run"

Script: `docker-guardian/skills/docker-guardian/scripts/docker_guard.py`

```bash
# Auditar la presencia de la tríada Docker (Dockerfile, docker-compose.yml, .dockerignore)
python docker-guardian/skills/docker-guardian/scripts/docker_guard.py check

# Generar automáticamente la tríada de Docker optimizada según el stack del proyecto
python docker-guardian/skills/docker-guardian/scripts/docker_guard.py scaffold

# Forzar un stack y puerto específico
python docker-guardian/skills/docker-guardian/scripts/docker_guard.py scaffold --stack python --port 8000
python docker-guardian/skills/docker-guardian/scripts/docker_guard.py scaffold --stack node --port 3000
```

---

### 9. 🎨 `frontend-guardian` — Accesibilidad, Tokens y Calidad Frontend

Script: `frontend-guardian/skills/frontend-guardian/scripts/frontend_guard.py`

```bash
# Auditar accesibilidad (a11y), tokens, foco visible y CLS en el diff actual de Git
python frontend-guardian/skills/frontend-guardian/scripts/frontend_guard.py

# Auditar exhaustivamente todos los archivos frontend de un proyecto
python frontend-guardian/skills/frontend-guardian/scripts/frontend_guard.py --all-files ./frontend
```

---

### 10. 🧠 `hermes-auto-learner` — Validador de Skills Procedurales

Script: `hermes-auto-learner/skills/hermes-auto-learner/scripts/validate_skill.py`

```bash
# Validar que un archivo SKILL.md cumpla el estándar Hardline (<= 60 chars) y directivas de seguridad
python hermes-auto-learner/skills/hermes-auto-learner/scripts/validate_skill.py ruta/al/skill/SKILL.md
```

---

### 11. 💎 `impeccable` — Suite de Calidad Visual y Frontend

Comandos y verbos integrados para la consola de desarrollo o chats de diseño:

| Verbo Impeccable | Finalidad |
| :--- | :--- |
| `init` | Configura el proyecto con `PRODUCT.md` y `DESIGN.md`. |
| `document` | Extrae el sistema de diseño visual (colores, fuentes, radios) a `DESIGN.md`. |
| `audit` | Inspecciona calidad técnica frontend (a11y, performance, responsive, anti-patrones). |
| `critique` | Evaluación experta de jerarquía visual y experiencia de usuario. |
| `polish` | Refina detalles visuales sutiles, alineaciones y microinteracciones. |
| `bolder` | Aumenta el carácter visual de diseños sosos o corporativos genéricos. |
| `quiet` | Reduce el ruido visual en interfaces sobrecargadas o ruidosas. |
| `live` | Modo interactivo con hot-reloading de variantes de diseño en el navegador. |

---

### 12. 🏗️ `foreman` — Capataz de Construcción Web (Turki Alshuaibi)

Skill: `foreman/skills/foreman/SKILL.md` *(100% Markdown puro, cero código ejecutable)*

Foreman opera como el director de obra web a través de un diálogo procedimental estricto estructurado en 8 compuertas:

1. **Orient**: Inventario de activos reales (logos, fotos, textos verdaderos). Cero datos inventados.
2. **Decide**: 1 único lector, 1 única acción tras 90 segundos, 1 trabajo central y lista de *non-goals*.
3. **Look**: Dirección visual, paleta y contraste tipográfico probados en `brand.html` desechable.
4. **Brief**: Redacción y congelamiento formal de `BUILD-BRIEF.md`.
5. **Build**: Construcción web bajo restricciones anti-slop (cero botones rotos `#`, cero rellenos).
6. **Verify**: Verificación destructiva de affordances en móvil (375px) y auditoría contra `vibe-coded-tells.md`.
7. **Ship**: Guía de despliegue en producción (Cloudflare Pages, Vercel, GitHub Pages), DNS y SSL.
8. **Index & Metadata**: Configuración de `404.html`, OpenGraph previews, `robots.txt`, `sitemap.xml` y `llms.txt`.

```bash
# Invocación en chat (Antigravity / Gemini CLI / Claude Code):
"Ayúdame a construir mi portfolio"
"Quiero armar una landing page para mi producto"
"Reconstruyamos la web de documentación con Foreman"
```

---

## 🛠️ Instalación Rápida de Herramientas y Dependencias

Para aprovechar al 100% las capacidades de auditoría estática (`semgrep`), grafos AST (`graphify`) y generación ofimática (`office-forge`), instala las siguientes herramientas en tu entorno:

### 1. Gestor `uv` y Herramientas Globales
```bash
# Instalar uv si aún no lo tienes
# Windows (PowerShell):
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
# Linux / macOS:
curl -LsSf https://astral.sh/uv/install.sh | sh

# Instalar Semgrep (para security-auditor)
uv tool install semgrep

# Instalar Graphify (para graphify)
uv tool install graphifyy
```

### 2. Paquetes Python Ofimáticos y de Análisis
```bash
uv pip install --system openpyxl python-docx pypdf pdfplumber python-pptx defusedxml reportlab networkx scipy
# O con pip tradicional:
pip install openpyxl python-docx pypdf pdfplumber python-pptx defusedxml reportlab networkx scipy
```

---

## 🚀 Cómo Instalar este Repositorio en un PC Nuevo

### En Windows (PowerShell)
```powershell
# 1. Asegurar la carpeta de configuración de Gemini / Antigravity
New-Item -ItemType Directory -Force -Path "$HOME\.gemini\config"

# 2. Clonar el repositorio como la carpeta 'plugins'
git clone https://github.com/Pipin333/MikeMode.git "$HOME\.gemini\config\plugins"
```

### En Linux / macOS (Bash / Zsh)
```bash
# 1. Crear el directorio de configuración si no existe
mkdir -p ~/.gemini/config

# 2. Clonar el repositorio
git clone https://github.com/Pipin333/MikeMode.git ~/.gemini/config/plugins
```

Antigravity detecta y carga de forma automática los plugins y sus skills asociadas al iniciarse.

---

## 🔄 Sincronización de Actualizaciones entre Máquinas

### Subir cambios desde cualquier PC
```bash
cd ~/.gemini/config/plugins   # (o "$HOME\.gemini\config\plugins" en Windows)
git add .
git commit -m "feat: nuevas mejoras en los plugins y skills"
git push
```

### Recibir actualizaciones en tus otros PCs
```bash
cd ~/.gemini/config/plugins
git pull
```

---

## 🧪 Verificación de Tests Automatizados

La suite incluye pruebas automatizadas para garantizar que los scripts de auditoría y relevo de sesión operen con código de salida 0:

```bash
# Ejecutar tests de architect-guardian (Handover, Pickup, Babysit, Report)
python -m unittest discover -s architect-guardian/tests -p "test_*.py"

# Ejecutar tests de doc-guardian (Auditoría de manifiestos y README)
python -m unittest discover -s doc-guardian/tests -p "test_*.py"
```
