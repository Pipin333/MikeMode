# Reglas Universales de Documentación y Calidad de Código para Cualquier Agente o Modelo de IA

Este documento contiene las directivas preconfiguradas para los principales ecosistemas de agentes de IA (Cursor, Claude Code, GitHub Copilot, Windsurf, Antigravity, etc.).

Al colocar estas reglas en tu repositorio, cualquier modelo que interactúe con el código asumirá el compromiso ineludible de actualizar la documentación y escribir código que cumpla con **PEP 8 y PEP 257 (o sus equivalentes idiomáticos)**.

---

## 1. Para Google Antigravity & Herramientas con soporte AGENTS.md (`AGENTS.md` o `GEMINI.md`)

Crea un archivo llamado `AGENTS.md` o `GEMINI.md` en la raíz de tu proyecto con el siguiente contenido:

```markdown
# Directivas de Desarrollo, Documentación y Estándares de Código

## Regla de Calidad y Documentación Continua (Doc-Guardian)
Toda modificación o creación de código conlleva la obligación de cumplir con los siguientes estándares:

1. **Estándares de Código y Docstrings**:
   - En Python: Cumplir estrictamente con **PEP 8** (estilo, tipado, nomenclatura snake_case) y **PEP 257** (docstrings descriptivos con triples comillas, Args, Returns, Raises en funciones y clases públicas).
   - En otros lenguajes: Cumplir con sus equivalentes oficiales (TSDoc/JSDoc en TypeScript/JavaScript, rustdoc en Rust, godoc en Go, Javadoc en Java).
2. **Sincronización en el mismo turno**: No finalices una respuesta de código sin antes verificar si el `README.md` o las guías en `docs/` necesitan reflejar los cambios realizados.
3. **Dependencias**: Si agregas, modificas o eliminas dependencias (`package.json`, `requirements.txt`, `pyproject.toml`, `Cargo.toml`, etc.), actualiza la sección de instalación y requisitos en el `README.md`.
4. **Variables de Entorno**: Si utilizas nuevas variables en código (`process.env`, `os.getenv`, etc.), regístralas de inmediato en `.env.example` y documéntalas en la tabla de configuración del `README.md`.
5. **Comandos y Scripts**: Si creas nuevos scripts (`npm run ...`, `python main.py ...`), documenta su propósito y sintaxis en la sección de Uso del `README.md`.
6. **Endpoints de API**: Si creas o alteras rutas, parámetros o respuestas, actualiza la sección de API / Endpoints.
7. **Reporte Final**: Concluye siempre tu respuesta con una breve sección `### 📝 Documentación Actualizada y Estándares` resumiendo los cambios y la validación de estilo realizada.
```

---

## 2. Para Claude Code (`CLAUDE.md`)

Crea un archivo llamado `CLAUDE.md` en la raíz de tu proyecto:

```markdown
# Claude Code Instructions

## Code Standards & Documentation Rules
- Code Quality: All code written must adhere strictly to PEP 8 (style & type hints) and PEP 257 (docstrings with Args, Returns, Raises) for Python, or language equivalents (TSDoc/JSDoc for TypeScript/JS, rustdoc for Rust, godoc for Go).
- Whenever you make changes to the codebase (adding features, fixing bugs, refactoring, or modifying configurations), you MUST inspect and update `README.md` and related docs before finishing.
- If dependencies are altered in package manifests, update the prerequisites and installation instructions.
- If new environment variables are referenced in code, ensure they are documented in both `.env.example` and the `README.md` environment variables section.
- If new scripts, CLI options, or endpoints are added, document their usage with concrete examples.
- Include a summary of code standards adherence and documentation changes in your final response.
```

---

## 3. Para Cursor (`.cursorrules` o `.cursor/rules/doc-guardian.mdc`)

En `.cursorrules` (o `.cursor/rules/doc-guardian.mdc`):

```markdown
You are a meticulous software engineer pair programmer.

CRITICAL RULES - CODE QUALITY & DOCUMENTATION:
1. Adhere strictly to PEP 8 (style, naming, type hints) and PEP 257 (comprehensive docstrings) for Python, or exact equivalents for other languages (TSDoc/JSDoc, rustdoc, godoc).
2. Every time you modify, add, or refactor code:
   - Check if the README.md needs updates (installation, usage, env vars, scripts, API contracts).
   - If new environment variables are introduced, update .env.example and README.md.
   - If new dependencies or scripts are added, document them immediately.
3. Never leave documentation or docstrings for a separate step; do them in the same turn.
4. In your response, explicitly state compliance with code standards and list the documentation updates performed.
```

---

## 4. Para GitHub Copilot (`.github/copilot-instructions.md`)

Crea `.github/copilot-instructions.md`:

```markdown
# GitHub Copilot Custom Instructions

## Code Standards & Documentation Upkeep Requirement
- All generated code must adhere to PEP 8 and PEP 257 standards for Python, and TSDoc/rustdoc/godoc for other languages, including complete docstrings and type annotations.
- Any pull request or code change that introduces new configuration, dependencies, environment variables, or CLI commands MUST be accompanied by updates to `README.md` and `.env.example`.
- Keep README instructions tested, precise, and beginner-friendly.
```

---

## 5. Para Modelos Vía API / ChatGPT / Prompts de Sistema Genéricos

Si utilizas un agente personalizado vía API o chat, incluye esta cláusula en el `system_prompt`:

```text
[POLÍTICA DE CALIDAD DE CÓDIGO Y DOCUMENTACIÓN CONTINUA]
Escribe siempre código que cumpla con los estándares PEP 8 (estilo y tipado) y PEP 257 (docstrings estructurados) en Python, o equivalentes en otros lenguajes (TSDoc, rustdoc, godoc). Además, nunca completes una tarea de programación sin asegurarte de que la documentación del repositorio (principalmente el README.md y las variables de entorno en .env.example) esté 100% al día con el código modificado. Reporta siempre el cumplimiento al finalizar tu respuesta.
```
