# Core Web Vitals y Rendimiento Frontend Extremo

Buenas prácticas de ingeniería para garantizar tiempos de carga instantáneos y cero saltos de maquetación (*Zero CLS*).

---

## 1. Cumulative Layout Shift (CLS = 0)

El CLS mide cuánto se mueven inesperadamente los elementos en pantalla mientras la página carga.

### Causas y Soluciones:
1. **Imágenes sin dimensiones**:
   ```html
   <!-- ❌ Provoca CLS severo -->
   <img src="banner.jpg" alt="Banner">

   <!-- ✅ Cero CLS: Reserva el espacio de antemano -->
   <img src="banner.jpg" alt="Banner" width="800" height="400" loading="lazy">
   ```
2. **Propiedad CSS `aspect-ratio`**:
   ```css
   .video-container {
     width: 100%;
     aspect-ratio: 16 / 9;
   }
   ```

---

## 2. Optimización de Fuentes (FOIT / FOUT)

Evita textos invisibles mientras carga la tipografía web:

```css
@font-face {
  font-family: 'Inter';
  src: url('/fonts/Inter-Variable.woff2') format('woff2');
  font-display: swap; /* Muestra fuente fallback inmediatamente y luego reemplaza */
  font-weight: 100 900;
}
```

---

## 3. Renderizado Diferido (`content-visibility`)

Para páginas con listas muy largas o blogs extensos:

```css
.card-list-item {
  content-visibility: auto;
  contain-intrinsic-size: 0 320px; /* Estima la altura del bloque antes de ser visible */
}
```
Esto le indica al motor del navegador que no renderice el layout ni pinte los elementos que están fuera del viewport hasta que el usuario se acerque a ellos con el scroll.
