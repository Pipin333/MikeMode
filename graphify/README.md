# 🕸️ Graphify Plugin for Antigravity

Plugin para convertir cualquier base de código, documentación y esquemas en grafos de conocimiento interactivos (`graph.html`) usando AST determinista con **Tree-sitter** y detección de comunidades (clustering Louvain/Leiden).

---

## 🚀 Características Principales
* **Análisis AST Determinista**: Sin depender de bases de datos vectoriales estocásticas ni embeddings externos. Mapeo estructural de relaciones `imports`, `calls`, `inherits` y `depends_on`.
* **Visualización Web Interactiva (`graph.html`)**: Grafo interactivo navegable con física de fuerzas y colores por comunidades de módulos.
* **Reporte Topológico Sintético (`GRAPH_REPORT.md`)**: Resumen arquitectónico optimizado para la ventana de contexto del LLM.
* **Salvaguardas de Balthasar-2**:
  * Ejecución 100% bajo demanda (cero daemons permanentes).
  * Auto-inyección de exclusiones en `.gitignore` para no contaminar repositorios.
  * Modo local `--code-only` predeterminado ($0 coste, máxima velocidad).

---

## 🛠️ Instalación y Requisitos
El plugin utiliza el binario oficial de Graphify (`graphifyy` en PyPI), instalado localmente:

```bash
python -m uv tool install graphifyy
# O alternativamente:
pip install graphifyy
```

El binario queda disponible en `~/.local/bin/graphify.exe`.

---

## 📖 Uso

### Vía Runner Seguro en Python (Recomendado)
```bash
python skills/graphify/scripts/run_graphify.py --target "C:\ruta\a\tu\proyecto"
```

### Vía CLI Directa
```powershell
# Extraer grafo en modo local AST (rápido, costo $0)
& "$HOME\.local\bin\graphify.exe" extract "C:\ruta\a\tu\proyecto" --code-only

# Abrir el grafo interactivo resultante
Start-Process "C:\ruta\a\tu\proyecto\graphify-out\graph.html"

# Consultar el grafo
& "$HOME\.local\bin\graphify.exe" query "donde se procesa la autenticacion"
& "$HOME\.local\bin\graphify.exe" path ModuloA ModuloB
```

---

## ⚖️ Aprobación MAGI (Tokyo-3 Tribunal)
- **Melchior-1**: `AGREED` (Deep Module con alta parsimonia y superioridad sobre RAG probabilístico).
- **Balthasar-2**: `CONDITIONAL` (Exclusión estricta de `.gitignore` y ejecución bajo demanda cumplida).
- **Casper-3**: `AGREED` (Superpoder de onboarding visual en 30 segundos).
