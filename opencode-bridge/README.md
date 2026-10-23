# OpenCode Bridge Plugin (`opencode-bridge`)

[![Status](https://img.shields.io/badge/Status-Active-success?style=flat)]()
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat)]()
[![Models](https://img.shields.io/badge/Models-Free%20Pool-brightgreen?style=flat)]()

Puente de interoperabilidad local entre **Google Antigravity** y **OpenCode Desktop**. Permite delegar tareas pesadas, refactorizaciones y consultas técnicas hacia el pool de modelos gratuitos de OpenCode (**DeepSeek V4.1 Flash**, **GLM-5.3 Flash**, **Nemotron 3.5 Super VL**, **Flint 40B**) sin consumir tokens ni cuotas de APIs pagadas.

---

## 🚀 Características Principales

- **Delegación Táctica (`/delegate`):** Deriva tareas directamente desde el chat de Antigravity hacia el modelo más apto en OpenCode.
- **Cero Costo & Cero Cuota:** Utiliza los modelos *free-tier* integrados en OpenCode Desktop.
- **Comunicación Local Efímera:** Se comunica con el daemon local de OpenCode (`localhost:28894`), crea una sesión de consulta, extrae la respuesta con su bloque de pensamiento (*reasoning*) y limpia la sesión automáticamente.
- **Salvaguardas de MAGI (Balthasar-2 & Melchior-1):**
  - **Secret Scrubber:** Purga patrones de credenciales, llaves API y archivos `.env` antes del despacho.
  - **Sandbox de Ejecución:** El modelo delegado actúa únicamente como asesor/generador de texto. Antigravity mantiene la autoridad exclusiva de ejecución en el sistema anfitrión.
  - **Fail-Fast:** Timeout estricto de 60 segundos para evitar bloqueos en el runtime.

---

## 📦 Estructura del Plugin

```
opencode-bridge/
├── plugin.json
├── README.md
├── scripts/
│   └── opencode_bridge.py      # Runner y conector local contra OpenCode CLI
└── skills/
    └── delegate/
        └── SKILL.md            # Definición del skill y slash command /delegate
```

---

## 🛠️ Uso por Línea de Comandos (CLI)

```powershell
# 1. Comprobar estado del daemon de OpenCode
python scripts/opencode_bridge.py status

# 2. Listar modelos activos
python scripts/opencode_bridge.py models

# 3. Consultar a DeepSeek V4.1 Flash Free
python scripts/opencode_bridge.py ask -m deepseek-v4.1-flash-free -p "¿Cómo optimizar esta función?"

# 4. Consultar a GLM-5.3 Flash Free (Pensamiento profundo y arquitectura)
python scripts/opencode_bridge.py ask -m glm-5.3-flash-free -p "Evalúa la cohesión de este módulo"
```

---

## 💬 Uso en Antigravity Chat

Escribe en el chat:

- `/delegate deepseek-v4.1-flash-free Refactoriza este archivo eliminando bucles anidados`
- O en lenguaje natural: *"Pídele una segunda opinión a DeepSeek sobre este bug"*
