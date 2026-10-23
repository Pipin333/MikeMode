---
name: delegate
description: Delega tareas analíticas, refactorizaciones y contrastes de código hacia los modelos gratuitos de OpenCode Desktop (DeepSeek V4.1 Flash, GLM-5.3 Flash, Nemotron 3.5) mediante comunicación local sin consumir cuotas de API. Actívalo con /delegate o cuando el usuario pida consultar a DeepSeek, GLM o delegar a OpenCode.
---

# Delegación Táctica a OpenCode Desktop (`/delegate`)

Este skill permite a Antigravity derivar tareas especializadas o consultas analíticas hacia los modelos de **OpenCode Desktop**, aprovechando su pool gratuito y local sin consumir tokens ni cuotas de APIs pagadas.

---

## 1. Cuándo activar la delegación

- Cuando el usuario escriba `/delegate [modelo] [tarea]`.
- Cuando el usuario pida:
  - *"Pregúntale a DeepSeek cómo optimizar esta función"*.
  - *"Pídele una segunda opinión a GLM sobre esta arquitectura"*.
  - *"Delega esta refactorización a OpenCode"*.
  - *"Consulta a Nemotron sobre este diseño frontend"*.
- Como soporte técnico para deliberaciones de MAGI (`six-hats-council`).

---

## 2. Modelos disponibles y catálogo táctico

| Identificador | Familia | Especialidad / Cuándo delegar |
| :--- | :--- | :--- |
| **`deepseek-v4.1-flash-free`** *(Default)* | DeepSeek | **Coding de alta velocidad:** Algoritmos, refactorizaciones, typescript/astro, depuración de bugs sintácticos y unit tests. |
| **`glm-5.3-flash-free`** | Zhipu AI | **Razonamiento y arquitectura:** Revisión de requerimientos, planes paso a paso, análisis lógico en español nativo. |
| **`nemotron-3.5-super-vl-free`** | NVIDIA | **UI & Visión:** Análisis de interfaces web, accesibilidad, CSS y layouts. |
| **`flint-40b-free`** | Flint | Inferencia analítica general de peso medio (40B). |
| **`mimo-v2.6-flash-free`** | MiMo | Respuestas ultra-cortas y directas para formateo. |
| **`qwen2.5-coder:7b`** | Ollama Local | Fallback búnker 100% offline (corre en tu GPU local). |

---

## 3. Protocolo de Ejecución

Para delegar una tarea, ejecuta el script oficial del puente mediante la herramienta de terminal:

```powershell
python "C:\Users\Petiso\.gemini\config\plugins\opencode-bridge\scripts\opencode_bridge.py" ask -m <MODEL_ID> -p "<PROMPT_SANITIZADO>"
```

### Argumentos del comando:
- `-m, --model`: ID del modelo (por defecto `deepseek-v4.1-flash-free`).
- `-p, --prompt`: La tarea, código o pregunta específica a responder.
- `--json`: (Opcional) Retorna la respuesta y el bloque de pensamiento en JSON estructurado.
- `--agent`: `general` (por defecto) o `build` (para tareas de construcción).
- `--keep-session`: Conserva la sesión en OpenCode si el usuario quiere seguirla en la interfaz gráfica.

---

## 4. Reglas de Seguridad (Mandato de MAGI / Balthasar-2)

1. **Aislamiento de Ejecución:** El modelo delegado en OpenCode solo devuelve texto y propuestas. **Jamás se le otorgan permisos directos para modificar el repositorio ni ejecutar comandos**.
2. **Arbitraje del Agente:** Antigravity recibe la propuesta de DeepSeek/GLM, la audita contra las reglas del proyecto (`Architect-Guardian`, `Debug-Guardian`), y la aplica de forma segura si es correcta.
3. **Scrubber Automático:** El puente purga automáticamente variables de entorno, llaves API y credenciales antes de enviarlas al modelo.
