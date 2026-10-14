# Anti-Slop, No-Comments y Código Auto-Explicativo

Principios para erradicar el código inflado, los comentarios redundantes y el ruido cognitivo generado por modelos de IA.

---

## 1. El Fenómeno del "AI Slop"

Los modelos de lenguaje tienden a generar código con dos vicios principales:
1. **Comentarios Obvios y Patronizantes**:
   ```python
   # ❌ AI SLOP: Explica lo que el código ya dice a gritos
   # Iteramos sobre la lista de usuarios
   for user in users:
       # Comprobamos si el usuario está activo
       if user.is_active:
           # Enviamos la notificación
           send_notification(user)
   ```
2. **Exceso de Capas Indireccionales**: Creación de funciones de 1 línea que solo delegan a otra función de 1 línea sin transformar datos ni asegurar invariantes.

---

## 2. La Regla de Oro de los Comentarios

> **"Un comentario solo es legítimo si documenta el POR QUÉ de una decisión contraintuitiva, un invariante de negocio no evidente, una anomalía de hardware/red o un workaround debido a un bug de una librería externa. Si explica el CÓMO, debe ser reemplazado por un mejor nombre de variable o función."**

### Ejemplo de Comentario Legítimo:
```python
# ✅ Legítimo: Documenta una restricción no obvia del entorno/librería
# Usamos un delay explícito de 50ms antes de emitir el frame de audio
# para evitar que el buffer de FFmpeg sufra subdesbordamiento en Linux.
time.sleep(0.05)
```

### Ejemplo de Código Auto-Explicativo (Sin Comentarios):
```python
# ✅ El código habla por sí mismo gracias a nombres de dominio precisos
active_users = [user for user in users if user.has_valid_subscription()]
dispatch_renewal_notices(active_users)
```
