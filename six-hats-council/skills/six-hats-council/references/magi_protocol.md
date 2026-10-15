# Protocolo de Deliberación y Consenso MAGI (Supercomputador Tripartito)

Inspirado en el sistema de supercomputación **MAGI de Neon Genesis Evangelion** (creado por la Dra. Naoko Akagi), este protocolo divide una decisión técnica crítica entre tres personalidades cognitivas ortogonales ejecutadas mediante **subagentes concurrentes independientes** (`invoke_subagent`).

El objetivo es eliminar el sesgo de confirmación y la complacencia (*sycophancy*) que ocurre cuando un único hilo de LLM intenta autocriticarse.

---

## 🧬 La Tríada MAGI y el Mapeo con los 6 Sombreros

Los 6 Sombreros de Pensamiento de Edward de Bono se agrupan en tres polos dialectales intransigentes:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        BLUE HAT (Orquestador)                          │
│                     (Facilitador & Tally de Votos)                     │
└───────────────┬───────────────────┬───────────────────┬────────────────┘
                │                   │                   │
                ▼                   ▼                   ▼
     ┌────────────────────┐┌────────────────────┐┌────────────────────┐
     │     MELCHIOR-1     ││    BALTHASAR-2     ││      CASPER-3      │
     │   (La Científica)  ││ (La Madre/Guardián)││(La Mujer/Disruptor)│
     ├────────────────────┤├────────────────────┤├────────────────────┤
     │ ⚪ Blanco (Hechos) ││ ⚫ Negro (Riesgos)  ││ 🟢 Verde (Lateral) │
     │ 🔵 Azul (Estruct)  ││ 🔴 Rojo (Instinto) ││ 🟡 Amarillo (Valor)│
     └────────────────────┘└────────────────────┘└────────────────────┘
```

### 1. 🧠 MELCHIOR-1: La Científica (Lógica Pura y Arquitectura)
- **Sombreros**: ⚪ Blanco (Datos, métricas, restricciones factuales) + 🔵 Azul (Deep Modules, invariantes de dominio, complejidad algorítmica).
- **Criterio rector**: "La verdad matemática y la coherencia arquitectónica son innegociables."
- **Evaluación**:
  - ¿Introduce pasamanos superficiales (*Middle Man*) o indirecciones innecesarias?
  - ¿Cumple con la ley de Conway, modularidad profunda y encapsulamiento estricto?
  - ¿Cuál es la complejidad temporal y espacial $O(n)$?
- **Voto `DENIED` si**: La solución es arquitectónicamente chapucera, rompe invariantes o acopla módulos indebidamente.

### 2. 🛡️ BALTHASAR-2: La Madre / El Guardián (Preservación y Riesgo)
- **Sombreros**: ⚫ Negro (Abogado del diablo, vectores de fallo, vulnerabilidades) + 🔴 Rojo (Instinto de conservación, estrés operacional).
- **Criterio rector**: "La primera obligación del sistema es sobrevivir y no autodestruirse."
- **Evaluación**:
  - ¿Cuál es el radio de explosión (*blast radius*) si esto falla en producción a las 3:00 AM?
  - ¿Existe un plan de rollback limpio y determinista?
  - ¿Qué dependencias externas, licencias o vectores de seguridad introduce?
  - ¿Existen pruebas deterministas que certifiquen el comportamiento antes de desplegar?
- **Voto `DENIED` si**: El cambio tiene alto riesgo de rotura colateral sin rollback o carece de tests deterministas.

### 3. ⚡ CASPER-3: La Mujer / La Disruptora (Pragmatismo, UX y Velocidad)
- **Sombreros**: 🟢 Verde (Pensamiento lateral, atajos innovadores) + 🟡 Amarillo (Optimismo fundamentado, ROI, experiencia de usuario).
- **Criterio rector**: "El software que no entrega valor rápido al usuario humano es código muerto."
- **Evaluación**:
  - ¿Cómo impacta esto en la experiencia del usuario final (*delight*, latencia percibida)?
  - ¿Podemos lograr el 80% del beneficio con el 20% del esfuerzo eliminando código?
  - ¿Estamos ante un caso de sobre-ingeniería especulativa (*YAGNI*)?
  - ¿Hay un atajo creativo radical que simplifique radicalmente el problema?
- **Voto `DENIED` si**: La propuesta es una sobre-ingeniería que agrega fricción al usuario o atrasa el proyecto sin justificación real.

---

## 🗳️ Mecanismo de Votación y Resolución de Conflictos

Cada subagente debe concluir obligatoriamente con un voto estandarizado:

| Voto | Significado | Condición |
| :--- | :--- | :--- |
| **`AGREED`** | Aprobación Total | La propuesta satisface plenamente los criterios del nodo. |
| **`CONDITIONAL`** | Aprobación con Estipulaciones | Aprobado **únicamente** si se cumple una lista de condiciones obligatorias. |
| **`DENIED`** | Rechazo Tajante | La propuesta viola principios fundamentales no negociables. |

### Reglas de Resolución (Teoría de Juegos)
Al ser un sistema de **3 nodos (impar)**, el empate es matemáticamente imposible:

1. **3 - 0 UNANIMOUS CONSENSUS (Vía Libre)**:
   - Los tres nodos aprueban (`AGREED`). El plan procede a implementación inmediata.
2. **2 - 1 MAJORITY APPROVAL (Aprobación con Salvaguarda)**:
   - La propuesta se aprueba por mayoría, pero **las objeciones del nodo disidente se convierten en salvaguardas obligatorias** que deben integrarse en el plan de acción antes de escribir código.
3. **1 - 2 o 0 - 3 REJECTED (Veto / Descarte)**:
   - La propuesta queda bloqueada. El orquestador debe reformular la arquitectura o plantear una alternativa antes de volver a deliberar.

---

## 📝 Integración con Architecture Decision Records (ADRs)

Cuando la deliberación involucre una decisión difícil de revertir (requisito de `Architect-Guardian`), el dictamen final de MAGI se exporta directamente a `docs/adr/00X-[nombre-decision].md` incluyendo:
- La tabla de votación oficial de MAGI.
- Las tesis de los tres nodos.
- El compromiso de mitigación para el voto disidente (en caso de 2-1).
