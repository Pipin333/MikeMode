# 🎩 Six Hats Council Skill

> Adaptación del concepto de [llm-council-skill](https://github.com/gcpdev/llm-council-skill), pero en lugar de invocar múltiples proveedores de modelos (ChatGPT, Gemini, etc.), utiliza el **mismo modelo LLM** jugando deliberadamente al **método de los 6 Sombreros para Pensar de Edward de Bono**.

---

## 💡 ¿Por qué los 6 Sombreros en un Único Modelo?

En el enfoque multi-LLM tradicional:
- Se requieren múltiples claves de API (`OPENAI_API_KEY`, etc.), acarreando costes extras y fricción.
- Los modelos externos suelen converger en respuestas promedio, complacientes o similares.
- Se pierde contexto del proyecto y del código local al comunicarse con APIs externas.

Con el **Consejo de los 6 Sombreros**:
- **Cero claves adicionales**: Utiliza directamente el modelo activo de tu asistente.
- **Polarización cognitiva deliberada**: Fuerza al modelo a adoptar posturas ortogonales y extremas:
  - ⚪ **Blanco**: Hechos puros, datos y métricas (sin opiniones).
  - 🔴 **Rojo**: Intuición técnica, *gut feeling* y experiencia de usuario (sin justificación lógica).
  - ⚫ **Negro**: Abogado del diablo, puntos de fallo catastróficos, seguridad y deuda técnica.
  - 🟡 **Amarillo**: Optimismo racional, ventajas competitivas, eficiencia y valor.
  - 🟢 **Verde**: Creatividad lateral, atajos innovadores y alternativas radicales.
  - 🔵 **Azul**: Director de orquesta, resolución de tensiones y **Plan de Implementación Definitivo**.
- **Contexto completo**: El modelo conoce tus archivos, arquitectura y dependencias locales.

---

## 🚀 Instalación

### Opción A: Global en Antigravity (Recomendada)
Para tener la skill disponible en **todos tus proyectos**:
El plugin se ubica en:
```text
~/.gemini/config/plugins/six-hats-council/
├── plugin.json
└── skills/
    └── six-hats-council/
        ├── SKILL.md
        ├── references/
        └── scripts/
```
*(Antigravity detecta y activa automáticamente los plugins en `~/.gemini/config/plugins/`)*.

### Opción B: Por Proyecto en Antigravity
Copia la carpeta de la skill a la raíz de tu repositorio:
```bash
mkdir -p .agents/skills
cp -r six-hats-council/skills/six-hats-council .agents/skills/
```

### Opción C: En Claude Code
Copia la carpeta a `.claude/skills/`:
```bash
mkdir -p .claude/skills
cp -r six-hats-council/skills/six-hats-council .claude/skills/
```

---

## 🛠️ Cómo Usar la Skill

Simplemente pídele a tu asistente deliberar antes de tomar una decisión o escribir código:

- *"Consulta con el consejo: ¿Deberíamos migrar este módulo a WebSockets o mantener SSE?"*
- *"Aplica los 6 sombreros de Bono a este diseño de base de datos"*
- *"Haz una sesión del consejo de sombreros antes de presentar el plan de implementación"*
- *"Analiza los riesgos y alternativas creativas de esta refactorización con los 6 sombreros"*

---

## 📂 Estructura de la Skill

```text
six-hats-council/
├── plugin.json                              # Manifiesto para instalación global como plugin
├── README.md                                # Esta guía
└── skills/
    └── six-hats-council/
        ├── SKILL.md                         # Definición de la skill, frontmatter y protocolo
        ├── references/
        │   ├── hats_framework.md            # Límites estrictos y directivas de cada sombrero
        │   └── prompt_templates.md          # Prompts para llamadas aisladas / subagentes
        └── scripts/
            └── six_hats.py                  # CLI auxiliar para ejecutar deliberaciones
```
