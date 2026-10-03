# Marco Teórico y Operativo de los 6 Sombreros de Bono para Ingeniería de Software

Este documento detalla las directivas cognitivas estrictas para cada sombrero cuando se aplica a arquitectura, diseño de sistemas, refactorizaciones y decisiones de producto.

---

## 1. ⚪ Sombrero Blanco (El Científico de Datos)

- **Objetivo**: Neutralidad absoluta y enfoque en la verdad empírica.
- **Mentalidad**: "Sólo los hechos; ninguna deducción o juicio."
- **Preguntas directrices**:
  - ¿Qué información fáctica tenemos sobre el problema o código actual?
  - ¿Cuáles son las métricas reales (tiempos de respuesta, volumen de solicitudes, tamaño de tablas)?
  - ¿Cuáles son las restricciones no negociables (presupuesto, SLA, versiones de runtime, compliance)?
  - ¿Qué datos **no tenemos** y necesitamos medir o averiguar antes de decidir?
- **Anti-patrón común**: Deslizar opiniones como hechos (ej. *"Nuestra base de datos es lenta"* no es blanco; *"El percentil p99 de consultas a la tabla users tarda 1.8 segundos"* sí lo es).

---

## 2. 🔴 Sombrero Rojo (El Empático y el Instinto Técnico)

- **Objetivo**: Capturar sensaciones, intuiciones y fricciones humanas que la lógica pura suele ignorar hasta que es tarde.
- **Mentalidad**: "Lo que siento al respecto, sin necesidad de justificarlo."
- **Preguntas directrices**:
  - ¿Qué me dice el instinto técnico (*gut feeling*) sobre esta solución? ¿Huele a sobre-ingeniería?
  - ¿Cómo se sentirá el usuario final al interactuar con esta feature? ¿Genera frustración, duda o deleite?
  - ¿Cómo afectará esto a la moral del equipo de desarrollo? ¿Será una pesadilla que nadie querrá tocar en guardia?
- **Anti-patrón común**: Intentar justificar las emociones con argumentos lógicos. El Sombrero Rojo tiene derecho a decir: *"No me gusta esta API, se siente engorrosa y propensa a errores"* sin dar un teorema formal.

---

## 3. ⚫ Sombrero Negro (El Auditor de Riesgos / Abogado del Diablo)

- **Objetivo**: Identificar vulnerabilidades, riesgos catastróficos, inviabilidades y costes ocultos.
- **Mentalidad**: "Cautela rigurosa: ¿Por qué va a fallar y dónde están las trampas?"
- **Preguntas directrices**:
  - ¿Qué pasa si falla la red, se cae la base de datos o el tráfico se multiplica por 100?
  - ¿Dónde están las brechas de seguridad o de integridad de datos?
  - ¿Qué dependencias externas introducimos que puedan quedar descontinuadas o cambiar su licencia?
  - ¿Cuál es la deuda técnica que esta 'solución rápida' acumulará en los próximos 12 meses?
- **Anti-patrón común**: Pesimismo destructivo sin fundamento. El Sombrero Negro no es para quejarse por quejarse; debe señalar riesgos específicos, plausibles y sus posibles consecuencias.

---

## 4. 🟡 Sombrero Amarillo (El Arquitecto Optimista)

- **Objetivo**: Explorar el valor genuino, los beneficios a largo plazo y las condiciones ideales de éxito.
- **Mentalidad**: "Búsqueda deliberada de valor, eficiencia y oportunidades."
- **Preguntas directrices**:
  - ¿Cuáles son los mayores beneficios si esta implementación sale exactamente bien?
  - ¿Cómo acelera esto el ciclo de entrega o reduce los costes operativos?
  - ¿Qué puertas abre esta nueva arquitectura para futuras capacidades del sistema?
  - ¿Cómo podemos apalancar las fortalezas actuales de la plataforma?
- **Anti-patrón común**: Optimismo ciego ("todo va a funcionar mágicamente"). El optimismo amarillo debe basarse en un mecanismo creíble de cómo se genera el valor.

---

## 5. 🟢 Sombrero Verde (El Innovador Lateral)

- **Objetivo**: Generar alternativas radicales, desafiar axiomas y encontrar soluciones no obvias.
- **Mentalidad**: "Pensamiento provocativo: ¿Qué pasaría si...?"
- **Preguntas directrices**:
  - ¿Podemos resolver el 80% del problema eliminando código en lugar de escribiendo más?
  - ¿Qué pasaría si invertimos completamente el flujo de datos o la responsabilidad de los componentes?
  - ¿Hay alguna tecnología, patrón o librería que haga esto trivial fuera del paradigma actual?
  - Si tuviéramos que implementar esto en 4 horas, ¿cuál sería la solución más inteligente?
- **Anti-patrón común**: Censurarse por creer que una idea es "demasiado rara" o "poco ortodoxa". El Sombrero Verde debe proponerla; el Azul y el Negro ya se encargarán de filtrarla o podarla.

---

## 6. 🔵 Sombrero Azul (El Director de Orquesta y Síntesis)

- **Objetivo**: Facilitar el proceso, asegurar que cada sombrero cumpla su rol, mediar las contradicciones y formular el plan de acción.
- **Mentalidad**: "Metapensamiento y liderazgo ejecutivo."
- **Responsabilidades**:
  - Definir la agenda y el foco inicial.
  - Asegurar que el Sombrero Negro no aplaste al Sombrero Verde antes de que este desarrolle sus ideas.
  - Confrontar los riesgos del Sombrero Negro con las oportunidades del Amarillo y las innovaciones del Verde para crear mitigaciones concretas.
  - Redactar el **Plan de Implementación Definitivo**, priorizado y accionable.
