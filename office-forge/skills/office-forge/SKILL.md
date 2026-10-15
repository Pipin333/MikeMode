---
name: office-forge
description: Manipulación y generación profesional de documentos Excel (xlsx), Word (docx), PDF y presentaciones PowerPoint (pptx) con fórmulas dinámicas, estilos ejecutivos de banca de inversión y defensas anti-XXE / anti-Zip-bomb. Úsalo cuando el usuario pida exportar reportes, crear hojas de cálculo financieras con fórmulas vivas, extraer tablas de PDFs o armar presentaciones.
---

# 📑 OfficeForge Skill (Document Synthesis & Engineering)

OfficeForge dota al agente de capacidades de grado profesional para generar, editar y analizar documentos corporativos (.xlsx, .docx, .pdf, .pptx) mediante Python determinista. Elimina las alucinaciones de formato y la corrupción de XMLs binarios mediante módulos profundos respaldados por `openpyxl`, `python-docx`, `pypdf`, `pdfplumber`, `reportlab` y `python-pptx`.

---

## 🎯 Cuándo Usar Esta Habilidad
- **Hojas de Cálculo Financieras (.xlsx)**: Cuando el usuario pide un presupuesto, estimación de costos, modelo de ingresos o tabla de métricas. **Obligatorio usar fórmulas dinámicas vivas (`=SUM()`, `=C5*D5`), nunca números estáticos calculados a mano**.
- **Informes Ejecutivos (.docx / .pdf)**: Auditorías de arquitectura, reportes de consultoría, actas de acuerdos o manuales técnicos con jerarquía tipográfica, tablas cebradas y cajas de alerta (*callouts*).
- **Extracción de Datos de PDFs (.pdf)**: Extracción limpia de texto y parseo de tablas estructuradas hacia arrays o DataFrames sin pérdida de columnas.
- **Presentaciones Ejecutivas (.pptx)**: Creación de diapositivas en formato 16:9 con contraste nítido, puntos de impacto y jerarquía visual.

---

## 📐 Estándar Canónico de Banca de Inversión (Excel Rules)

Para cualquier hoja `.xlsx` generada:
1. **Fórmulas Dinámicas Obligatorias**: Si una celda es el resultado de una operación aritmética o suma, debe contener la fórmula de Excel (ej: `=SUM(E5:E20)` o `=C5*D5`). Prohibido insertar el total como valor plano.
2. **Código de Colores Canónico (Wall Street Model)**:
   * **Azul (`#0000FF`)**: Inputs manuales, supuestos y constantes del usuario.
   * **Negro (`#000000`)**: Fórmulas, cálculos y totales.
   * **Verde (`#008000`)**: Referencias a otras hojas (`=Hoja2!B5`).
   * **Rojo (`#FF0000`)**: Alertas, cheques de balance o anomalías.
3. **Líneas de Cuadrícula Activas**: Siempre activar `ws.views.sheetView[0].showGridLines = True`.
4. **Formato Numérico Estricto**: Todo valor monetario debe llevar formato de moneda (ej: `"$#,##0"`), los decimales deben tener dos dígitos (`"#,##0.00"`) y los porcentajes `"0.0%"`.
5. **Auto-ajuste de Columnas**: Calcular el ancho de columnas automáticamente para evitar el error `###` por ancho insuficiente.

---

## 🛡️ Salvaguardas de Seguridad (Directivas de Balthasar-2)
- **Defensa contra XXE**: Todo procesamiento de XMLs en Office debe usar `defusedxml` o deshabilitar la resolución de entidades externas (`resolve_entities=False`).
- **Defensa contra Zip-Bombs**: No abrir archivos de más de 45 MB ni con ratios de compresión anómalos (>1:20).
- **Prohibición de Macros**: Prohibido generar o ejecutar archivos con macros (`.xlsm`, `.docm`) sin confirmación explícita del usuario.

---

## 🚀 Uso Rápido mediante la API del Motor

El motor reside en `skills/office-forge/scripts/office_engine.py`. Puedes importarlo directamente en scripts de Python o en snippets de automatización:

### 1. Generar Excel Financiero con Fórmulas
```python
from office_engine import ExcelForge

ExcelForge.create_financial_sheet(
    output_path="presupuesto_q4.xlsx",
    title="Presupuesto de Infraestructura Cloud",
    headers=["Servicio", "Entorno", "Instancias", "Costo Unitario", "Subtotal"],
    rows=[
        ["API Gateway", "Producción", 2, 45000, "=C5*D5"],
        ["Base de Datos", "Producción", 1, 120000, "=C6*D6"],
        ["Cache Redis", "Producción", 2, 25000, "=C7*D7"],
    ],
    total_formula_cols=[5],  # Columna 5 (Subtotal) tendrá =SUM(...)
    is_currency_col=[4, 5]   # Formato $#,##0
)
```

### 2. Generar Informe Ejecutivo en Word
```python
from office_engine import WordForge

WordForge.create_executive_report(
    output_path="informe_seguridad.docx",
    title="Auditoría de Arquitectura y Seguridad",
    subtitle="Evaluación del Sistema MAGI | Octubre 2026",
    sections=[
        {
            "heading": "1. Resumen de Hallazgos",
            "callout": "Se mitigaron 3 vulnerabilidades críticas de inyección XSS.",
            "paragraphs": [
                "Se verificó la transición hacia URLs estáticas con compresión determinista.",
                "Se eliminó la dependencia de bases de datos remotas en el cálculo de presupuestos."
            ],
            "table": {
                "headers": ["Componente", "Riesgo", "Remediación"],
                "rows": [
                    ["URL Hash", "Alto (XSS)", "Sanitización estricta con escapeHTML"],
                    ["Payload LZW", "Medio (Truncamiento)", "Vector semilla mínimo <90 chars"]
                ]
            }
        }
    ]
)
```

### 3. Extraer Tablas de un PDF
```python
from office_engine import PdfForge

tabla_extraida = PdfForge.extract_tables("balance_financiero.pdf", page_num=1)
# Retorna lista de filas tabulares listas para procesar
```

### 4. Generar Presentación PPTX
```python
from office_engine import PresentationForge

PresentationForge.create_deck(
    output_path="presentacion_arquitectura.pptx",
    deck_title="Modernización de Infraestructura",
    deck_subtitle="Estrategia 2026",
    slides_data=[
        {
            "title": "Decisiones Clave de Arquitectura",
            "bullets": [
                "Desacoplamiento total de BaaS externos.",
                "Integración de Graphify para análisis topológico de código.",
                "Adopción de OfficeForge para entregables corporativos."
            ]
        }
    ]
)
```
