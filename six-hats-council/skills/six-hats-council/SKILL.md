---
name: six-hats-council
description: Deliberación técnica profunda, consenso democrático estilo MAGI de Evangelion con subagentes concurrentes y metodología de los Seis Sombreros de Bono. Úsalo cuando el usuario pida "consultar a MAGI", "iniciar protocolo MAGI", "votación estilo Evangelion", "consultar al consejo", "analizar con los 6 sombreros" o solicite una evaluación rigurosa antes de tomar decisiones técnicas irreversibles.
---

# Consejo de Deliberación Técnica: MAGI & Six Hats

Este protocolo proporciona dos modos de evaluación arquitectónica multidimensional para resolver dilemas técnicos complejos sin caer en el sesgo de confirmación ni en la complacencia (*sycophancy*) de un único hilo de pensamiento:

1. **🔮 Modo 1: Protocolo de Consenso Democrático MAGI (Subagentes Concurrentes - Estilo Evangelion)**:
   Inspirado en el supercomputador tripartito de la Dra. Naoko Akagi en *Neon Genesis Evangelion*. Invoca a **tres subagentes concurrentes e independientes** (`MELCHIOR-1`, `BALTHASAR-2`, `CASPER-3`) mediante `invoke_subagent` para que deliberen en paralelo sin contaminarse y emitan votos soberanos (`AGREED`, `DENIED`, `CONDITIONAL`).
2. **🎩 Modo 2: Deliberación Secuencial de los 6 Sombreros de Edward de Bono**:
   Para reflexiones rápidas dentro del mismo hilo conversacional, forzando al modelo a adoptar posturas dialectales ortogonales (Blanco, Rojo, Negro, Amarillo, Verde, Azul).

---

## 🔮 MODO 1: PROTOCOLO DE CONSENSO DEMOCRÁTICO MAGI (Subagentes)

### Cuándo Activar el Protocolo MAGI
Activa este modo preferente ante decisiones de alto impacto o cuando el usuario utilice expresiones como:
- *"Inicia el protocolo MAGI para decidir si..."*
- *"Consulta a MAGI: Melchior, Balthasar y Casper sobre este cambio"*
- *"Haz una votación de subagentes estilo Evangelion"*
- *"Somete esta arquitectura al consejo tripartito de MAGI"*
- Ante cualquier decisión técnica **difícil de revertir** (criterio de ADR de `Architect-Guardian`).

### La Tríada MAGI y Mapeo con los 6 Sombreros

| Nodo MAGI | Arquetipo de Naoko Akagi | Sombreros de Bono Integrados | Enfoque y Criterio de Voto |
| :--- | :--- | :--- | :--- |
| **🧠 MELCHIOR-1** | La Científica | ⚪ **Blanco** (Datos/Métricas) + 🔵 **Azul** (Estructura/Deep Modules) | **Lógica Pura y Coherencia:** Evalúa modularidad profunda, complejidad $O(n)$, interfaces limpias y principios DDD. Vota `DENIED` ante pasamanos superficiales o acoplamiento desordenado. |
| **🛡️ BALTHASAR-2** | La Madre / El Guardián | ⚫ **Negro** (Abogado del Diablo/Riesgos) + 🔴 **Rojo** (Instinto/Seguridad) | **Preservación y Aversión al Riesgo:** Evalúa el peor escenario (*worst-case*), radio de explosión (*blast radius*), reversibilidad/rollback y necesidad de tests deterministas. Vota `DENIED` si hay riesgo de fallo catastrófico en producción. |
| **⚡ CASPER-3** | La Mujer / La Disruptora | 🟢 **Verde** (Creatividad/Disrupción) + 🟡 **Amarillo** (Valor/UX/ROI) | **Pragmatismo, UX y Velocidad:** Evalúa la regla 80/20, deleite del usuario final, valor de negocio y atajos laterales que eliminen código. Vota `DENIED` ante sobre-ingeniería masturbatoria que demore la entrega sin aportar valor. |

### Cómo Invocar los Subagentes MAGI
El agente orquestador debe invocar a los tres subagentes en una **única llamada concurrente** utilizando la herramienta `invoke_subagent`:

