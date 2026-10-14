# Revisión de Código en Dos Ejes Ciegos (Two-Axis Code Review)

Metodología de revisión de diffs para evitar el sesgo de auto-complacencia en agentes de IA.

---

## 1. Por qué Dos Ejes Separados

Un cambio de código puede fallar de dos maneras completamente ortogonales:
1. **Pasa los estándares, pero falla la spec**: Sigue perfectamente la guía de estilo, tipos limpios y sin code smells, pero implementa algo distinto a lo que el usuario pidió o introduce *scope creep*.
2. **Pasa la spec, pero destruye los estándares**: Hace exactamente lo que pedía el ticket, pero introduce duplicación de código, parches frágiles, nombres opacos y viola las convenciones del repositorio.

Si un solo revisor evalúa ambos aspectos a la vez, el éxito en un eje suele eclipsar las deficiencias del otro. La solución es **evaluarlos de forma aislada e independiente**.

---

## 2. Eje 1: Estándares y Fowler Smells Baseline

Audita el diff contra dos fuentes:
1. **Estándares documentados del repositorio**: `AGENTS.md`, `CODING_STANDARDS.md`, `CONTRIBUTING.md`, reglas de linter del proyecto. (Los estándares del repo siempre tienen prioridad).
2. **Línea base de olores de código (Fowler Baseline)**: Heurísticas de diseño orientadas a la legibilidad y mantenimiento futuro:
   - *Mysterious Name*: Identificadores que no comunican su intención.
   - *Duplicated Code*: Fragmentos lógicos análogos repetidos en múltiples archivos.
   - *Feature Envy*: Métodos que operan intensivamente sobre datos de otro objeto en lugar del propio.
   - *Primitive Obsession*: Uso de tipos primitivos sueltos en vez de tipos de dominio cohesivos.
   - *Data Clumps*: Parámetros que siempre viajan juntos y deberían ser un tipo/struct.
   - *Shotgun Surgery*: Un solo cambio conceptual obligó a editar decenas de archivos dispersos.
   - *Speculative Generality*: Parámetros o capas abstractas introducidas "por si acaso".

---

## 3. Eje 2: Fidelidad Estricta a la Especificación

Audita el diff exclusivamente contra el requerimiento original, issue o spec:
1. **Requerimientos Faltantes o Incompletos**: Casos de uso o criterios de aceptación prometidos que no están cubiertos en el código o tests.
2. **Comportamiento No Solicitado (*Scope Creep*)**: Modificaciones o funcionalidades añadidas que nadie pidió y que aumentan la superficie de mantenimiento.
3. **Lógica Errónea**: Casos donde la función parece implementada, pero las condiciones límite, cálculos o respuestas no se ajustan a la especificación acordada.

---

## 4. Estructura del Reporte

```markdown
## 🔍 Revisión de Código en Dos Ejes

### Eje 1: Estándares y Fowler Smells
- [ ] Hallazgo 1: [Nombre del smell o regla] en `archivo:línea` -> [Propuesta de solución]
- [x] Sin violaciones de estándares detectadas.

### Eje 2: Fidelidad a la Especificación
- [ ] Hallazgo 1: [Requisito faltante / Scope creep] -> [Cita del requerimiento original]
- [x] Todos los criterios de aceptación verificados.
```
