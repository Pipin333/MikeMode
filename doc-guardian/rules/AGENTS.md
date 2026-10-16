# Regla de Integridad de Documentación, Calidad de Código y Estándares (Doc-Guardian)

## Mandato Obligatorio para Agentes y Modelos de IA
Cada vez que realices cambios, adiciones o refactorizaciones en el código fuente de cualquier proyecto, **es obligatorio cumplir con dos mandatos antes de concluir tu respuesta**:
1. **Documentación Externa Continua**: Verificar y actualizar la documentación técnica del proyecto (principalmente el `README.md`, `.env.example` y archivos en `docs/`).
2. **Estándares de Código y Documentación Interna (PEP 8, PEP 257 o Equivalentes)**: Todo código nuevo o modificado debe cumplir rigurosamente con estándares idiomáticos de formato y convenciones de docstrings/comentarios técnicos según el lenguaje del proyecto.

No se considera completada ninguna tarea de código si las instrucciones de instalación, configuración, uso o arquitectura han quedado desactualizadas con respecto a la implementación real, o si el código introducido incumple los estándares de estilo y documentación interna.

---

## 1. Mandato de Estándares de Código y Docstrings (PEP 8, PEP 257 o Equivalentes)
El agente debe garantizar que el código escrito sea limpio, consistente y autodocumentado:

- **Ecosistema Python**:
  - **PEP 8 (Guía de Estilo de Código)**:
    - Nomenclatura obligatoria: `snake_case` para funciones y variables, `PascalCase` para clases, `UPPER_SNAKE_CASE` para constantes.
    - Tipado estático con anotaciones (`type hints`) en argumentos y valores de retorno.
    - Longitud de línea legible (máximo 88-100 caracteres).
    - Organización limpia de imports: estándar primero, terceros después, locales al final.
    - Espaciado consistente (4 espacios por sangría, sin tabulaciones mezcladas).
  - **PEP 257 (Convenciones de Docstrings)**:
    - **Docstrings obligatorios** con triples comillas `"""..."""` en todo módulo, clase, método y función pública.
    - Resumen conciso de una línea en modo imperativo (ej. `"""Calcula el hash SHA-256 del contenido."""`).
    - Desglose detallado de argumentos (`Args:` / `Parameters:`), valores de retorno (`Returns:`) y excepciones (`Raises:`) siguiendo formato Google, NumPy o Sphinx.

- **Ecosistemas Equivalentes (JavaScript, TypeScript, Rust, Go, Java, C#)**:
  - **TypeScript / JavaScript**:
    - Formato estándar Prettier/ESLint, indentación de 2 espacios, `camelCase` para variables/funciones, `PascalCase` para componentes/clases.
    - **TSDoc / JSDoc obligatorio** (`/** ... */`) en todas las funciones, métodos e interfaces exportadas, documentando parámetros (`@param`), tipo de retorno (`@returns`) y casos de error (`@throws`).
  - **Rust**:
    - Formato estricto según `rustfmt`.
    - **Rustdoc obligatorio** con `///` en todos los ítems públicos y `//!` a nivel de módulo/crate.
  - **Go**:
    - Formateado con `gofmt` y convenciones de *Effective Go*.
    - **GoDoc obligatorio**: Comentario previo a cada identificador exportado comenzando con su nombre (ej. `// NewServer creates a new HTTP server instance.`).
  - **Java / C#**:
    - Google Java Style / C# Conventions.
    - **Javadoc / XML Comments (`/// <summary>`) obligatorios** en clases y métodos públicos.

---

## 2. Disparadores Automáticos de Documentación Técnica
Revisa y actualiza el `README.md` si has modificado:
- **Dependencias**: Se instalaron, actualizaron o eliminaron paquetes en `package.json`, `pyproject.toml`, `requirements.txt`, `Cargo.toml`, `go.mod`, etc.
- **Variables de Entorno**: Se agregaron o cambiaron claves como `process.env.VAR`, `os.getenv('VAR')`, etc. Actualiza tanto el `README.md` como el archivo `.env.example`.
- **Scripts y Comandos**: Se agregaron nuevos scripts en `package.json`, comandos de build, tests, migraciones o flags de CLI.
- **Endpoints o APIs**: Se añadieron rutas HTTP/REST, queries GraphQL, eventos WebSocket o contratos de datos.
- **Estructura, Monorepos o Nuevos Plugins/Módulos**: Se añadieron nuevos módulos, plugins, skills, paquetes o carpetas de primer nivel. **En monorepos o suites de plugins, crear un `README.md` dentro de la subcarpeta NO exime de actualizar el `README.md` raíz del repositorio** para registrar el nuevo módulo en la tabla o índice general.
- **Requisitos Previos**: Se cambió la versión mínima de Node.js, Python, base de datos o herramientas externas (Docker, Redis, etc.).

---

## 3. Protocolo de Ejecución al Finalizar Cambios de Código
Antes de marcar tu tarea como finalizada o entregar el mensaje al usuario:
1. **Audita tus propios cambios**: Examina qué archivos tocaste y valida que el código cumpla con PEP 8 / PEP 257 o equivalentes (docstrings completos, tipos explícitos y formato limpio).
2. **Revisa tanto el `README.md` del módulo como el `README.md` raíz**:
   - Si no existe `README.md` en la raíz, créalo utilizando la estructura estándar (descripción, requisitos, instalación, variables de entorno, uso, scripts).
   - Si trabajas en un monorepo o repositorio de plugins/skills, actualiza el `README.md` del subpaquete **y obligatoriamente también el índice del `README.md` raíz**.
3. **Sincroniza `.env.example`**: Asegúrate de que toda variable requerida en código tenga su contraparte documentada en `.env.example` con un valor de ejemplo o descripción.
4. **Comunica los cambios documentados y estándares**: En tu respuesta final, incluye siempre un breve resumen bajo el encabezado `### 📝 Documentación Actualizada y Estándares` indicando qué partes del README fueron ajustadas y confirmando el cumplimiento de PEP 8/257 o sus equivalentes.
