# 🧹 Higiene de Código y Eliminación de Residuos de Depuración

Un buen ingeniero de software no deja huellas de su proceso de depuración en la base de código final. Este documento resume los principios de **Higiene Estricta de Debug**.

---

## 🚫 Catálogo de Residuos Prohibidos en Código de Producción

| Lenguaje / Ecosistema | Residuo de Diagnóstico | Alternativa Correcta |
| :--- | :--- | :--- |
| **JavaScript / TypeScript** | `console.log(...)`, `console.debug(...)` | Logger estructurado (`pino`, `winston`) en nivel debug, o eliminar completamente. |
| **JavaScript / TypeScript** | `debugger;` | Utilizar puntos de interrupción del IDE, nunca en el código fuente. |
| **Python** | `print(f"DEBUG: ...")`, `print(variable)` | `logging.getLogger(__name__).debug(...)` o eliminar antes del commit. |
| **Python** | `breakpoint()`, `pdb.set_trace()` | Eliminar antes de entregar la respuesta. |
| **Go** | `fmt.Println("llegó aquí")` | `slog.Debug(...)` o eliminar. |
| **Rust** | `println!("{:?}", var)` | `tracing::debug!(...)` o eliminar. |
| **Todos** | Grandes bloques de código comentado | Utilizar el historial de Git (`git log`). Si un bloque no se usa, bórralo. |
| **Todos** | `// TODO: quitar esto luego`, `// FIXME: parche` | Resolver el problema en el mismo turno o crear un issue formal. |

---

## 🔍 Checklist de Pre-Entrega (Pre-Flight Hygiene)

Antes de emitir el mensaje final al usuario o solicitar feedback:

1. **Revisión de Diff**:
   - Ejecuta `git diff` o audita los archivos modificados.
   - ¿Aparece algún `print` o `console.log` añadido durante la sesión para ver valores? -> **Elimínalo**.
2. **Cierre de Recursos (Leak Prevention)**:
   - ¿Se abrieron sockets, cursores de base de datos o streams de archivo?
   - Asegúrate de que estén dentro de un `try...finally`, `with` statement (Python) o bloque de liberación automática (`defer` en Go, `using` en C#).
3. **Gestión de Promesas y Asincronía**:
   - En TypeScript/JavaScript: ¿Hay alguna llamada a una función asíncrona sin `await` ("floating promise")?
   - En Python: ¿Se usó `await` en todas las corrutinas requeridas?
4. **Validación de Linters y Tests**:
   - Ejecuta el script de auditoría:
     ```bash
     python C:/Users/Petiso/.gemini/config/plugins/debug-guardian/skills/debug-guardian/scripts/debug_guard.py check
     ```
