# Autoría Independiente de Tests (Test-Author Subagent)

Un test escrito por quien ya vio la implementación tiende a describir lo que el código *hace*, no lo que *debería* hacer. Esta guía rompe esa circularidad separando quién escribe el test de quién escribe el código.

---

## Cuándo aplicarlo

| Situación | ¿Subagente autor de tests? |
| :--- | :---: |
| Lógica de negocio o de dominio (facturación, cuotas, reglas de cálculo, permisos) | Sí |
| Bug confirmado cuya causa raíz toca lógica no trivial | Sí |
| Código crítico: seguridad, dinero, datos del usuario | Sí |
| El usuario lo pide explícitamente | Sí |
| Cambios triviales (renombrados, estilos, textos, configuración) | No |
| Prototipos desechables | No |

---

## Protocolo

1. **Preparar la especificación (agente principal)**: redacta un documento autocontenido con:
   - Comportamiento esperado o criterios de aceptación, expresados en términos del dominio.
   - Firma pública (nombre, parámetros, tipo de retorno) del módulo bajo prueba.
   - Ejemplos concretos de entrada y salida esperada. Si es lógica de negocio, pídeselos al usuario antes de seguir.
   - **Nunca** incluyas el cuerpo de la implementación, ni el diff de la corrección.
2. **Invocar al subagente autor** con solo ese documento y acceso de lectura a los tests y utilidades existentes. No debe poder leer el archivo de implementación.
3. **El subagente escribe los tests** y declara las suposiciones que tuvo que hacer porque la especificación era ambigua.
4. **Verificar rojo**: el agente principal ejecuta los tests y confirma que fallan por la razón esperada (aserción incumplida, no error de importación ni de sintaxis).
5. **Congelar**: los tests quedan en un commit propio, previo a la implementación.
6. **Implementar**: el agente principal corrige el código hasta ponerlos en verde.

---

## Reglas de no manipulación

- Durante la implementación, **está prohibido modificar, borrar o saltar (`skip`, `xit`, `@pytest.mark.skip`) los tests congelados**.
- Si un test congelado parece incorrecto, el agente se detiene y reporta al usuario la discrepancia entre la especificación y el test. La decisión es del usuario, no del agente.
- Las suposiciones declaradas por el subagente se presentan al usuario para confirmar o corregir.
- Si el test congelado pasa antes de implementar, no prueba nada: se descarta o se rehace.

---

## Plantilla del encargo al subagente

```text
Rol: autor de tests independiente.
Tienes la especificación de abajo y NO tienes acceso a la implementación.
Escribe tests que fallen si el comportamiento especificado no se cumple.
Cubre casos felices, bordes, entradas inválidas y errores esperados.
Cada aserción debe comparar contra un valor esperado derivado de la
especificación, nunca recalculado con la lógica que se está probando.
Al final, lista cada suposición que hiciste por ambigüedad.

Especificación:
<criterios de aceptación>

Firma pública:
<nombre, parámetros, retorno>

Ejemplos de entrada y salida:
<casos>
```

---

## Señales de que un test fue diseñado para pasar

- La aserción repite la lógica del código en vez de un valor esperado independiente.
- Todo está mockeado y no se ejercita comportamiento real.
- Solo hay casos felices.
- El nombre del test promete una cosa y la aserción comprueba otra.
- El test pasa con y sin la corrección aplicada.

---

## Límites del método

- El subagente comparte el mismo modelo base, por lo que puede heredar los mismos sesgos. Reduce la circularidad, no la elimina.
- Una especificación vaga produce tests vagos. Los ejemplos del usuario son la fuente más fiable.
- Para lógica crítica, combínalo con mutation testing (Stryker, `mutmut`, `cargo-mutants`) y con revisión humana de los tests.
