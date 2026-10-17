# Foreman: Web Build Playbook for Coding Agents

**Foreman** (creado por *Turki Alshuaibi*, v2.2.0, licencia MIT) es un *playbook* procedimental que convierte a tu agente de IA en el **Capataz de Obra** de la construcción de un sitio web, portfolio, landing page o documentación.

> *"Los agentes de código eliminaron el costo de escribir una web, pero no el costo de decidir qué debería ser."*

Foreman es **100% Markdown puro (cero scripts ejecutables)**. No requiere dependencias, no compila y no ejecuta código en segundo plano. Su mecanismo es un conjunto estricto de compuertas (*gates*) y directivas que obligan a tomar las decisiones clave antes de tocar una sola línea de código.

---

## 🧭 Las 8 Compuertas Secuenciales (*Gates*)

1. **`1. Orient`**: Diagnostica qué se va a construir y qué activos reales existen (textos, logos, fotos, testimonios verídicos). Prohibido inventar datos si faltan.
2. **`2. Decide`**: Define un único lector prioritario, una única acción clave tras 90 segundos, el trabajo nuclear de la página y una lista explícita de lo que **NO** se va a construir (*non-goals*).
3. **`3. Look`**: Bloquea la dirección visual, contraste tipográfico y paleta con un arnés `brand.html` desechable antes de tocar código de producción.
4. **`4. Brief`**: Redacta y congela un documento formal `BUILD-BRIEF.md`.
5. **`5. Build`**: Construye el sitio bajo restricciones de calidad de producto (cero botones rotos, cero controles decorativos muertos).
6. **`6. Verify`**: Auditoría destructiva de affordances: verificación responsive en viewport móvil a 375px, clic en todos los controles y revisión exhaustiva contra el catálogo de *vibe-coded tells*.
7. **`7. Ship`**: Guía paso a paso para despliegue en hosting real (Cloudflare Pages, Vercel, GitHub Pages), registros DNS (`A`, `CNAME`) y SSL.
8. **`8. Index & Metadata`**: Implementación de página `404.html`, OpenGraph y Twitter Cards, `robots.txt`, `sitemap.xml` y `llms.txt`.

---

## ⚡ Las 8 Reglas Cardinales

1. **Cero código de web antes de congelar el brief**: Prohibido crear HTML, CSS, componentes o carpetas de proyecto durante los pasos 1 al 4.
2. **Un paso, una pregunta, un mensaje**: Mensajes breves (<100 palabras) con la compuerta actual (`**FOREMAN · X/8**`) para no saturar la conversación.
3. **El razonamiento se queda en el chat**: La página final no debe argumentar sus propias decisiones; el diseño debe auto-explicarse.
4. **Las compuertas se sostienen bajo presión**: Si el usuario pide *"hazlo a tu criterio y después iteramos"*, se comprime el flujo a 4 intercambios pero nunca se salta a ciegas.
5. **Cero Em Dashes (`—`)**: Prohibidos los guiones largos por ser el tell lingüístico más común de texto generado por IA.
6. **Pensar antes de responder**: Escuchar el detalle sutil del usuario en lugar de responder la respuesta promedio de un LLM.
7. **Calidad de producto, incluso en descartables**: Todo botón debe funcionar; lo que no esté implementado se elimina del DOM en vez de fingir interactividad.
8. **El dueño decide, el capataz asesora una sola vez**: Se advierte el costo de una mala decisión una vez; si el usuario la mantiene, se implementa con máxima calidad sin objeciones.

---

## 📚 Biblioteca de Referencias y Activos

Ubicados en `skills/foreman/references/` y `skills/foreman/assets/`:
- **`vibe-coded-tells.md`**: Catálogo quirúrgico de reflejos perezosos de las IAs (tarjetas dentro de tarjetas, orbes borrosos de fondo, glassmorphism innecesario, textos SaaS vacíos como *"Unlock seamless workflows"*, status dots verdes que no monitorean nada).
- **`content-interview.md`**: Protocolo periodístico para extraer decisiones del usuario sin inventar contenido ficticio.
- **`palette.md`**: Cómo diseñar paletas de color con balance y jerarquía sin caer en el índigo predeterminado (`#6366F1`).
- **`composition-and-contrast.md`**: Principios de jerarquía tipográfica y composición espacial.
- **`verify-and-ship.md`**: Checklist de pruebas destructivas y despliegue real en producción.
- **`metadata-and-404.md`**: Guía de metadatos sociales, indexación y página 404 de alta calidad.
- **`bilingual-rtl.md`**: Soporte para idiomas bidireccionales y diseño árabe/hebreo (RTL).
- **`assets/`**: Plantillas listas para `404.html`, `brand-harness.html`, `head-metadata.html`, `llms.txt`, `robots.txt` y `sitemap.xml`.

---

## 🚀 Cómo Usarlo

En cualquier sesión de chat con Antigravity, Claude Code o Gemini CLI, simplemente di:
- *"Ayúdame a construir mi portfolio"*
- *"Quiero hacer una landing page para mi proyecto"*
- *"Reconstruyamos la web de documentación"*
- *"Activa Foreman para estructurar este sitio web"*

El agente presentará la tarjeta de orientación de Foreman y comenzará la entrevista guiada.

---

## 🛡️ Salvaguardas MAGI del Ecosistema (Pacto Naoko Akagi)

Para garantizar la máxima seguridad operativa y evitar fricción innecesaria, se aplican 3 salvaguardas vinculantes durante la ejecución de Foreman:

1. **Protocolo de Derivación Rápida (*Emergency Bypass*):**
   Si el usuario declara expresamente urgencia, un prototipo de prueba o una demo interna, el agente colapsará automáticamente las compuertas 1 a 4 en un intercambio sumario y procederá a la construcción sin fricciones pedagógicas.
2. **Auditoría de Secretos Pre-Deploy (Paso 5):**
   Antes de autorizar cualquier `git push` o despliegue a hosting estático (Vercel/Cloudflare Pages), se verificará que ninguna variable sensible (`.env`, API keys) quede expuesta en el código cliente.
3. **Snapshot de Zona DNS Obligatorio (Paso 7):**
   Queda estrictamente prohibido que el agente instruya cambios o borrado de registros DNS sin solicitar primero una copia/exportación de la zona actual, con advertencia explícita sobre la intangibilidad de los registros de correo (`MX`, `SPF`, `DKIM`).

