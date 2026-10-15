# Protocolo de Auto-Mutación por Fallos (Failure-Driven Mutation)

Este protocolo define cómo un agente de Antigravity evoluciona dinámicamente un skill existente tras detectar y solucionar un fallo de ejecución, garantizando que el aprendizaje persista sin corromper la integridad del código fuente.

---

## 1. El Ciclo de Auto-Inmunización

```
[Ejecución de Skill] ──> [Fallo / Gotcha Detectado] ──> [Diagnóstico y Fix Exitoso]
                                                               │
                                                               ▼
[Respaldo .bak Creado] <── [Validación de Inmunidad] <── [Captura de Causa Raíz]
          │
          ▼
[Append en ## Pitfalls] ──> [validate_skill.py] ──> [Notificación Transparente al Usuario]
```

### Disparadores del Protocolo:
- Un comando provisto por un skill falló debido a una bandera obsoleta, un formato no contemplado o una diferencia de sistema operativo (ej. Windows PowerShell vs Bash).
- Una llamada a API devolvió un código de error (ej. HTTP 400, 429) por un límite no documentado.
- El usuario corrigió explícitamente una asunción del skill durante la sesión.

---

## 2. Las 5 Salvaguardas Infranqueables de Balthasar-2

Toda mutación en caliente debe cumplir estrictamente estos 5 cerrojos de contención:

### Regla 1: Inmunidad del Núcleo (Core Blacklist)
Queda terminantemente prohibido que el motor de auto-aprendizaje modifique archivos en:
- `C:\Users\Mike\.gemini\antigravity\builtin\skills\*` (Skills nativas del motor).
- `C:\Users\Mike\.gemini\config\plugins\*-guardian\*` (Plugins de gobernanza y auditoría).
- Archivos fuera del directorio de plugins o skills de usuario.

### Regla 2: Inmutabilidad del Prompt Base (Solo-Append)
- **Prohibido reescribir**: El agente jamás debe alterar el título, la descripción, el prompt de sistema ni las instrucciones primarias de un skill funcional.
- **Zona exclusiva de mutación**: Las mutaciones solo pueden añadirse al final de la sección `## Pitfalls` en forma de viñeta estructurada:
  ```markdown
  - **[Fecha / Contexto]**: [Descripción concisa del gotcha o fallo]. *Solución/Mitigación*: [El comando o parámetro exacto que resuelve el problema].
  ```

### Regla 3: Deduplicación Semántica
Antes de insertar un nuevo pitfall, el agente debe inspeccionar los existentes. Si el gotcha ya está cubierto conceptualmente, no debe duplicarse. El contenido añadido debe aportar información nueva y accionable.

### Regla 4: Respaldo Automático Previo (`.bak`)
Antes de modificar cualquier archivo `SKILL.md` existente en disco:
1. Crear una copia de seguridad idéntica nombrada `SKILL.md.bak`.
2. Aplicar la edición quirúrgica mediante la herramienta de reemplazo de contenido.
3. Si la verificación estática falla, restaurar inmediatamente desde `.bak`.

### Regla 5: Transparencia Activa hacia el Usuario
El agente **nunca debe mutar un skill en silencio**. Tras registrar el aprendizaje, debe emitir una notificación limpia en el chat:
```markdown
🧬 **Auto-aprendizaje (Failure-Driven Mutation)**:
- Skill actualizada: `[nombre-del-skill]`
- Gotcha catalogado: *"[Explicación en una frase del error y su solución]"*
- Respaldo de seguridad creado: `SKILL.md.bak`
```
