# Regla de Arquitectura, Modelado de Dominio, Descomposición y Revisión en Dos Ejes (Architect-Guardian)

## Mandato Obligatorio para Agentes y Modelos de IA
Cada vez que diseñes, refactorices, implementes o revises código o arquitectura en cualquier proyecto, **es obligatorio cumplir con los cuatro mandatos de Architect-Guardian antes de concluir tu respuesta**:

1. **Diseño de Módulos Profundos vs. Pasamanos Superficiales (*Deep Modules & Real Seams*)**:
   - **Módulos Profundos (*A Philosophy of Software Design*)**: Maximiza el apalancamiento (*leverage*) y la localidad (*locality*). Diseña módulos con un comportamiento sustancial y rico detrás de una interfaz pequeña, limpia y fácil de consumir.
   - **Prohibido el "Middle Man"**: Prohibido crear clases, envoltorios o funciones pasamanos superfluas que solo delegan llamadas sin agregar invariantes, transformación o valor tangible.
   - **Regla de Costuras Reales (*Real Seams*)**: No introduzcas interfaces abstractas, adaptadores ni capas de indirección especulativas a menos que existan al menos dos implementaciones reales concurrentes que las requieran (*One adapter is a hypothetical seam; two adapters is a real seam*).
   - **Test de la Eliminación**: Si al imaginar borrar un módulo su complejidad se desvanece por completo, era un pasamanos injustificado; si su complejidad se desparrama sobre $N$ consumidores, el módulo es legítimo y debe profundizarse.

2. **Modelado de Dominio Ubicuo (DDD) y Registros de Decisión (ADR)**:
   - **Lenguaje Ubicuo y Vocabulario Preciso**: Prohibido el uso de nombres genéricos, borrosos o sobrecargados (`Manager`, `Handler`, `Helper`, `Processor`, `Data`, `Service` ambiguo). Utiliza el término exacto del dominio del negocio.
   - **Glosario Vivo (`GLOSSARY.md`)**: Si el proyecto cuenta con un archivo `GLOSSARY.md`, o si el dominio técnico/de negocio introduce términos que se prestan a confusión, mantén y consulta activamente el glosario para unificar variables, tipos y funciones.
   - **Criterio Estricto para ADRs (`docs/adr/`)**: Registra o propón un *Architecture Decision Record* únicamente cuando se cumplan simultáneamente tres condiciones:
     1. Es **difícil de revertir** (el coste de cambiar de opinión más tarde es significativo).
     2. Resultaría **sorprendente o confusa sin contexto** para un futuro desarrollador o agente.
     3. Es el **fruto de un trade-off real** entre dos o más alternativas viables analizadas.

3. **Descomposición de Tareas en Grafos de Dependencia (DAG) y Cortes Verticales**:
   - **Tracer Bullets Verticales**: Divide el trabajo de gran envergadura en cortes verticales estrechos pero completos (desde la entrada/API hasta la persistencia y sus tests integrados), nunca en capas horizontales desacopladas que no puedan probarse de extremo a extremo.
   - **Frontera de Ejecución Concurrente (*Ready Frontier*)**: Modela las dependencias entre tareas como un grafo acíclico dirigido (DAG) identificando explícitamente qué tareas bloquean a cuáles. Las tareas no bloqueadas pertenecen a la frontera activa y pueden ejecutarse concurrentemente sin conflictos de merge.
   - **Refactorizaciones Transversales (*Expand-Contract*)**: Si un cambio mecánico tiene un radio de explosión que afecta a todo el proyecto (ej. reescribir firmas centrales o tipos compartidos), nunca intentes cambiarlo de golpe rompiendo la compilación. Aplica el patrón *expand-contract*:
     1. *Expandir*: Añade la nueva forma junto a la antigua preservando compatibilidad.
     2. *Migrar*: Actualiza los consumidores en lotes independientes asegurando que la suite siga pasando en cada lote.
     3. *Contraer*: Elimina la forma obsoleta cuando ya no existan consumidores.

4. **Revisión de Código en Dos Ejes Ciegos (*Two-Axis Review*)**:
   - Antes de dar por finalizada una intervención significativa o un conjunto de cambios, evalúa el diff bajo dos lentes completamente independientes para evitar que un aspecto enmascare al otro:
     - **Eje 1: Estándares y Fowler Code Smells**: Evalúa *Mysterious Name*, *Duplicated Code*, *Feature Envy*, *Data Clumps*, *Primitive Obsession*, *Repeated Switches*, *Shotgun Surgery*, *Speculative Generality*, *Message Chains* y *Refused Bequest*.
     - **Eje 2: Fidelidad Estricta a la Especificación**: Verifica exhaustivamente: (a) requerimientos solicitados que hayan quedado sin implementar o a medias; (b) código no solicitado que represente *scope creep*; (c) lógica aparentemente implementada que no satisfaga los criterios de aceptación exactos.

---

## Protocolo de Reporte Final
En tu respuesta final al usuario, incluye siempre el bloque explícito:

```markdown
### 🏛️ Arquitectura, Dominio y Diseño (Architect-Guardian)
- **Módulos y Costuras**: [Explicación de la profundidad de interfaces creadas/modificadas y justificación de costuras].
- **Modelado de Dominio (DDD)**: [Vocabulario de negocio alineado / GLOSSARY.md o ADR registrado si aplica].
- **Descomposición & Flujo**: [Corte vertical completado / Gestión de la frontera de tareas].
- **Revisión en Dos Ejes**: [Estándares & Code Smells evaluados | Fidelidad estricta a la spec sin scope creep].
```
