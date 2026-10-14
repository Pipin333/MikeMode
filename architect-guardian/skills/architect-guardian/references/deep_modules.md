# Principio de Módulos Profundos y Diseño de Costuras (Deep Modules)

Basado en la filosofía de diseño de John Ousterhout (*A Philosophy of Software Design*) y las técnicas de ingeniería de software para agentes.

---

## 1. Módulos Profundos vs. Módulos Superficiales

Un **módulo** es cualquier unidad con una **interfaz** y una **implementación** (una clase, una función, un paquete o un servicio).

### Módulo Profundo (*Deep Module*)
Presenta una interfaz pequeña y simple, pero oculta un comportamiento complejo, robusto e invariante.
Ofrece **alto apalancamiento (*leverage*)** para los consumidores y **alta localidad (*locality*)** para los mantenedores:

```text
┌──────────────────────────────────────┐
│       Interfaz Pequeña y Limpia       │  <- Pocas funciones, parámetros claros y comprensibles
├──────────────────────────────────────┤
│                                      │
│       Implementación Profunda        │  <- Invariantes, concurrencia, persistencia y validaciones ocultas
│                                      │
└──────────────────────────────────────┘
```

### Módulo Superficial (*Shallow Module*) - A Evitar
La interfaz es casi tan compleja o detallada como el código que ejecuta por debajo. A menudo actúa como mero pasamanos (*pass-through* o *middle man*), incrementando la carga cognitiva sin ofrecer valor real.

```text
┌────────────────────────────────────────────────────────┐
│               Interfaz Extensa y Verborrágica          │  <- Múltiples métodos, configuración dispersa
├────────────────────────────────────────────────────────┤
│  Implementación Delgada                                │  <- Solo delega a otra librería o función
└────────────────────────────────────────────────────────┘
```

---

## 2. El Test de la Eliminación (*The Deletion Test*)

Imagina eliminar el módulo del sistema:
- Si al borrarlo la complejidad simplemente **desaparece**, era un envoltorio innecesario.
- Si al borrarlo la complejidad se **desparrama** sobre múltiples archivos y llamadores (*callers*), el módulo estaba haciendo su trabajo y aportando localidad.

---

## 3. Principio de Costuras Reales (*Seams*)

Una **costura** (término de Michael Feathers) es un punto de acoplamiento donde el comportamiento puede alterarse sin editar el código en ese lugar.
- **Un solo adaptador = costura hipotética (Speculative Generality)**: No extraigas una interfaz o abstracción si solo existe una clase concreta que la implemente hoy.
- **Dos adaptadores = costura real**: Introduce la interfaz cuando existan al menos dos implementaciones concretas que compitan o coexistan genuinamente (ej. cliente PostgreSQL real y fake en memoria para tests).

---

## 4. Diseño para la Testabilidad

Los buenos módulos hacen que los tests sean simples y directos:
1. **Aceptar dependencias en el constructor o argumentos**, no instanciarlas internamente de forma rígida.
2. **Retornar resultados enriquecidos** en lugar de producir mutaciones o efectos secundarios ocultos en objetos globales.
3. **Superficie de prueba natural**: La interfaz pública es la superficie del test; evita exponer métodos privados o internos solo para poder probarlos.
