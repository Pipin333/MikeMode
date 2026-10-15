# 📑 OfficeForge Plugin for Antigravity

Plugin para la generación, manipulación y extracción programática de documentos corporativos en formatos **Excel (`.xlsx`)**, **Word (`.docx`)**, **PDF (`.pdf`)** y **PowerPoint (`.pptx`)** mediante Python determinista.

---

## 🌟 Capacidades Clave
* **Hojas de Cálculo Financieras (.xlsx)**:
  * Generación con fórmulas dinámicas vivas (`=SUM()`, `=AVERAGE()`, multiplicaciones de celdas).
  * Estándar de colores canónico de banca de inversión (azul para inputs, negro para fórmulas, verde para hojas cruzadas).
  * Auto-ajuste de columnas y formato monetario automático.
* **Documentos Ejecutivos (.docx)**:
  * Jerarquía visual limpia (Aptos / Calibri).
  * Cajas de alerta destacadas (*callouts*) con acentos de color.
  * Tablas estilizadas con cabeceras azul marino y filas alternadas (*zebra striping*).
* **Herramientas para PDFs (.pdf)**:
  * Extracción de texto con límites seguros de memoria.
  * Parseo de tablas estructuradas con `pdfplumber`.
* **Presentaciones (.pptx)**:
  * Diapositivas widescreen 16:9 con jerarquía tipográfica y contraste nítido.
* **Defensas de Seguridad (Balthasar-2)**:
  * Protección contra ataques de inyección XML (XXE) vía `defusedxml`.
  * Verificación de tamaños y ratios de descompresión para neutralizar *Zip-Bombs*.

---

## 🛠️ Requisitos
Librerías Python estándar para procesamiento ofimático:
```bash
pip install openpyxl python-docx pypdf pdfplumber python-pptx defusedxml reportlab
```

---

## 📖 Uso Rápido vía CLI
El plugin incluye un motor de demostración y generación en `skills/office-forge/scripts/office_engine.py`:

```bash
# Probar generación de todos los formatos de ejemplo
python skills/office-forge/scripts/office_engine.py --demo all --outdir ./mis_documentos
```

O importa directamente los módulos `ExcelForge`, `WordForge`, `PdfForge` o `PresentationForge` en tus scripts Python.
