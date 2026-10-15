---
name: graphify
description: Convierte cualquier base de código, documentación y esquemas en grafos de conocimiento interactivos (graph.html) usando AST determinista con Tree-sitter y detección de comunidades. Úsalo para onboarding en repositorios masivos, auditoría de dependencias, cálculo visual de blast radius y compresión topológica antes de refactorizar.
---

# 🕸️ Graphify Skill (Knowledge Graph & Architecture Visualizer)

Graphify transforma un repositorio completo de software en un **Grafo de Conocimiento Interactivo** sin depender de bases de datos vectoriales ni incurrir en alucinaciones estocásticas. Utiliza gramáticas formales de **Tree-sitter** para parsear el código a nivel de Árbol de Sintaxis Abstracta (AST) y aplica algoritmos de clustering (Louvain/Leiden) para descubrir comunidades y módulos acoplados.

## 🎯 Cuándo Usar Esta Habilidad
- **Onboarding Rápido**: Cuando aterrizas en un repositorio nuevo o de gran tamaño (>5.000 líneas) y necesitas entender la arquitectura en 30 segundos.
- **Auditoría de Módulos Profundos y Acoplamiento**: Antes de emprender una refactorización (siguiendo *Architect-Guardian*), para ver qué módulos están en el núcleo espagueti y cuáles son periféricos.
- **Mapeo de Radio de Explosión (*Blast Radius*)**: Para identificar todas las funciones y módulos aguas abajo que dependen de un contrato antes de modificarlo.
- **Visualización para el Usuario**: Cuando el usuario pide ver el mapa de su proyecto o generar un diagrama interactivo navegable en el navegador.

---

## 🛡️ Salvaguardas Obligatorias (Directivas de Balthasar-2)
Para evitar saturación de memoria, cuelgues del host o polución de repositorios:
1. **Ejecución On-Demand**: Graphify es una herramienta episódica bajo demanda, **nunca un daemon residente ni un hook síncrono bloqueante**.
2. **Protección de `.gitignore`**: Todo proyecto analizado **debe tener en su `.gitignore`**:
   ```gitignore
   # Graphify output & cache
   graphify-out/
   .graphify/
   graph.html
   graph.json
   GRAPH_REPORT.md
   ```
3. **Exclusiones Estrictas de Escaneo**: Prohibido escanear carpetas masivas de dependencias o secretos (`node_modules`, `.venv`, `venv`, `.git`, `dist`, `build`, `__pycache__` y `.env*`).
4. **Modo Predeterminado (`--code-only`)**: Salvo petición expresa de análisis semántico con LLM externo, priorizar siempre el modo local `--code-only` (AST 100% determinista, costo $0, velocidad inmediata sin necesidad de API keys).

---

## 🚀 Flujo de Ejecución

### 1. Invocación Asistida mediante Runner Seguro
El plugin incluye un runner en Python que valida automáticamente las dependencias, aplica exclusiones seguras y verifica el `.gitignore`:

```powershell
python "C:\Users\Petiso\.gemini\config\plugins\graphify\skills\graphify\scripts\run_graphify.py" --target "<ruta_del_proyecto>"
```

### 2. Comandos CLI Directos
Si prefieres usar el binario directamente desde PowerShell:

* **Mapeo Rápido Local (AST determinista sin API key, recomendado)**:
  ```powershell
  & "C:\Users\Petiso\.local\bin\graphify.exe" extract "<ruta_del_proyecto>" --code-only
  ```

* **Exportar Grafo Interactivo HTML**:
  ```powershell
  & "C:\Users\Petiso\.local\bin\graphify.exe" export html --graph "<ruta_del_proyecto>\graphify-out\graph.json"
  ```

* **Consultar Dependencias o Rutas entre Módulos**:
  ```powershell
  & "C:\Users\Petiso\.local\bin\graphify.exe" path ModuloA ModuloB
  & "C:\Users\Petiso\.local\bin\graphify.exe" query "donde se procesa la autenticacion"
  ```

* **Exportar Árbol Jerárquico D3 (Tree View)**:
  ```powershell
  & "C:\Users\Petiso\.local\bin\graphify.exe" tree --graph "<ruta_del_proyecto>\graphify-out\graph.json"
  ```

---

## 📊 Artefactos Producidos
Al completar la extracción, se genera la carpeta `graphify-out/` en la raíz del proyecto:
1. **`graph.html`**: Visualización web interactiva en 2D/3D con nodos coloreados por comunidad y enlaces de dependencia navegables con zoom y física de fuerzas.
2. **`graph.json`**: Estructura de datos completa de nodos (archivos, funciones, clases) y aristas (`imports`, `calls`, `inherits`).
3. **`GRAPH_REPORT.md`**: Reporte sintético en Markdown con el ranking de centralidad, componentes críticos y comunidades detectadas, ideal para ser leído por el agente sin saturar la ventana de contexto.

---

## 💡 Buenas Prácticas
- Tras generar `graph.html`, preséntale el enlace clickable al usuario: `file:///<ruta_del_proyecto>/graphify-out/graph.html`.
- Si el reporte detecta un nodo con centralidad desproporcionada (*God Class* / *God Module*), utilízalo como evidencia para proponer una refactorización de corte vertical (*Tracer Bullet*).
