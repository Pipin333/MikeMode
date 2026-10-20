# Regla de Disciplina de Equipo y Honestidad de Tests (Team-Guardian)

## Mandato para Agentes y Modelos de IA

1. **Ramas y commits**: las ramas son `main` o `feat|fix|chore/<slug-kebab-case>`. Los commits siguen Conventional Commits (`tipo(alcance)?: descripcion`, tipos `feat fix docs ci refactor test chore`, encabezado de hasta 72 caracteres). Si el repositorio no tiene el hook, ofrece instalarlo con `team_guard.py install-hook`.

2. **Prohibido debilitar tests para ponerlos en verde**: si tu cambio borra un test, elimina o altera una asercion, o agrega un `skip`, debes detenerte antes de dar la tarea por terminada:
   - Genera el diff y ejecuta `team_guard.py gate-test-changes`.
   - Si el estado es `blocked_missing_justification`, escribe `.scratch/justificacion-tests.md` con, por cada cambio, las etiquetas `Antes:`, `Ahora:`, `Fuente:` (especificacion, ejemplo del usuario o documentacion; nunca "porque el codigo lo hace") y `Prueba de que falla:` (como se comprobo que el test nuevo falla si el codigo esta mal). Cita la ruta de cada archivo afectado.
   - Explica la justificacion al usuario en detalle. **Si no lo convence, el gate falla** y debes revertir el test o rehacer la correccion.

3. **Prohibido autoaprobar**: nunca ejecutes `approve-test-changes` por tu cuenta. La aprobacion es del usuario y queda atada al hash del diff; cualquier cambio posterior la invalida.

4. **Honestidad de verificacion**: si no pudiste ejecutar una verificacion, escribe "no verificado". Nunca afirmes que algo pasa sin haber visto la salida real del comando.

## Reporte bajo demanda (`/report`)

Solo cuando el usuario lo pida, incluye `### 🤝 Disciplina de Equipo (Team-Guardian)` con rama y commits validados, estado del gate de tests y cambios sensibles pendientes de aprobacion.
