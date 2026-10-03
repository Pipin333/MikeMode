# Reglas Universales de Documentación para Cualquier Agente o Modelo de IA

Este documento contiene las directivas preconfiguradas para los principales ecosistemas de agentes de IA (Cursor, Claude Code, GitHub Copilot, Windsurf, Antigravity, etc.).

Al colocar estas reglas en tu repositorio, cualquier modelo que interactúe con el código asumirá el compromiso ineludible de actualizar la documentación ante cualquier cambio.

---

## 1. Para Google Antigravity & Herramientas con soporte AGENTS.md (`AGENTS.md` o `GEMINI.md`)

Crea un archivo llamado `AGENTS.md` o `GEMINI.md` en la raíz de tu proyecto con el siguiente contenido:

```markdown
# Directivas de Desarrollo y Mantenimiento de Documentación

## Regla de Integridad de Documentación (Doc-Guardian)
Toda modificación de código conlleva la obligación de revisar y sincronizar la documentación técnica:

1. **Sincronización en el mismo turno**: No finalices una respuesta de código sin antes verificar si el `README.md` o las guías en `docs/` necesitan reflejar los cambios realizados.
2. **Dependencias**: Si agregas, modificas o eliminas dependencias (`package.json`, `requirements.txt`, `pyproject.toml`, `Cargo.toml`, etc.), actualiza la sección de instalación y requisitos en el `README.md`.
3. **Variables de Entorno**: Si utilizas nuevas variables en código (`process.env`, `os.getenv`, etc.), regístralas de inmediato en `.env.example` y documéntalas en la tabla de configuración del `README.md`.
4. **Comandos y Scripts**: Si creas nuevos scripts (`npm run ...`, `python main.py ...`), documenta su propósito y sintaxis en la sección de Uso del `README.md`.
5. **Endpoints de API**: Si creas o alteras rutas, parámetros o respuestas, actualiza la sección de API / Endpoints.
6. **Reporte Final**: Concluye siempre tu respuesta con una breve sección `### 📝 Documentación Actualizada` resumiendo los cambios documentales realizados.
```

---

## 2. Para Claude Code (`CLAUDE.md`)

Crea un archivo llamado `CLAUDE.md` en la raíz de tu proyecto:

```markdown
# Claude Code Instructions

## Documentation Maintenance Rules
- Whenever you make changes to the codebase (adding features, fixing bugs, refactoring, or modifying configurations), you MUST inspect and update `README.md` and related docs before finishing.
- If dependencies are altered in package manifests, update the prerequisites and installation instructions.
- If new environment variables are referenced in code, ensure they are documented in both `.env.example` and the `README.md` environment variables section.
- If new scripts, CLI options, or endpoints are added, document their usage with concrete examples.
- Include a summary of documentation changes in your final response.
```

---

## 3. Para Cursor (`.cursorrules` o `.cursor/rules/doc-guardian.mdc`)

En `.cursorrules` (o `.cursor/rules/doc-guardian.mdc`):

```markdown
You are a meticulous software engineer pair programmer.

CRITICAL RULE - ALWAYS KEEP DOCUMENTATION IN SYNC:
Every time you modify, add, or refactor code:
1. Check if the README.md needs updates (installation, usage, env vars, scripts, API contracts).
2. If new environment variables are introduced, update .env.example and README.md.
3. If new dependencies or scripts are added, document them.
4. Never leave documentation updates for a separate step; do them in the same turn.
5. In your response, explicitly list the documentation updates you performed.
```

---

## 4. Para GitHub Copilot (`.github/copilot-instructions.md`)

Crea `.github/copilot-instructions.md`:

```markdown
# GitHub Copilot Custom Instructions

## Documentation Upkeep Requirement
- Any pull request or code change that introduces new configuration, dependencies, environment variables, or CLI commands MUST be accompanied by updates to `README.md` and `.env.example`.
- Keep README instructions tested, precise, and beginner-friendly.
```

---

## 5. Para Modelos Vía API / ChatGPT / Prompts de Sistema Genéricos

Si utilizas un agente personalizado vía API o chat, incluye esta cláusula en el `system_prompt`:

```text
[POLÍTICA DE DOCUMENTACIÓN CONTINUA]
Nunca completes una tarea de programación sin asegurarte de que la documentación del repositorio (principalmente el README.md y las variables de entorno en .env.example) esté 100% al día con el código modificado. Si agregas dependencias, variables o scripts, documéntalos antes de finalizar tu turno y reporta los cambios realizados.
```
