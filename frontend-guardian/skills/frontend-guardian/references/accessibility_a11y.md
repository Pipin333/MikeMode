# Guía de Accesibilidad Web (a11y) y WCAG 2.2 AA

Buenas prácticas y estándares de accesibilidad obligatorios para el desarrollo de interfaces inclusivas.

---

## 1. Semántica HTML5 Nativa vs. ARIA

La primera regla de ARIA (según W3C):
> *"Si puedes usar un elemento HTML nativo con la semántica y comportamiento que necesitas, ya integrado, entonces hazlo en lugar de repurposar un elemento y añadirle ARIA."*

### Comparativa:
```html
<!-- ❌ Antipatrón de IA -->
<div class="button" onclick="handleSubmit()">Enviar</div>

<!-- ✅ Correcto y accesible -->
<button type="submit" class="btn btn-primary">Enviar</button>
```

---

## 2. Formularios y Etiquetas

Todo control de formulario debe estar inequívocamente etiquetado:

```html
<!-- Opción 1: for con id (Estándar de Oro) -->
<label for="user-email">Correo Electrónico</label>
<input type="email" id="user-email" name="email" required autocomplete="email">

<!-- Opción 2: Wrapping explícito -->
<label>
  <span>Contraseña</span>
  <input type="password" name="password" required>
</label>
```

---

## 3. Manejo de Foco y Anillos Visibles

Nunca anules el foco por razones puramente estéticas sin dar una alternativa visible:

```css
/* ❌ Prohibido: deja a usuarios de teclado ciegos */
button:focus {
  outline: none;
}

/* ✅ Correcto: foco distintivo y de alto contraste */
button:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

---

## 4. Diálogos Modales y Regiones Vivas (ARIA Live)

Para notificaciones dinámicas (toasts, alertas de error):
```html
<div role="status" aria-live="polite" class="toast">
  Cambios guardados con éxito.
</div>

<div role="alert" aria-live="assertive" class="error-banner">
  Fallo en la conexión. Por favor reintente.
</div>
```
