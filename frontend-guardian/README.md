# 🎨 Frontend-Guardian: Plugin de Excelencia Frontend, Accesibilidad y Resiliencia de UI

> El quinto componente de la **Suite de los Guardianes** (`doc-guardian`, `docker-guardian`, `debug-guardian`, `architect-guardian`, `frontend-guardian`). Complementa el motor de diseño de `impeccable` aplicando estándares rigurosos de accesibilidad (a11y/WCAG 2.2 AA), diseño por tokens, microinteracciones con física natural, la regla de los 5 estados de UI y Core Web Vitals (cero CLS).

---

## 🎯 ¿Qué problema resuelve?

Los modelos de lenguaje asistiendo en desarrollo frontend suelen introducir defectos invisibles a simple vista:
1. **Falta de semántica y accesibilidad**: Crean botones con `<div onClick>` y formularios sin etiquetas `<label>`, arruinando la navegación por teclado y para lectores de pantalla.
2. **Píxeles mágicos y falta de escala**: Usan márgenes y paddings arbitrarios (`margin: 17px`) que rompen la coherencia visual del layout.
3. **Animaciones mecánicas o agresivas**: Implementan transiciones lineales sin física natural y olvidan `@media (prefers-reduced-motion)`.
4. **Interfaces frágiles de un solo estado**: Asumen el "camino feliz" e ignoran los estados de carga, vacío, error o datos parciales.
5. **Cumulative Layout Shift (CLS)**: Insartan imágenes o videos sin dimensiones, haciendo que la pantalla salte al cargar.

**Frontend-Guardian** garantiza que todo código de interfaz sea **accesible, armónico, fluido y resiliente**.

---

## ✨ Características Principales

1. **Regla Obligatoria en `rules/AGENTS.md`**:
   - Elementos interactivos nativos obligatorios (`<button>`, `<a>`).
   - Foco visible garantizado con `:focus-visible` (prohibido `outline: none` huérfano).
   - Escala modular de espaciado en múltiplos de 4px / 8px y tipografía fluida con `clamp()`.
   - Soporte para `@media (prefers-reduced-motion: reduce)`.
   - La regla de los 5 estados para componentes asíncronos.
2. **Referencias Técnicas Exhaustivas (`references/`)**:
   - `accessibility_a11y.md`: Directivas WCAG 2.2 AA, roles ARIA y formularios.
   - `design_tokens_and_fluid_css.md`: Tokens semánticos, escala modular y fluid typography.
   - `motion_and_microinteractions.md`: Curvas bezier naturales y física de resortes.
   - `form_and_state_ux.md`: La regla de los 5 estados y validación no invasiva.
   - `core_web_vitals_performance.md`: Cero CLS, aspect-ratio y optimización de fuentes.
3. **Herramienta CLI Integrada (`frontend_guard.py`)**:
   - Audita automáticamente antipatrones interactivos (`div/span onClick`).
   - Verifica foco visible, atributos `alt` y dimensiones en imágenes (CLS).
   - Detecta espaciados con píxeles arbitrarios sueltos.

---

## 🛠️ Uso de la Herramienta CLI

```bash
# 1. Auditar componentes modificados en el diff actual de Git:
python C:/Users/Petiso/.gemini/config/plugins/frontend-guardian/skills/frontend-guardian/scripts/frontend_guard.py .

# 2. Auditar todos los archivos frontend del proyecto:
python C:/Users/Petiso/.gemini/config/plugins/frontend-guardian/skills/frontend-guardian/scripts/frontend_guard.py . --all-files
```

---

## 📁 Estructura del Plugin

```text
~/.gemini/config/plugins/frontend-guardian/
├── plugin.json
├── README.md
├── rules/
│   └── AGENTS.md
└── skills/
    └── frontend-guardian/
        ├── SKILL.md
        ├── references/
        │   ├── accessibility_a11y.md
        │   ├── design_tokens_and_fluid_css.md
        │   ├── motion_and_microinteractions.md
        │   ├── form_and_state_ux.md
        │   └── core_web_vitals_performance.md
        └── scripts/
            └── frontend_guard.py
```
