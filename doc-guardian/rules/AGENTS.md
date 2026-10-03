# Regla de Integridad de Documentación y Sincronización Continua (Doc-Guardian)

## Mandato Obligatorio para Agentes y Modelos de IA
Cada vez que realices cambios, adiciones o refactorizaciones en el código fuente de cualquier proyecto, **es obligatorio verificar y actualizar la documentación técnica del proyecto (principalmente el `README.md` y archivos en `docs/`) antes de concluir tu respuesta**.

No se considera completada ninguna tarea de código si las instrucciones de instalación, configuración, uso o arquitectura han quedado desactualizadas con respecto a la implementación real.

---

## 1. Disparadores Automáticos (Cuándo es OBLIGATORIO actualizar la documentación)
Revisa y actualiza el `README.md` si has modificado:
- **Dependencias**: Se instalaron, actualizaron o eliminaron paquetes en `package.json`, `pyproject.toml`, `requirements.txt`, `Cargo.toml`, `go.mod`, etc.
- **Variables de Entorno**: Se agregaron o cambiaron claves como `process.env.VAR`, `os.getenv('VAR')`, etc. Actualiza tanto el `README.md` como el archivo `.env.example`.
- **Scripts y Comandos**: Se agregaron nuevos scripts en `package.json`, comandos de build, tests, migraciones o flags de CLI.
- **Endpoints o APIs**: Se añadieron rutas HTTP/REST, queries GraphQL, eventos WebSocket o contratos de datos.
- **Estructura o Arquitectura**: Se añadieron nuevos módulos, carpetas principales o cambió el flujo de ejecución.
- **Requisitos Previos**: Se cambió la versión mínima de Node.js, Python, base de datos o herramientas externas (Docker, Redis, etc.).

---

## 2. Protocolo de Ejecución al Finalizar Cambios de Código
Antes de marcar tu tarea como finalizada o entregar el mensaje al usuario:
1. **Audita tus propios cambios**: Examina qué archivos tocaste y qué comportamiento nuevo o modificado existe.
2. **Revisa el `README.md` existente**:
   - Si no existe `README.md`, créalo utilizando la estructura estándar (descripción, requisitos, instalación, variables de entorno, uso, scripts).
   - Si existe, localiza las secciones afectadas y actualízalas con precisión milimétrica sin borrar notas existentes del usuario.
3. **Sincroniza `.env.example`**: Asegúrate de que toda variable requerida en código tenga su contraparte documentada en `.env.example` con un valor de ejemplo o descripción.
4. **Comunica los cambios documentados**: En tu respuesta final, incluye siempre un breve resumen bajo el encabezado `### 📝 Documentación Actualizada` indicando qué partes del README o guías fueron ajustadas.
