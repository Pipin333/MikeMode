# Paridad Visual en Refactorizaciones UI (Visual Parity)

Metodología para refactorizar código de interfaz (CSS clásico a Tailwind, vanilla JS a React, o reestructuración de componentes) garantizando equivalencia visual exacta.

---

## 1. El Riesgo de la Refactorización Frontend

Cuando se refactoriza código de interfaz, un cambio que preserva la funcionalidad lógica puede degradar inadvertidamente el diseño visual:
- Reducir el padding de un botón en móviles.
- Provocar que un titular largo se desborde o se solape.
- Introducir un scroll horizontal inesperado en viewports estrechos (375px).
- Alterar la jerarquía de colores en modo oscuro.

---

## 2. Protocolo de Verificación de Paridad

1. **Captura del Estado Original (*Baseline*)**:
   - Inspecciona o captura visualmente los elementos clave antes de iniciar la migración: dimensiones calculadas (`offsetWidth`, `offsetHeight`), margenes computados y estructura visual.
2. **Preservación de Proporciones y Escala**:
   - Si un botón medía 44px de alto para cumplir accesibilidad táctil, la nueva versión con Tailwind o CSS modules debe medir exactamente 44px (`h-11`).
3. **Auditoría Multi-Viewport**:
   - Verifica la vista resultante en al menos dos tamaños críticos:
     - **Móvil estrecho (375px)**: Asegurar que `document.body.scrollWidth === window.innerWidth`.
     - **Escritorio amplio (1440px)**: Asegurar que el contenido no se estire de forma desproporcionada (`max-width` en contenedores principales).
