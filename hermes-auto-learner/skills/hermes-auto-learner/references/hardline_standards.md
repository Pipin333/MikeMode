# Estándares Hardline de Autoría de Skills (NousResearch / Hermes Specification)

Guía de especificación técnica obligatoria para la destilación y compilación de skills en el ecosistema Antigravity y `agentskills.io`. Todo skill generado por el motor de auto-aprendizaje debe cumplir estas reglas al 100% de forma determinista.

---

## 1. Reglas Inflexibles de Frontmatter YAML

```yaml
---
name: lowercase-kebab-case
description: Exactly one sentence <=60 chars ending with a period.
version: 0.1.0
platforms: [windows, linux, macos]
metadata:
  tags: [Category, Domain]
---
```

### Directivas de Campo:
- **`name`**:
  - Minúsculas separadas por guiones (`kebab-case`).
  - Máximo **64 caracteres**.
  - Sin espacios, caracteres especiales ni barras.
- **`description` (Regla Crítica del Router de Sistema)**:
  - **Exactamente una sola oración, $\le 60$ caracteres y terminando con un punto (`.`)**.
  - Describe la **capacidad técnica**, jamás la implementación ni el nombre del skill.
  - **Prohibido el lenguaje de marketing ("slop")**: palabras como *powerful*, *seamless*, *comprehensive*, *advanced*, *robust*, *ultimate*.
  - Si contiene dos puntos (`:`), debe encerrarse en comillas dobles.
  - *Fundamento Técnico*: Los indexadores de contexto de Antigravity y Claude cargan todas las descripciones en cada sesión para el enrutamiento de intenciones. Todo lo que exceda 60 caracteres es truncado silenciosamente en el router primario, degradando la tasa de selección del skill y consumiendo tokens innecesarios.
- **`version`**: Versión semántica inicial (`0.1.0`).
- **`platforms`**: Omitir si el skill es portable (código estándar Python/Node sin dependencias de OS). Especificar `[windows]`, `[linux]`, o `[macos]` solo si depende de comandos ligados al sistema operativo (ej. `powershell`, `systemctl`, `osascript`).

---

## 2. Orden Canónico de Secciones en `SKILL.md`

El cuerpo del archivo `SKILL.md` debe seguir este orden exacto sin omitir secciones salvo que no apliquen:

1. `# <Título Humano en Modo Título>`
   - Resumen conciso de 2-3 oraciones: qué hace, qué **NO** hace y su postura sobre dependencias (ej. "Solo stdlib", "Usa CLI uv").
2. `## When to Use`
   - Lista con viñetas de frases disparadoras exactas que el usuario o el agente reconocen para activar este skill.
3. `## Prerequisites`
   - Variables de entorno (`.env`), herramientas instaladas, claves de API o requisitos previos de sistema.
4. `## How to Run`
   - La invocación canónica y directa mediante las herramientas del agente (`run_command`, scripts en `scripts/`, etc.).
5. `## Quick Reference`
   - Tabla o lista compacta de comandos, subcomandos, banderas o endpoints sin narrativa.
6. `## Procedure`
   - Pasos numerados secuenciales con comandos exactos listos para copiar y ejecutar.
7. `## Pitfalls`
   - Errores comunes, trampas de entorno (ej. Windows vs Linux), límites de tasa (*rate limits*) y peculiaridades de APIs.
8. `## Verification`
   - Un único comando, aserción o prueba que certifique con código de salida 0 que el skill operó con éxito.

---

## 3. Arquitectura de Base de Conocimiento (Knowledge-Base Layout)

Para evitar la saturación de la ventana de contexto:

- **Límite de Líneas en `SKILL.md`**: El archivo raíz `SKILL.md` debe mantenerse en un rango de **100 a 200 líneas**.
- **Desglose en `references/`**: Si la documentación de origen es un manual extenso, un libro o una especificación de API masiva:
  - `SKILL.md` actúa como un índice delgado de navegación y protocolo de uso.
  - Cada capítulo o subtema denso se almacena en `references/<subtema>.md`.
  - El agente lee bajo demanda (`view_file`) únicamente el archivo de referencia que responde a la consulta del usuario (*Progressive Disclosure*).
- **Scripts en `scripts/`**: Todo código ejecutable de más de 15 líneas no debe inlinarse en el markdown; se persiste en `scripts/<herramienta>.py` o `.sh` y se referencia por ruta relativa.
