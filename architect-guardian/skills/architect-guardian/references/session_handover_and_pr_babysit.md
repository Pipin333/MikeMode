# Continuidad de Sesión (`pause-safely` / `session-pickup`), Aterrizaje de PRs (`babysit`) y Reporte Bajo Demanda (`/report`)

## 1. Pausa Segura y Relevo entre Sesiones (`/handover` & `/pickup`)

Cuando una tarea abarca múltiples sesiones o la ventana de contexto se acerca a su límite, es crítico evitar la "amnesia entre sesiones" (donde el nuevo agente repite experimentos fallidos o pierde el hilo del grafo de dependencias DAG).

### A. Protocolo `/handover` (`pause-safely`)
Antes de pausar una sesión en vuelo:
1. Deja el árbol de trabajo en un estado coherente (commits limpios o cambios claramente acotados) y asegúrate de que `.scratch/` esté excluido en `.gitignore`.
2. Ejecuta el generador determinista de snapshot:
   ```bash
   python C:/Users/Petiso/.gemini/config/plugins/architect-guardian/skills/architect-guardian/scripts/architect_guard.py --handover \
     --summary "Resumen exacto de los cortes verticales completados y verificados" \
     --next-step "Siguiente corte vertical concreto de la frontera activa" \
     --dead-ends "Hipótesis o parches descartados que el próximo agente NO debe repetir"
   ```
3. Esto escribe `.scratch/HANDOVER.md` con la telemetría exacta de Git (`branch`, `HEAD`, estado del árbol y frontera DAG).

### B. Protocolo `/pickup` (`session-pickup`)
Al iniciar una nueva conversación sobre un proyecto con trabajo en vuelo:
1. Ejecuta:
   ```bash
   python C:/Users/Petiso/.gemini/config/plugins/architect-guardian/skills/architect-guardian/scripts/architect_guard.py --pickup
   ```
2. Verifica que el `HEAD` y la rama coincidan con el snapshot, respeta estrictamente la sección **Dead-Ends** y retoma de inmediato el **Próximo Corte Vertical** sin pedirle al usuario que vuelva a explicar el contexto.

---

## 2. Aterrizaje Autónomo de Ramas y PRs (`/babysit`)

Inspirado en el playbook `babysit` de `pstack`, cuando el usuario solicita llevar una rama o Pull Request hasta estado *merge-ready*:
1. **Inspección Determinista de Convergencia**:
   ```bash
   python C:/Users/Petiso/.gemini/config/plugins/architect-guardian/skills/architect-guardian/scripts/architect_guard.py --babysit
   ```
2. **Sincronización con la Rama Base**:
   - Ejecuta `git fetch origin` y verifica si existen conflictos con `origin/main`.
   - Si hay conflictos de merge, resuélvelos preservando las invariantes de ambos lados (nunca descartando cambios a ciegas con `--ours` o `--theirs` sin analizar el historial con `git log`).
3. **Verificación de CI y Suite Local**:
   - Ejecuta la suite de pruebas local y, si el repositorio cuenta con GitHub CLI (`gh pr checks`), inspecciona el estado de los pipelines remotos hasta que todos los checks estén en verde.

---

## 3. Auditoría Ejecutiva Consolidada Bajo Demanda (`/report`)

Por defecto, los 5 Guardianes del **Modo Mike™** operan en **modo silencioso**: aplican todas sus reglas y verificaciones internamente sin saturar el chat con plantillas de reporte al final de cada mensaje.

Cuando el usuario escribe `/report` (o pide explícitamente el reporte de los guardianes):
1. Ejecuta el orquestador consolidado:
   ```bash
   python C:/Users/Petiso/.gemini/config/plugins/architect-guardian/skills/architect-guardian/scripts/architect_guard.py --report
   ```
2. Presenta en la respuesta los bloques de auditoría de los guardianes pertinentes (`Architect-Guardian`, `Debug-Guardian`, `Doc-Guardian`, `Docker-Guardian`, `Frontend-Guardian`).