```json
{
  "Subagents": [
    {
      "TypeName": "self",
      "Role": "MAGI-1 MELCHIOR (Scientist)",
      "Prompt": "Eres MELCHIOR-1 (La Científica). Evalúa el siguiente dilema con Sombrero Blanco y Azul (datos, modularidad profunda, complejidad O(n), DDD): [DESCRIPCIÓN]. Concluye con VOTO: [AGREED | DENIED | CONDITIONAL], MOTIVO y ESTIPULACIONES."
    },
    {
      "TypeName": "self",
      "Role": "MAGI-2 BALTHASAR (Mother/Guardian)",
      "Prompt": "Eres BALTHASAR-2 (La Madre/Guardián). Evalúa el siguiente dilema con Sombrero Negro y Rojo (peor escenario, blast radius, rollback, seguridad, tests): [DESCRIPCIÓN]. Concluye con VOTO: [AGREED | DENIED | CONDITIONAL], MOTIVO y ESTIPULACIONES."
    },
    {
      "TypeName": "self",
      "Role": "MAGI-3 CASPER (Woman/Disruptor)",
      "Prompt": "Eres CASPER-3 (La Mujer/Disruptora). Evalúa el siguiente dilema con Sombrero Verde y Amarillo (pragmatismo 80/20, UX, valor de negocio, pensamiento lateral): [DESCRIPCIÓN]. Concluye con VOTO: [AGREED | DENIED | CONDITIONAL], MOTIVO y ESTIPULACIONES."
    }
  ]
}
```

### Reglas de Decisión del Orquestador
Al recibir las 3 respuestas independientes:
- **3 - 0 UNANIMOUS CONSENSUS**: Aprobación inmediata.
- **2 - 1 MAJORITY APPROVAL**: Se aprueba por mayoría, pero **las estipulaciones del nodo disidente son mandatos obligatorios** que se integran en el plan.
- **0 - 3 o 1 - 2 REJECTED**: Veto del sistema. Se debe reformular la propuesta.
- Si la decisión es de alto impacto, documentar el veredicto en `docs/adr/00X-[decision].md`.

### Formato de Salida Visual MAGI (Estilo NERV)

```markdown
# 🔮 SISTEMA MAGI: DELIBERACIÓN TÁCTICA TRIPARTITA

```
╔══════════════════════════════════════════════════════════════════════╗
║                       MAGI SUPERCOMPUTER SYSTEM                      ║
║                     NERV TOKYO-3 ARCHITECTURE GRID                   ║
╚══════════════════════════════════════════════════════════════════════╝
```

### 1. Votación de los Nodos Soberanos

| Nodo MAGI | Arquetipo / Sombreros | Voto Oficial | Dictamen Técnico Principal |
| :--- | :--- | :---: | :--- |
| **MELCHIOR-1** | 🧠 Científica (⚪ Blanco + 🔵 Azul) | **AGREED** | "Estructura modular profunda con interfaz simple y cohesión alta." |
| **BALTHASAR-2** | 🛡️ Madre (⚫ Negro + 🔴 Rojo) | **CONDITIONAL** | "Aprobado solo con patrón expand-contract y tests de regresión previos." |
| **CASPER-3** | ⚡ Mujer (🟢 Verde + 🟡 Amarillo) | **AGREED** | "Acelera la entrega y reduce la fricción de usuario en 40%." |

### 2. Veredicto del Consenso
**`>>> VEREDICTO FINAL: 3-0 CONSENSO CON CONDICIONES (MAJORITY PASS)`**

### 3. Tesis Individuales de los Nodos
- **Melchior-1 (Análisis Formal)**: ...
- **Balthasar-2 (Matriz de Riesgo y Blast Radius)**: ...
- **Casper-3 (Valor de Usuario y Atajos Laterales)**: ...

### 4. Salvaguardas Obligatorias (Mandato de Balthasar / Disidentes)
1. ...

### 5. Plan de Acción Aprobado por MAGI
1. ...
```

---

## 🎩 MODO 2: CONSEJO CLÁSICO DE BONO (Un solo hilo)

Para consultas breves de exploración rápida, ejecuta el flujo secuencial clásico:
1. 🔵 **Sombrero Azul**: Encuadre del problema y criterios de éxito.
2. ⚪ **Sombrero Blanco**: Datos duros y métricas sin opiniones.
3. 🔴 **Sombrero Rojo**: Gut feeling técnico e instinto de UX.
4. 🟢 **Sombrero Verde**: Creatividad y pensamiento lateral.
5. ⚫ **Sombrero Negro**: Riesgos, puntos de fallo y auditoría implacable.
6. 🟡 **Sombrero Amarillo**: Optimismo lógico, beneficios y ROI.
7. 🔵 **Sombrero Azul**: Síntesis ejecutiva y Plan Maestro.

---

## Referencias
- Protocolo y teoría detallada de MAGI: [magi_protocol.md](./references/magi_protocol.md).
- Límites cognitivos de los 6 Sombreros: [hats_framework.md](./references/hats_framework.md).
- Prompts para subagentes y CLI: [prompt_templates.md](./references/prompt_templates.md).
- CLI ejecutable local: [six_hats.py](./scripts/six_hats.py).
