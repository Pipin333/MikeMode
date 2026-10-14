# Modelado de Dominio Ubicuo (DDD), GLOSSARY.md y Registros ADR

Basado en *Domain-Driven Design* (Eric Evans) y las directrices de concisión de contexto para agentes de IA.

---

## 1. El Coste del Lenguaje Borroso

Cuando los desarrolladores y los agentes de IA se comunican utilizando descripciones largas en lugar de un **lenguaje ubicuo** formalizado, ocurren dos problemas graves:
1. **Desperdicio de ventana de contexto**: Una explicación de 25 palabras ("hay un problema cuando una lección dentro de una sección de un curso se materializa en el sistema de archivos...") consume tokens valiosos que podrían resumirse en 1 término preciso ("fallo en la cascada de materialización").
2. **Desalineación conceptual**: El agente confunde términos como `Usuario`, `Cliente`, `Cuenta`, `Perfil`, generando entidades cruzadas y lógica rota.

---

## 2. Convención `GLOSSARY.md`

El archivo `GLOSSARY.md` reside en la raíz del proyecto (o por subdominios si es un monorepo complejo):

```markdown
# Glosario del Proyecto

### Order (Pedido)
Contrato comercial inmutable que agrupa uno o más Items solicitados por un Cliente. Pasa por los estados: `Draft`, `Placed`, `Fulfilled` o `Cancelled`.

### Materialization (Materialización)
Proceso síncrono por el cual los metadatos de un recurso se escriben como archivos físicos persistentes en disco.
```

### Reglas para `GLOSSARY.md`
- **Cero detalles de implementación**: No almacenes rutas de base de datos, nombres de librerías ni snippets de código. Es exclusivamente un glosario de términos y definiciones semánticas.
- **Actualización inline**: En el momento en que se acuerde el significado de un concepto nuevo durante una sesión de diseño, agrégalo inmediatamente al glosario.

---

## 3. Registros de Decisión de Arquitectura (ADR)

Los ADRs documentan decisiones cruciales para evitar que futuros agentes o desarrolladores reconsideren alternativas ya descartadas.

### Ubicación
`docs/adr/NNNN-nombre-en-kebab-case.md` (ej. `docs/adr/0001-postgresql-jsonb-para-eventos.md`).

### Cuándo crear un ADR
Solo cuando se cumplan **las tres condiciones**:
1. **Difícil de revertir**: Cambiar de opinión más adelante requeriría semanas de migración o refactor masivo.
2. **Sorprendente sin contexto**: Quien lea el código se preguntará: "¿Por qué demonios hicieron esto de esta manera?".
3. **Fruto de un trade-off real**: Existían opciones legítimas (ej. Redis vs Postgres vs S3) y se eligió una con justificación técnica ponderada.

### Plantilla de ADR

```markdown
# ADR-0001: [Título de la decisión]

- **Estado**: Aceptado / En Revisión / Reemplazado por ADR-XXXX
- **Fecha**: YYYY-MM-DD
- **Autores**: [Nombres]

## Contexto
[Descripción concisa del problema técnico, requisitos y limitaciones].

## Decisión
[La arquitectura, tecnología o patrón elegido].

## Opciones Evaluadas
1. **Opción A**: [Pros y contras, por qué se descartó].
2. **Opción B (Elegida)**: [Justificación técnica].

## Consecuencias
- **Positivas**: [Beneficios esperados].
- **Negativas / Riesgos**: [Deuda asumida o compensaciones requeridas].
```
