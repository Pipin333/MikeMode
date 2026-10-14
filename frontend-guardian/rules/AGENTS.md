# Regla de Excelencia Frontend, Accesibilidad, Diseño por Tokens y Resiliencia de UI (Frontend-Guardian)

## Mandato Obligatorio para Agentes y Modelos de IA
Cada vez que crees, modifiques, rediseñes o refactorices interfaces de usuario, componentes frontend (React, Vue, Svelte, Angular, Astro, HTML/CSS nativo) o páginas web, **es obligatorio cumplir con los cuatro mandatos de Frontend-Guardian antes de concluir tu respuesta**:

1. **Semántica HTML5 y Accesibilidad Radical (a11y / WCAG 2.2 AA)**:
   - **Elementos Nativos Obligatorios**: Prohibido usar `<div onClick>` o `<span onClick>` para elementos interactivos. Usa siempre `<button type="button">`, `<button type="submit">` o `<a href="...">` con enlaces válidos.
   - **Asociación de Formularios**: Todo elemento `<input>`, `<select>` y `<textarea>` debe tener un `<label for="id">` explícito o estar envuelto directamente en un `<label>`, o disponer de `aria-label` / `aria-labelledby` justificado.
   - **Foco Visible Garantizado**: Prohibido el uso de `outline: none` o `outline: 0` sin proveer inmediatamente un reemplazo perceptible mediante `:focus-visible` (ej. `focus-visible:ring-2 focus-visible:ring-offset-2`).
   - **Navegación por Teclado**: Todo componente personalizado (modales, menús desplegables, accordions) debe ser operable con `Tab`, `Shift+Tab`, `Escape`, `Enter` y flechas direccionales.
   - **Ratios de Contraste**: Cumplir mínimo 4.5:1 para texto normal y 3:1 para texto grande/componentes interactivos.

2. **Tokens de Diseño, Escala Modular y Tipografía Fluida**:
   - **Cero Valores Mágicos Arbitrarios**: Prohibido inventar píxeles arbitrarios sueltos (`margin: 17px`, `padding: 23px`, `gap: 19px`). Todo espaciado debe regirse por la escala modular geométrica de 4px / 8px (4, 8, 12, 16, 24, 32, 48, 64px) o variables semánticas del design system.
   - **Tipografía Fluida**: Implementa escalas tipográficas responsivas basadas en `rem` y funciones `clamp()` (ej. `clamp(1rem, 0.9rem + 0.5vw, 1.35rem)`), evitando el uso de docenas de media queries rígidos.
   - **Tokens Semánticos de Color**: Separa la intención del color (`surface`, `surface-raised`, `on-surface`, `border-subtle`, `primary`, `destructive`) permitiendo soporte limpio para modo claro y oscuro sin parpadeos (*FOUC*).

3. **Motion Natural y Micro-interacciones Responsables**:
   - **Prohibidas Transiciones Lineales**: Prohibido el uso de `transition: all 0.3s linear`. Utiliza física de resortes (*spring physics*) o curvas de aceleración naturales (`cubic-bezier(0.16, 1, 0.3, 1)` o configuraciones `stiffness: 300, damping: 25`).
   - **Respeto a Preferencias de Movimiento**: Obligatorio contemplar usuarios con sensibilidad vestibular:
     ```css
     @media (prefers-reduced-motion: reduce) {
       *, *::before, *::after {
         animation-duration: 0.01ms !important;
         animation-iteration-count: 1 !important;
         transition-duration: 0.01ms !important;
         scroll-behavior: auto !important;
       }
     }
     ```
   - **Feedback Inmediato**: Todo botón o enlace debe proporcionar estados visibles de `:hover`, `:active` y estado deshabilitado.

4. **Resiliencia de UI (Los 5 Estados) y Core Web Vitals (CLS = 0)**:
   - **La Regla de los 5 Estados**: Todo componente que cargue o transforme datos asíncronos debe implementar explícitamente sus 5 estados:
     1. *Vacío (Empty State)*: Mensaje claro con llamada a la acción.
     2. *Carga (Skeleton Screens / Shimmer)*: Marcadores de posición que reserven el espacio exacto.
     3. *Éxito / Datos Listos*: La vista completa renderizada.
     4. *Error Reintentable*: Explicación comprensible para el usuario humano y botón para reintentar.
     5. *Parcial o Deshabilitado*: Indicación visual de indisponibilidad.
   - **Cero Layout Shift (CLS = 0)**: Todo elemento `<img>`, `<video>` o iframe debe tener atributos `width` y `height` explícitos, o la propiedad CSS `aspect-ratio` para evitar saltos de pantalla durante la carga.

5. **Paridad Visual en Refactorizaciones UI (*Visual Parity*)**:
   - Al refactorizar componentes existentes, migrar CSS clásico a Tailwind, o reestructurar vistas (ej. en React o HTML/JS), es obligatorio garantizar la **equivalencia visual exacta píxel a píxel**.
   - Prohibido alterar espaciados, proporciones, alineaciones o jerarquía tipográfica bajo el pretexto de una "limpieza de código", salvo petición expresa del usuario.
   - Verifica el comportamiento responsivo en los viewports móvil (375px) y escritorio (1440px) para evitar saltos y scroll horizontal involuntario.

---

## Protocolo de Reporte Final
En tu respuesta final al usuario, incluye siempre el bloque explícito:

```markdown
### 🎨 Diseño y Frontend (Frontend-Guardian)
- **Semántica & a11y**: [HTML5 semántico / Roles ARIA / Foco visible / Contraste verificado].
- **Tokens & Espaciado**: [Escala 4/8px respetada / Tipografía fluida con clamp / Sin px arbitrarios].
- **Motion & Resiliencia**: [Curvas naturales con prefers-reduced-motion / Los 5 estados de UI cubiertos].
- **Core Web Vitals**: [Cero CLS / Dimensiones en medios / Carga optimizada].
```
