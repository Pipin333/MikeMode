# Descomposición de Tareas en Grafos de Dependencia (DAG) y Tracer Bullets

Técnicas de ingeniería para estructurar el trabajo antes de implementarlo, maximizando el paralelismo y evitando conflictos de merge entre subagentes.

---

## 1. Tracer Bullets Verticales vs. Capas Horizontales

### Corte Horizontal (Antipatrón)
- Tarea 1: Crear todas las tablas y migraciones de base de datos.
- Tarea 2: Crear todos los modelos de dominio.
- Tarea 3: Crear todos los endpoints REST.
- Tarea 4: Crear las pantallas UI.
*Problema*: Nada funciona hasta el final de la última tarea. La retroalimentación es tardía y los errores de diseño se descubren tarde.

### Tracer Bullet Vertical (Recomendado)
Cada tarea corta una franja estrecha pero **completa** a través de todas las capas:
- Tarea 1: Crear el flujo de registro de usuario extremo a extremo (migración de 1 tabla, 1 endpoint `/register`, 1 formulario básico, test de integración que certifique el flujo completo).
- Tarea 2: Crear el flujo de confirmación por email (lógica de token, endpoint `/verify`, pantalla de confirmación, test).

Cada corte vertical completado es **demostrable, verificable y fusionable** en la rama principal sin dejar código huérfano.

---

## 2. El Grafo de Tareas y la Frontera de Ejecución (*Ready Frontier*)

Las tareas no forman una lista secuencial plana; forman un **Grafo Acíclico Dirigido (DAG)** de dependencias declaradas explícitamente (`Blocked by`).

```text
       [ Ticket 01: Modelo Base ]
             /            \
            v              v
  [ Ticket 02: API ]   [ Ticket 03: Auth ]   <- Frontera de Tareas Listas (Paralelizable)
            \              /
             v            v
      [ Ticket 04: UI Integrada ]
```

### Reglas de Ejecución:
1. **La Frontera Lista (*Ready Frontier*)**: Cualquier tarea cuyos bloqueadores ya hayan sido completados puede ejecutarse de inmediato.
2. **Paralelismo de Subagentes**: Cuando existan múltiples tareas en la frontera (ej. Ticket 02 y Ticket 03), pueden asignarse a subagentes independientes en branches/worktrees separados sin riesgo de colisión.
3. **Punteros de Contexto**: La comunicación entre tareas debe hacerse mediante punteros de archivo y referencias (`specs/01-auth.md`, `git log`, `docs/adr/`), no repitiendo información ya disponible.

---

## 3. Refactorizaciones Masivas: El Patrón Expand-Contract

Cuando un refactor tiene un **radio de explosión masivo** (afecta a cientos de llamadas en todo el proyecto, como renombrar una columna de base de datos o modificar la firma de una función nuclear), una reescritura masiva de un solo golpe romperá la compilación y los tests en todas las ramas.

### Fases de Expand-Contract:
1. **Expandir (*Expand*)**:
   - Introduce la nueva función, método o columna **junto** a la antigua.
   - La antigua pasa a delegar internamente a la nueva o se marca como obsoleta (*deprecated*).
   - Los tests existentes siguen en verde.
2. **Migrar (*Migrate*)**:
   - Migra los puntos de llamada en lotes acotados (por carpeta, submódulo o feature).
   - Cada lote constituye un ticket pequeño y verificable en verde.
3. **Contraer (*Contract*)**:
   - Una vez que ningún consumidor utilice la forma antigua, elimínala definitivamente en un ticket final.
