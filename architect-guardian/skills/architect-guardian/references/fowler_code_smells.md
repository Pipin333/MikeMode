# Catálogo de Code Smells (Martin Fowler Baseline)

Referencia rápida de olores de código extraídos de *Refactoring* (Capítulo 3) adaptados para auditorías de diffs y revisiones automatizadas por agentes.

---

| Code Smell | Síntoma en el Diff | Acción Correctiva |
| :--- | :--- | :--- |
| **Mysterious Name** | Funciones, tipos o variables cuyo nombre no revela qué hacen o contienen (`data`, `temp`, `res`, `doProcess`, `handler`). | Renombrar con un nombre revelador de intención. Si no surge un nombre honesto, el diseño es difuso. |
| **Duplicated Code** | La misma estructura lógica o bloques análogos aparecen en más de un lugar en el diff. | Extraer la lógica común a una función o módulo profundo reutilizable. |
| **Feature Envy** | Una función o método accede a los datos internos de otro objeto con mayor frecuencia que a los suyos propios. | Mover el método a la clase/módulo dueña de los datos. |
| **Data Clumps** | El mismo grupo de 3-4 parámetros siempre viaja junto en múltiples firmas (`street, city, zip`, `x, y, width, height`). | Empaquetar los campos en una clase de datos o tipo cohesivo. |
| **Primitive Obsession** | Uso de strings, números o tuplas para representar conceptos del dominio (`currency`, `email`, `phone`, `orderStatus`). | Crear un Value Object o tipo específico con sus validaciones e invariantes. |
| **Repeated Switches** | El mismo bloque `switch` o cascada `if/elif` sobre un enum o tipo se repite en varios archivos. | Reemplazar por polimorfismo o por una tabla de despacho (*lookup table*) compartida. |
| **Shotgun Surgery** | Un único cambio conceptual obliga a retocar pequeños fragmentos en decenas de archivos dispersos. | Reubicar lo que cambia junto dentro de un único módulo profundo cohesionado. |
| **Divergent Change** | Un mismo archivo o módulo se modifica continuamente por razones completamente distintas y desacopladas. | Separar el módulo en unidades independientes según el principio de responsabilidad única. |
| **Speculative Generality** | Parámetros no utilizados, métodos genéricos abstractos o hooks añadidos "por si se necesitan en el futuro". | Eliminar código especulativo. Mantener el diseño simple hasta que surja la necesidad real. |
| **Message Chains** | Navegaciones profundas del tipo `a.getB().getC().getD().getValue()`. | Ocultar la delegación encapsulando la consulta en el objeto inicial (*Law of Demeter*). |
| **Middle Man** | Una clase o módulo no hace más que delegar el 90% de sus métodos hacia otra clase sin añadir valor. | Eliminar el intermediario y conectar al consumidor directamente con la clase real. |
| **Refused Bequest** | Una subclase que ignora o sobreescribe con excepciones la mayor parte de los métodos heredados de su padre. | Reemplazar la herencia por composición (*Favor composition over inheritance*). |
