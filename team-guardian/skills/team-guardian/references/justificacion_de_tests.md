# Justificacion de cambios en tests

Archivo: `.scratch/justificacion-tests.md`. Por cada cambio sensible que reporte el gate, un bloque con las cuatro etiquetas y la ruta del archivo.

```markdown
## tests/test_cuotas.py

Antes: assert total_cuotas(100000, 3) == 33333
Ahora: assert total_cuotas(100000, 3) == 100000
Fuente: ejemplo del usuario: la suma de las cuotas debe igualar el monto original.
Prueba de que falla: con la version anterior de total_cuotas() el nuevo test falla (99999 != 100000).
```

## Que convence y que no

| Convence | No convence |
| :--- | :--- |
| La especificacion o un ejemplo del usuario contradice la aserción anterior. | "El codigo devuelve ese valor". |
| Se muestra el test nuevo fallando contra el codigo defectuoso. | "Era un test fragil" sin evidencia. |
| El test se reemplaza por otro mas estricto. | Borrar el test sin reemplazo. |

Si el usuario no queda convencido, se revierte el cambio del test o se rehace la correccion.
