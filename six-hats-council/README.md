# 🔮 Six Hats Council & MAGI System Skill

> Framework de deliberación técnica multidimensional y consenso democrático para agentes de IA. Combina el **método de los 6 Sombreros para Pensar de Edward de Bono** con el **Protocolo de Consenso Democrático MAGI de Neon Genesis Evangelion** mediante subagentes concurrentes e independientes (`invoke_subagent`).

---

## 💡 Dos Modos de Deliberación

### 1. 🔮 Modo 1: Protocolo MAGI de Evangelion (Subagentes Concurrentes)
Inspirado en el supercomputador de la Dra. Naoko Akagi, divide la decisión entre **tres personalidades ortogonales e intransigentes** ejecutadas en paralelo mediante subagentes aislados:

```
[ MELCHIOR-1 : AGREED ]      -> "Lógica formal, deep modules y coherencia algorítmica."
[ BALTHASAR-2: DENIED ]      -> "Riesgo crítico de migración sin rollback determinista."
[ CASPER-3   : CONDITIONAL ] -> "Aprobado si simplificamos la UX a un único paso."

>>> RESOLUCIÓN FINAL: 2-1 MAJORITY DECISION (APROBADO CON CONDICIONES)
>>> SALVAGUARDA VINCULANTE: Se exige expand-contract antes de desplegar.
```

- **🧠 MELCHIOR-1 (La Científica)**: ⚪ Blanco (Datos/Hechos) + 🔵 Azul (Deep Modules, invariantes de dominio, complejidad $O(n)$).
- **🛡️ BALTHASAR-2 (La Madre / Guardián)**: ⚫ Negro (Riesgos/Worst-case) + 🔴 Rojo (Instinto de preservación, blast radius, rollback).
- **⚡ CASPER-3 (La Mujer / Disruptora)**: 🟢 Verde (Pensamiento lateral/Creatividad) + 🟡 Amarillo (Valor/UX/ROI/80-20).

*Ventaja radical:* **Cero contaminación cruzada de contexto**. Cada subagente evalúa en un espacio de razonamiento independiente y emite su voto formal (`AGREED`, `DENIED`, `CONDITIONAL`).

### 2. 🎩 Modo 2: Consejo Secuencial de los 6 Sombreros (De Bono)
Para consultas rápidas dentro del mismo hilo conversacional, forzando polarización cognitiva en 6 facetas:
- ⚪ **Blanco**: Hechos puros y métricas sin opiniones.
- 🔴 **Rojo**: Intuición técnica y UX visceral.
- ⚫ **Negro**: Abogado del diablo y puntos de fallo.
- 🟡 **Amarillo**: Optimismo racional y ROI.
- 🟢 **Verde**: Pensamiento lateral y atajos radicales.
- 🔵 **Azul**: Director de orquesta y Plan Maestro.

---

## 🚀 Instalación

### Opción A: Global en Antigravity (Recomendada)
El plugin se ubica en:
```text
~/.gemini/config/plugins/six-hats-council/
├── plugin.json
└── skills/
    └── six-hats-council/
        ├── SKILL.md
        ├── references/
        │   ├── magi_protocol.md
        │   ├── hats_framework.md
        │   └── prompt_templates.md
        └── scripts/
            └── six_hats.py
```
*(Antigravity detecta y activa automáticamente los plugins en `~/.gemini/config/plugins/`)*.

---

## 🛠️ Cómo Usar la Skill

### Para Activar el Protocolo MAGI (Subagentes de Evangelion)
- *"Inicia el protocolo MAGI para evaluar si deberíamos migrar a WebSockets o SSE"*
- *"Consulta a MAGI: Melchior, Balthasar y Casper sobre este cambio arquitectónico"*
- *"Haz una votación de subagentes estilo Evangelion antes de tocar la base de datos"*

### Para Activar los 6 Sombreros Secuenciales
- *"Consulta con el consejo de los 6 sombreros sobre este diseño"*
- *"Aplica los 6 sombreros de Bono a esta propuesta técnica"*

### Vía CLI Local (Terminal)
```bash
# Modo MAGI (Evangelion)
python skills/six-hats-council/scripts/six_hats.py --magi "¿Deberíamos reescribir el parser en Rust?"

# Modo 6 Sombreros clásico
python skills/six-hats-council/scripts/six_hats.py "¿Deberíamos migrar a GraphQL?"
```

---

## 📂 Estructura de la Skill

```text
six-hats-council/
├── plugin.json                              # Manifiesto del plugin
├── README.md                                # Esta guía
└── skills/
    └── six-hats-council/
        ├── SKILL.md                         # Protocolos MAGI y Six Hats
        ├── references/
        │   ├── magi_protocol.md             # Especificación técnica del protocolo MAGI
        │   ├── hats_framework.md            # Límites estrictos de los 6 Sombreros
        │   └── prompt_templates.md          # Prompts para subagentes Melchior, Balthasar y Casper
        └── scripts/
            └── six_hats.py                  # CLI auxiliar con soporte --magi y --cli
```
