# 🛡️ Doc-Guardian Plugin para Antigravity

Plugin global de **Antigravity** que garantiza la integridad, actualización continua de la documentación técnica (`README.md`, `.env.example`, `docs/`) y el cumplimiento de **estándares de código limpio y docstrings (PEP 8, PEP 257 o equivalentes idiomáticos)** ante cualquier cambio en el código fuente.

Diseñado tanto para agentes de **Antigravity** como para cualquier otro modelo o asistente de IA (**Cursor, Claude Code, GitHub Copilot, Windsurf, ChatGPT**).

---

## 📦 Contenido del Plugin

- **`plugin.json`**: Manifiesto del plugin.
- **`rules/AGENTS.md`**: Regla activa global que se fusiona con las directivas de todos los agentes de Antigravity, obligándolos a cumplir con PEP 8/257 (o equivalentes) y a no olvidar la documentación cada vez que toquen código.
- **`skills/doc-guardian/`**:
  - `SKILL.md`: Protocolo paso a paso para el agente (estándares PEP 8 y PEP 257, detección de impacto, auditoría de dependencias, variables de entorno y edición quirúrgica de documentación).
  - `scripts/doc_guard.py`: Script CLI multiplataforma en Python para auditar proyectos y detectar código modificado sin documentar o sin reglas.
  - `references/universal_agent_rules.md`: Guía y fragmentos listos para usar en `AGENTS.md`, `CLAUDE.md`, `.cursorrules` y `.github/copilot-instructions.md`.
  - `references/readme_template.md`: Plantilla estándar y modular para nuevos READMEs.

---

## 📐 Estándares de Código y Docstrings Exigidos

1. **Python**:
   - **PEP 8**: Nomenclatura `snake_case`, tipado estático obligatorio (`type hints`), sangría de 4 espacios y longitud de línea razonable.
   - **PEP 257**: Docstrings estructurados con triples comillas `"""..."""` en módulos, clases y funciones públicas con secciones `Args:`, `Returns:` y `Raises:`.
2. **TypeScript / JavaScript**:
   - ESLint / Prettier, tipos e interfaces explícitos, y **TSDoc / JSDoc** (`/** ... */`) en elementos exportados.
3. **Rust, Go, Java, C#**:
   - Estándares oficiales (`rustfmt` + `rustdoc`, `gofmt` + `godoc`, Google Java Style + `Javadoc`, C# + XML comments).

---

## 🚀 Uso Rápido con el Asistente CLI

El script `doc_guard.py` se puede ejecutar en cualquier proyecto:

```bash
# Auditar el repositorio o proyecto actual:
python C:/Users/Petiso/.gemini/config/plugins/doc-guardian/skills/doc-guardian/scripts/doc_guard.py check

# Instalar reglas universales (AGENTS.md / GEMINI.md) en el proyecto actual:
python C:/Users/Petiso/.gemini/config/plugins/doc-guardian/skills/doc-guardian/scripts/doc_guard.py init
```

---

## 🤖 ¿Cómo Funciona para Cualquier Modelo de IA?

1. **En Antigravity**:
   - Al estar instalado en `~/.gemini/config/plugins/doc-guardian`, la regla `rules/AGENTS.md` y la skill `doc-guardian` están automáticamente disponibles para todos tus proyectos y conversaciones.
2. **En Otros Agentes (Cursor, Claude Code, Copilot, etc.)**:
   - Al ejecutar `doc_guard.py init` en un proyecto (o copiar el snippet de `universal_agent_rules.md`), se genera un archivo `AGENTS.md` en la raíz del repositorio. Las herramientas compatibles leen estas directivas y fuerzan al modelo a mantener el código con PEP 8/257 y el README sincronizado.
