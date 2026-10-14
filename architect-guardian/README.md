# 🏛️ Architect-Guardian: Plugin de Arquitectura de Software, Dominio y Calidad de Diseño

> El cuarto componente de la **Suite de los Guardianes** (`doc-guardian`, `docker-guardian`, `debug-guardian`, `architect-guardian`). Integra y hace contextual la disciplina clásica de ingeniería de software inspirada en John Ousterhout (*A Philosophy of Software Design*), Eric Evans (*Domain-Driven Design*), Martin Fowler (*Refactoring*) y las metodologías avanzadas de agentes de Matt Pocock.

---

## 🎯 ¿Qué problema resuelve?

Los modelos de lenguaje asistiendo en desarrollo tienden a acelerar la **entropía del software**:
1. **Módulos superficiales y pasamanos (*Shallow Modules / Middle Man*)**: Crean clases intermedias, wrappers vacíos o servicios delgados donde la interfaz es casi tan compleja como la implementación.
2. **Abstracciones prematuras (*Speculative Generality*)**: Inventan interfaces, adaptadores o capas genéricas para un único caso de uso (*"por si en el futuro se necesita"*), encareciendo el mantenimiento.
3. **Lenguaje difuso y pérdida de contexto**: Usan nombres ambiguos (`Manager`, `Helper`, `Handler`) y descripciones largas que saturan la ventana de contexto en vez de formalizar un vocabulario de dominio conciso (`GLOSSARY.md`).
4. **Descomposición caótica de tareas**: Abordan cambios complejos mediante capas horizontales desconectadas en lugar de cortes verticales completos (*tracer bullets*) con dependencias acíclicas explícitas.
5. **Auto-complacencia en revisiones**: Un agente que revisa su propio código tiende a mezclar estándares de código con cumplimiento de especificación, pasando por alto *scope creep* o regresiones de diseño.

**Architect-Guardian** vuelve esta disciplina **100% contextual y proactiva** sin necesidad de recordar comandos manuales.

---

## ✨ Características Principales

1. **Regla de Agente Obligatoria (`rules/AGENTS.md`)**:
   - Exige diseñar módulos profundos con alto apalancamiento y localidad.
   - Prohíbe pasamanos injustificados y abstracciones sin al menos dos adaptadores reales.
   - Impone el uso de un lenguaje de dominio preciso y criterios estrictos para ADRs (`docs/adr/`).
   - Guía la descomposición de tareas en grafos de dependencias (DAG) y cortes verticales.
   - Aplica revisión de código en dos ejes ciegos (*Estándares/Smells* vs. *Spec Alignment*).
2. **Referencias Técnicas Exhaustivas (`references/`)**:
   - `deep_modules.md`: Principios de profundidad, apalancamiento, costuras reales y test de eliminación.
   - `domain_modeling_and_glossary.md`: Lenguaje ubicuo, formato de `GLOSSARY.md` y criterios para ADRs.
   - `task_graph_decomposition.md`: Tracer bullets, frontera lista de ejecución y patrón *expand-contract*.
   - `two_axis_code_review.md`: Revisión independiente de estándares frente a requerimientos.
   - `fowler_code_smells.md`: Catálogo completo de 12 code smells de Fowler adaptados para IA.
3. **Herramienta CLI Integrada (`architect_guard.py`)**:
   - Detección de code smells en el diff de Git o archivos (`Mysterious Name`, `Message Chains`, `Speculative Generality`).
   - Auditoría de salud de artefactos de dominio (`GLOSSARY.md` y directorio `docs/adr/`).
   - Detección de grafos de tickets y cálculo de la frontera de tareas listas (*Ready Frontier*).

---

## 🛠️ Uso de la Herramienta CLI

```bash
# 1. Auditar arquitectura, artefactos de dominio y smells en el diff actual:
python C:/Users/Petiso/.gemini/config/plugins/architect-guardian/skills/architect-guardian/scripts/architect_guard.py .

# 2. Auditar exhaustivamente todos los archivos del proyecto (sin limitarse al diff):
python C:/Users/Petiso/.gemini/config/plugins/architect-guardian/skills/architect-guardian/scripts/architect_guard.py . --all-files
```

---

## 📁 Estructura del Plugin

```text
~/.gemini/config/plugins/architect-guardian/
├── plugin.json
├── README.md
├── rules/
│   └── AGENTS.md
└── skills/
    └── architect-guardian/
        ├── SKILL.md
        ├── references/
        │   ├── deep_modules.md
        │   ├── domain_modeling_and_glossary.md
        │   ├── task_graph_decomposition.md
        │   ├── two_axis_code_review.md
        │   └── fowler_code_smells.md
        └── scripts/
            └── architect_guard.py
```
