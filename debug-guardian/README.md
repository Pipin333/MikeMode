# 🐞 Debug-Guardian: Plugin de Depuración Rigurosa, Testing e Higiene de Código

> El tercer componente de la **Trilogía de los Guardianes** (`doc-guardian`, `docker-guardian`, `debug-guardian`). Garantiza que los modelos y agentes de IA investiguen la causa raíz de los fallos, apliquen desarrollo guiado por pruebas (TDD), prevengan regresiones y entreguen código limpio sin residuos de depuración (`console.log`, `print`, `breakpoint`).

---

## 🎯 ¿Qué problema resuelve?

Los modelos de lenguaje asistiendo en código suelen cometer 4 fallos sistemáticos al depurar:
1. **Parches superficiales**: Ponen `if (!x) return;`, `as any` o silenciadores de excepciones en lugar de solucionar el flujo de datos defectuoso.
2. **Falta de verificación real**: Declaran que el problema está "arreglado" sin haber escrito un test que reproduzca el fallo ni ejecutado las pruebas existentes.
3. **Regresiones accidentales**: Al cambiar una función para solucionar un caso límite, rompen tres funcionalidades que ya funcionaban.
4. **Contaminación de código**: Dejan `console.log("llegó aquí")`, `print(f"DEBUG: {val}")`, `debugger;` o bloques enteros de código muerto comentado.

**Debug-Guardian** impone una disciplina de ingeniería de software senior: **Reproducir -> Análisis de Causa Raíz -> Corrección Estructural -> Higiene de Residuos -> Verificación de No-Regresión**.

---

## ✨ Características Principales

1. **Regla de Agente Obligatoria (`rules/AGENTS.md`)**:
   - Prohíbe silenciar excepciones o degradar tipos con `any`.
   - Exige escribir primero un test automatizado en rojo que reproduzca el defecto.
   - Exige ejecutar la suite de pruebas del proyecto y certificar código de salida 0.
   - Obliga a eliminar todo rastro de logs temporales o breakpoints antes de concluir.
2. **Metodología de Causa Raíz (RCA)**:
   - Técnica de los 5 Porqués para llegar al origen estructural del problema.
   - Catálogo de anti-patrones comunes de IA y cómo evitarlos.
3. **Patrones Idiomáticos de Testing**:
   - Ejemplos listos para usar en `pytest`, `vitest`/`jest`, `go test` y `cargo test`.
4. **Herramienta CLI Integrada (`debug_guard.py`)**:
   - Escaneo automático de residuos (`check`).
   - Limpieza automática de prints y breakpoints (`clean`).
   - Detección y ejecución automática de la suite de pruebas (`--run-tests`).
   - Inyección de directivas en proyectos (`init`).

---

## 🛠️ Uso de la Herramienta CLI

```bash
# 1. Auditar si hay residuos de debug o código modificado sin tests:
python C:/Users/Petiso/.gemini/config/plugins/debug-guardian/skills/debug-guardian/scripts/debug_guard.py check

# 2. Auditar y además ejecutar la suite de pruebas del proyecto:
python C:/Users/Petiso/.gemini/config/plugins/debug-guardian/skills/debug-guardian/scripts/debug_guard.py check --run-tests

# 3. Limpiar automáticamente console.log, prints de debug y breakpoints:
python C:/Users/Petiso/.gemini/config/plugins/debug-guardian/skills/debug-guardian/scripts/debug_guard.py clean

# 4. Inyectar directivas en AGENTS.md / GEMINI.md del proyecto:
python C:/Users/Petiso/.gemini/config/plugins/debug-guardian/skills/debug-guardian/scripts/debug_guard.py init
```

---

## 📁 Estructura del Plugin

```text
~/.gemini/config/plugins/debug-guardian/
├── plugin.json                                 # Manifiesto del plugin
├── README.md                                   # Esta documentación
├── rules/
│   └── AGENTS.md                               # Regla obligatoria para modelos y agentes de IA
└── skills/
    └── debug-guardian/
        ├── SKILL.md                            # Guía de ejecución y protocolo para agentes
        ├── references/
        │   ├── root_cause_analysis.md          # Metodología RCA y anti-patrones
        │   ├── testing_patterns.md             # Patrones de pruebas (pytest, vitest, go, rust)
        │   ├── independent_test_authorship.md  # Tests escritos por un subagente sin ver la implementacion
        │   └── debug_hygiene.md                # Checklist de higiene y limpieza de residuos
        └── scripts/
            └── debug_guard.py                  # Herramienta CLI en Python
```
