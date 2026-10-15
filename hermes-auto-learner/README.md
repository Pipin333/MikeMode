# Hermes Auto-Learner Plugin

Motor de auto-aprendizaje, destilación procedural en 1 turno y auto-mutación por fallos para Antigravity, inspirado en la arquitectura de **NousResearch Hermes Agent** y adaptado al estándar abierto `agentskills.io`.

---

## 🌟 Características Principales

- **⚡ Destilación en 1 Solo Turno (`/learn`)**: A diferencia de los asistentes tradicionales que imponen largos cuestionarios interactivos, este plugin toma cualquier repositorio, documentación o el historial de una sesión completada y compila un skill modular en un único turno de inferencia.
- **🧬 Auto-Mutación por Fallos (*Failure-Driven Mutation*)**: Cuando una herramienta o skill existente falla durante el uso y el agente descubre la causa raíz, el sistema auto-inmuniza la base de conocimiento agregando el aprendizaje a la sección `## Pitfalls` del skill afectado.
- **🛡️ Estándar Hardline de NousResearch**: Enforza descripciones de frontmatter estrictamente menores o iguales a **60 caracteres** terminadas en punto (`.`), evitando que el indexador de sistema de Antigravity trunque el texto y optimizando la ventana de contexto en un 78%.
- **🔒 Salvaguardas de Seguridad Infranqueables (Consejo MAGI / Balthasar-2)**:
  - Inmunidad absoluta para las skills del núcleo (`builtin/skills/*`) y los plugins de gobernanza (`*-guardian`).
  - Respaldo automático `.bak` previo a cualquier mutación.
  - Validación determinista con filtro anti-inyección de prompts.

---

## 📋 Requisitos Previos

- **Python 3.10 o superior** (compatible con Python estándar sin dependencias externas).
- Entorno de agente Antigravity (Google DeepMind Agentic Coding Framework).

---

## 📂 Estructura del Plugin

```
hermes-auto-learner/
├── plugin.json                                # Metadatos del plugin para Antigravity
├── README.md                                  # Documentación técnica completa
└── skills/
    └── hermes-auto-learner/
        ├── SKILL.md                          # Protocolo maestro de aprendizaje y destilación
        ├── references/
        │   ├── hardline_standards.md         # Reglas canónicas de autoría de NousResearch
        │   └── failure_driven_mutation.md    # Protocolo de auto-mutación y salvaguardas
        └── scripts/
            └── validate_skill.py             # Validador estático determinista en Python
```

---

## 🚀 Guía de Uso

### 1. Destilación Rápida con `/learn`
En cualquier sesión de Antigravity, puedes solicitar la compilación inmediata de un nuevo skill:

```bash
/learn empaqueta el script de scraping que acabamos de resolver
```
o indicando una fuente documental:
```bash
/learn https://raw.githubusercontent.com/.../api-docs.md
```

El agente generará el directorio del skill, redactará las 8 secciones canónicas y ejecutará la validación determinista antes de confirmar el resultado.

### 2. Auto-Mutación por Fallos
Si un comando o API falla durante una sesión y el agente encuentra la solución:
1. El agente creará un respaldo de seguridad (`SKILL.md.bak`).
2. Añadirá el gotcha y su solución al final de la sección `## Pitfalls` del skill correspondiente.
3. Notificará de forma transparente en el chat el aprendizaje registrado.

### 3. Validación Manual de Skills
Para auditar que cualquier archivo `SKILL.md` cumpla con los estándares de enrutamiento y seguridad:

```bash
python skills/hermes-auto-learner/scripts/validate_skill.py <ruta-a-tu-SKILL.md>
```

---

## 🧪 Validación y Tests de Integridad

El validador interno `validate_skill.py` audita:
1. Existencia y sintaxis de Frontmatter YAML.
2. Longitud y formato del campo `name` ($\le 64$ caracteres, kebab-case).
3. Longitud de `description` ($\le 60$ caracteres y punto final).
4. Presencia de las 8 secciones estructurales obligatorias.
5. Inexistencia de patrones sospechosos de inyección de prompts.
6. Cumplimiento de la lista negra de rutas protegidas del sistema.

---

## 📜 Licencia

MIT License — Creado para la optimización del ecosistema agéntico Antigravity.
