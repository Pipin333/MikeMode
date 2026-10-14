# Tokens de Diseño, Escala Modular y CSS Fluido

Fundamentos de diseño visual sistemático para erradicar píxeles mágicos y lograr layouts armónicos y escalables.

---

## 1. La Escala de Espaciado Modular (Base 4px / 8px)

No inventes márgenes ni paddings aleatorios. Apégate estrictamente a la progresión:

| Token / Clase | Valor en px | Equivalente rem | Uso Típico |
| :--- | :--- | :--- | :--- |
| `space-1` | 4px | 0.25rem | Espaciado mínimo interno, badges, borders |
| `space-2` | 8px | 0.5rem | Padding botones pequeños, gaps de tags |
| `space-3` | 12px | 0.75rem | Separación compacta de inputs y etiquetas |
| `space-4` | 16px | 1.0rem | Padding base de tarjetas, gap estándar |
| `space-6` | 24px | 1.5rem | Separación entre secciones en móviles |
| `space-8` | 32px | 2.0rem | Padding de modales y contenedores |
| `space-12` | 48px | 3.0rem | Separación de bloques en escritorio |
| `space-16` | 64px | 4.0rem | Espaciado hero / separadores mayores |

---

## 2. Tipografía Fluida con `clamp()`

Evita escribir 5 media queries para cambiar el tamaño de un titular:

```css
:root {
  /* Escala fluida entre 360px y 1280px de viewport */
  --font-size-sm: clamp(0.8rem, 0.75rem + 0.2vw, 0.875rem);
  --font-size-base: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
  --font-size-lg: clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem);
  --font-size-xl: clamp(1.5rem, 1.35rem + 0.75vw, 2.0rem);
  --font-size-hero: clamp(2.25rem, 1.8rem + 2vw, 3.75rem);
}
```

---

## 3. Paletas de Colores Semánticos (Dark/Light Native)

Define tokens basados en su función en la interfaz, nunca en su valor cromático literal (`--blue-500` -> `--color-primary`):

```css
:root {
  --color-surface-bg: #ffffff;
  --color-surface-card: #f8fafc;
  --color-text-main: #0f172a;
  --color-text-muted: #64748b;
  --color-border: #e2e8f0;
  --color-primary: #2563eb;
  --color-destructive: #dc2626;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-surface-bg: #0b0f19;
    --color-surface-card: #151d2f;
    --color-text-main: #f8fafc;
    --color-text-muted: #94a3b8;
    --color-border: #1e293b;
    --color-primary: #3b82f6;
    --color-destructive: #ef4444;
  }
}
```
