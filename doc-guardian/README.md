# 🛡️ Doc-Guardian Plugin para Antigravity

Plugin global de **Antigravity** que garantiza la integridad y actualización continua de la documentación técnica (`README.md`, `.env.example`, `docs/`) ante cualquier cambio en el código fuente.

Diseñado tanto para agentes de **Antigravity** como para cualquier otro modelo o asistente de IA (**Cursor, Claude Code, GitHub Copilot, Windsurf, ChatGPT**).

---

## 📦 Contenido del Plugin

- **`plugin.json`**: Manifiesto del plugin.
- **`rules/AGENTS.md`**: Regla activa global que se fusiona con las reglas de todos los agentes de Antigravity, obligándolos a no olvidar la documentación cada vez que toquen código.
- **`skills/doc-guardian/`**:
  - `SKILL.md`: Protocolo paso a paso para el agente (detección de impacto, auditoría de dependencias, variables de entorno y edición quirúrgica de documentación).
  - `scripts/doc_guard.py`: Script CLI multiplataforma en Python para auditar proyectos y detectar código modificado sin documentar.
  - `references/universal_agent_rules.md`: Guía y fragmentos listos para usar en `AGENTS.md`, `CLAUDE.md`, `.cursorrules` y `.github/copilot-instructions.md`.
  - `references/readme_template.md`: Plantilla estándar y modular para nuevos READMEs.

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
   - Al ejecutar `doc_guard.py init` en un proyecto (o copiar el snippet de `universal_agent_rules.md`), se genera un archivo `AGENTS.md` en la raíz del repositorio. Las herramientas compatibles leen estas directivas y fuerzan al modelo a mantener el README sincronizado.
