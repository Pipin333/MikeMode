# Cálculo del Radio de Explosión (Blast Radius) y Arqueología "Why"

Metodología de ingeniería para modificar código nuclear sin provocar regresiones catastróficas.

---

## 1. El Concepto de Radio de Explosión (*Blast Radius*)

El **radio de explosión** mide cuántos componentes, módulos y flujos aguas abajo dependen de una función, modelo de datos o interfaz.

### Protocolo de Análisis Previo:
1. **Mapeo de Puntos de Llamada (*Call Sites*)**:
   - Antes de modificar la firma o retorno de un método nuclear (ej. en `database.py`, esquemas ORM o endpoints compartidos), busca todas sus apariciones en el repositorio:
     ```bash
     git grep "nombre_de_la_funcion"
     ```
2. **Clasificación del Impacto**:
   - **Bajo Impacto**: La función solo es consumida por 1-2 módulos hermanos.
   - **Alto Impacto (Nuclear)**: La función es consumida transversalmente por modelos de base de datos, tareas en segundo plano o el frontend.
3. **Estrategia para Alto Impacto**:
   - Aplica el patrón **Expand-Contract** (mantener la firma vieja delegando a la nueva hasta migrar los llamadores en lotes) para evitar romper la compilación o suite de pruebas.

---

## 2. Arqueología de Código ("Why")

> **Ley de Chesterton**: *"No derribes una cerca hasta que sepas exactamente por qué fue construida en primer lugar."*

Cuando un agente encuentra código que parece arcaico, redundante o extraño:
1. **Inspección de Commits Previos**:
   ```bash
   git log -S "nombre_de_funcion" --oneline
   git log -p -n 1 <commit-hash>
   ```
2. **Comprensión de Contexto Histórico**:
   - Averigua si ese bloque responde a un workaround por un bug de un sistema operativo, un deadlock de base de datos o un caso borde histórico que el cliente reportó en el pasado.
3. **Validación de la Hipótesis**:
   - Solo refactoriza si puedes demostrar con un test automatizado que el caso borde sigue cubierto con la nueva implementación.
