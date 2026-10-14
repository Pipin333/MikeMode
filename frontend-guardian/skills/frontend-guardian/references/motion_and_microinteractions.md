# Motion, Microinteracciones y Física de Animación

Principios de animación de interfaz de alto impacto y respeto al usuario.

---

## 1. Por qué Descartar Animaciones Lineales

Las animaciones lineales (`transition: all 0.3s linear` o `ease`) no existen en el mundo físico real. Todo objeto físico acelera y desacelera orgánicamente.

### Curvas de Salida Suave (Ease-Out Exponencial)
Ideal para elementos que entran a pantalla o modales que se abren:
```css
/* Entradas enérgicas pero amortiguadas */
transition: transform 300ms cubic-bezier(0.16, 1, 0.3, 1), opacity 200ms ease;
```

---

## 2. Física de Resortes (*Spring Physics*)

En librerías modernas como `framer-motion`:
```tsx
<motion.div
  initial={{ scale: 0.95, opacity: 0 }}
  animate={{ scale: 1, opacity: 1 }}
  transition={{
    type: "spring",
    stiffness: 350,
    damping: 25,
    mass: 0.8
  }}
/>
```

---

## 3. Respeto Obligatorio a `prefers-reduced-motion`

Siempre incluye la anulación para usuarios sensibles al movimiento:

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
