---
name: hermes-auto-learner
description: Auto-distill and evolve skills in one turn from experience.
version: 1.0.0
platforms: [windows, linux, macos]
metadata:
  tags: [MetaLearning, SkillEngineering, SelfImprovement]
---

# Hermes Auto-Learner

Motor de auto-aprendizaje y destilación en 1 solo turno de skills inspirado en NousResearch Hermes Agent. Transforma automáticamente sesiones complejas, repositorios, documentación externa y soluciones a fallos en skills modulares y persistentes compatibles con el estándar `agentskills.io`.

## When to Use
- Cuando el usuario use el comando `/learn <tema, url, repo o "lo que acabamos de hacer">`.
- Cuando se resuelva una tarea compleja que haya requerido más de 5 llamadas a herramientas o debugging de APIs no documentadas (activación del *Post-Task Self-Nudge*).
- Cuando un comando de una skill existente falle durante la sesión y se descubra la solución técnica, activando la auto-mutación por fallos (*Failure-Driven Mutation*).

## Prerequisites
- Entorno de ejecución con Python 3 instalado para correr el script validador (`python scripts/validate_skill.py`).
- Permisos de escritura en el directorio de plugins o skills locales del usuario.
- Salvaguarda activa: el núcleo del sistema (`builtin/skills/*`) y los plugins guardianes (`*-guardian`) son estrictamente de solo lectura.

## How to Run
Invocar mediante comandos directos en la sesión:
- Destilación directa: `/learn [fuente o contexto]`
- Validación determinista: `python scripts/validate_skill.py <ruta-al-SKILL.md>`
- Consulta de estándares: consultar [hardline_standards.md](./references/hardline_standards.md) y [failure_driven_mutation.md](./references/failure_driven_mutation.md).

## Quick Reference
| Operación | Comando / Acción | Salida Esperada |
| :--- | :--- | :--- |
| **Destilación en 1 Turno** | `/learn <tema>` | Directorio con `SKILL.md` validado y formateado |
| **Validación de Skill** | `python scripts/validate_skill.py <file>` | Código de salida 0 con confirmación de límites |
| **Auto-Mutación por Fallo** | Actualizar `## Pitfalls` en skill afectada | Respaldo `.bak` creado y gotcha añadido |

## Procedure

### Flujo A: Destilación en 1 Turno (`/learn`)
1. **Extracción de la Ruta Crítica**: Analizar el historial de la sesión o la fuente suministrada, aislando la secuencia exacta de comandos exitosos y descartando los intentos fallidos.
2. **Generación de Frontmatter Hardline**:
   - Asignar `name` en kebab-case ($\le 64$ caracteres).
   - Redactar `description`: exactamente una sola oración, $\le 60$ caracteres y terminada en punto.
3. **Estructuración Canónica**: Redactar las 8 secciones obligatorias respetando el orden canónico. Si la documentación técnica de soporte es extensa, bifurcar los detalles en `references/`.
4. **Validación Determinista**: Ejecutar `python scripts/validate_skill.py <ruta>` verificando que termine con código 0.
5. **Notificación al Usuario**: Emitir una confirmación minimalista en una sola línea indicando el nombre del skill y su ubicación.

### Flujo B: Auto-Mutación por Fallos (In-Situ Pitfall Patching)
1. **Comprobar Inmunidad**: Verificar que la skill a mutar no pertenezca al núcleo del sistema ni a un guardián.
2. **Crear Respaldo**: Copiar `SKILL.md` a `SKILL.md.bak` en la misma carpeta.
3. **Append de Gotcha**: Agregar la viñeta con el error y la solución al final de la sección `## Pitfalls`. Prohibido modificar el resto del documento.
4. **Validar**: Ejecutar `validate_skill.py` sobre el archivo mutado.
5. **Notificar**: Informar al usuario en el chat con el diff del aprendizaje consolidado.

## Pitfalls
- **Exceder 60 Caracteres en la Descripción**: Es la causa número uno de fallo en enrutamiento. Contar siempre los caracteres antes de persistir; si supera 60, recortar inmediatamente.
- **Inclusión de Slop de Marketing**: Evitar palabras vacías (*seamless*, *powerful*, *robust*) en la descripción; centrarse exclusivamente en la capacidad operativa.
- **Mutación Ciega sin Respaldo**: Jamás editar un `SKILL.md` sin generar antes la copia `.bak` de seguridad.
- **Rutas Absolutas en Scripts**: Utilizar siempre rutas relativas o `Path(__file__)` en scripts auxiliares para preservar la portabilidad universal.

## Verification
Para verificar la integridad del skill y de su validador interno, ejecutar:
```bash
python scripts/validate_skill.py SKILL.md
```
Debe responder con código de salida 0: `✅ VALIDACIÓN EXITOSA`.
