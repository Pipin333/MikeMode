# Regla de Excelencia Frontend, Accesibilidad, Diseño por Tokens y Resiliencia de UI (Frontend-Guardian)

## Mandato Obligatorio para Agentes y Modelos de IA
Cada vez que crees, modifiques, rediseñes o refactorices interfaces de usuario, componentes frontend (React, Vue, Svelte, Angular, Astro, HTML/CSS nativo) o páginas web, **es obligatorio cumplir con los cuatro mandatos de Frontend-Guardian antes de concluir tu respuesta**:

1. **Semántica HTML5 y Accesibilidad Radical (a11y / WCAG 2.2 AA)**:
   - **Elementos Nativos Obligatorios**: Prohibido usar `<div onClick>` o `<span onClick>` para elementos interactivos. Usa siempre `<button type="button">`, `<button type="submit">` o `<a href="...">` con enlaces válidos.
   - **Asociación de Formularios**: Todo elemento `<input>`, `<select>` y `<textarea>` debe tener un `<label for="id">` explícito o estar envuelto directamente en un `<label>`, o disponer de `aria-label` / `aria-labelledby` justificado.
   - **Foco Visible Garantizado**: Prohibido el uso de `outline: none` o `outline: 0` sin proveer inmediatamente un reemplazo perceptible mediante `:focus-visible` (ej. `focus-visible:ring-2 focus-visible:ring-offset-2`).
   - **Navegación por Teclado**: Todo componente personalizado (modales, menús desplegables, accordions) debe ser operable con `Tab`, `Shift+Tab`, `Escape`, `Enter` y flechas direccionales.
   - **Ratios de Contraste (Especial Modo Oscuro y Footers)**: Cumplir mínimo 4.5:1 para texto normal y 3:1 para texto grande/componentes interactivos. En fondos oscuros profundos (`#060911`–`#0F1420`), está prohibido usar `text-slate-500` o más oscuros para textos de lectura, metadatos o *footers*; utiliza como mínimo `text-slate-400` (`#94A3B8`) para evitar fallos en auditorías Lighthouse/PageSpeed.

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

6. **Iconografía Vectorial Canónica y Resiliencia de Navegación (`Navbar` / `Header`)**:
   - **Cero Emojis ni `<path>` SVG Manuales en UI Técnica**: Evita usar emojis del sistema como iconografía de interfaz y jamás pegues cadenas `<path d="...">` manuales no verificadas que puedan contener artefactos de trazado. Utiliza librerías vectoriales canónicas (`bootstrap-icons`, `lucide`, `heroicons`) renderizadas como SVG inline en **build-time** (cero hojas de estilo/fuentes externas bloqueantes en runtime).
   - **Barras de Navegación Sin Quiebres de Línea (`Anti-Wrapping`)**: Todo enlace, *badge* y botón CTA dentro de un `<header>` o `<nav>` horizontal debe incluir `whitespace-nowrap` y `flex-shrink-0` para impedir que textos como *"Sobre mí"* o *"Iniciar contacto"* se partan en dos líneas en pantallas medianas (`768px`–`1200px`). Los subtítulos largos junto al logo deben ocultarse hasta breakpoints amplios (`hidden xl:inline-flex`).
   - **Cero Rutas Duplicadas en el Mismo Viewport**: Prohibido repetir el mismo destino simultáneamente como enlace de texto en `<nav>` y como botón CTA en la misma barra de escritorio.

7. **Theming Dial: Identidad Local por Dominio sobre Chasis Inmutable (Lab & Micro-Apps)**:
   - **Universo Temático por Dominio**: Al diseñar módulos de experimentación, playgrounds o micro-aplicaciones (`/lab/*`), identifica el elemento característico esencial de su dominio técnico (ej. audio vintage y pantallas VFD de sobremesa; tratados ontológicos, fortalezas y mística medieval; calculadoras logísticas) e itera visualmente sobre él.
   - **Invariante del Chasis Padre**: La ambientación temática NUNCA debe desbordar ni degradar el sistema de diseño padre (fondo oscuro profundo `#030712`, tipografía técnica Sans/Mono, WCAG AA, sin emojis del sistema ni cliparts sólidos pesados).
   - **Técnica de Ejecución Periférica**:
     1. *Auras y Luces Radiales*: Resplandores difusos con la paleta del dominio (púrpura real/oro viejo, cian/ámbar fluorescente VFD).
     2. *Trazos Técnicos de Precisión (1px Stroke)*: Planos esquemáticos, diagramas de bloques, vúmetros o grabados vectoriales en línea fina de 1px, evitando figuras infantiles.
     3. *Ubicación Periférica*: Los elementos temáticos se disponen en el fondo ambiental y en los márgenes del viewport, preservando el núcleo central de interacción 100% limpio y sin fricción de lectura.

---

## Protocolo de Ejecución Silenciosa y Reporte Bajo Demanda (`/report`)
- **Por defecto (Ejecución Silenciosa)**: Cumple todos los mandatos de accesibilidad, tokens, motion, 5 estados, CLS=0 y paridad visual directamente en el código **SIN imprimir el bloque de reporte al final de tu respuesta**.
- **Bajo Demanda (`/report`)**: Únicamente cuando el usuario escriba `/report` o solicite explícitamente un reporte de auditoría de los guardianes, incluye el bloque:

```markdown
### 🎨 Diseño y Frontend (Frontend-Guardian)
- **Semántica & a11y**: [HTML5 semántico / Roles ARIA / Foco visible / Contraste verificado].
- **Tokens & Espaciado**: [Escala 4/8px respetada / Tipografía fluida con clamp / Sin px arbitrarios].
- **Motion & Resiliencia**: [Curvas naturales con prefers-reduced-motion / Los 5 estados de UI cubiertos].
- **Core Web Vitals**: [Cero CLS / Dimensiones en medios / Carga optimizada].
```
