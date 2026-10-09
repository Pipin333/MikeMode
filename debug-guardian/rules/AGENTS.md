# Regla de Depuración Rigurosa, Calidad de Testing e Higiene de Código (Debug-Guardian)

## Mandato Obligatorio para Agentes y Modelos de IA
Cada vez que soluciones un error, implementes una funcionalidad o refactorices código en cualquier proyecto, **es obligatorio cumplir con los cuatro mandatos de Debug-Guardian antes de concluir tu respuesta**:

1. **Análisis de Causa Raíz (RCA) vs. "Parche Curita"**:
   - **Prohibido silenciar errores**: Jamás captures excepciones vacías (`except Exception: pass`, `catch (e) {}` sin manejo o log estructurado).
   - **Prohibido debilitar tipado**: Prohibido usar `as any`, `@ts-ignore`, `cast(Any, ...)` o silenciar linters con comentarios `@eslint-disable` para eludir fallos de tipos.
   - **Atacar el origen**: Si una variable llega como `None` o `undefined`, investiga *por qué* el flujo upstream la envía vacía en lugar de limitarte a poner un `if (!val) return;` que oculte el verdadero defecto de arquitectura.

2. **Reproducción Previa y Prevención de Regresiones (Test-Driven Bugfixing)**:
   - **Paso 1: Test en Rojo**: Ante un bug confirmado, escribe primero un test automatizado (unitario o de integración) que reproduzca exactamente el fallo y falle de manera determinista.
   - **Paso 2: Corrección en Verde**: Modifica el código de negocio hasta que el test reproductor pase limpiamente.
   - **Paso 3: Suite Completa**: Ejecuta las pruebas existentes del módulo o proyecto para certificar que la solución no introdujo regresiones en otros flujos.

3. **Higiene Estricta de Código (Cero Residuos de Depuración)**:
   - Antes de dar por finalizada la tarea, inspecciona minuciosamente los diffs y elimina cualquier artefacto temporal de diagnóstico:
     - Instrucciones de logging temporal: `console.log()`, `print(f"DEBUG: ...")`, `println!()`, `System.out.println()`.
     - Puntos de interrupción: `debugger;`, `breakpoint()`, `import pdb; pdb.set_trace()`.
     - Código muerto comentado (`// function oldImplementation() { ... }`).
     - Notas temporales como `// TODO: remove later`, `// FIXME: parche temporal`.

4. **Verificación Automatizada Ejecutable**:
   - Si el proyecto cuenta con un entorno o comando de pruebas (`pytest`, `vitest`, `npm test`, `cargo test`, `go test`, `mvn test`), es OBLIGATORIO ejecutar las pruebas mediante la terminal y verificar que concluyan con código de salida 0.

---

## Protocolo de Reporte Final
En tu respuesta final al usuario, incluye siempre un bloque explícito:

```markdown
### 🐞 Depuración, Testing e Higiene (Debug-Guardian)
- **Causa Raíz**: [Explicación concisa del defecto original y por qué ocurría].
- **Test de Regresión**: [Archivo y función del test creado/actualizado para blindar el caso].
- **Higiene de Código**: [Confirmado: sin prints/console.log residuales ni código comentado].
- **Estado de Pruebas**: [Ejecutadas con éxito (código de salida 0 / X tests pasados)].
```
