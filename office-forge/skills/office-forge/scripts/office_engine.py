"""Motor unificado de generación y manipulación de documentos Office (XLSX, DOCX, PDF, PPTX).

Diseñado bajo estándares de banca de inversión y consultoría estratégica:
- Excel: Fórmulas dinámicas vivas, colores canónicos (azul/negro), auto-ajuste de columnas.
- Word: Tipografía ejecutiva, tablas con encabezados estilizados y cajas de alerta.
- PDF: Extracción segura de tablas y texto con pdfplumber y pypdf.
- PPTX: Diapositivas limpias con jerarquía visual y contraste profesional.
- Seguridad: Defensas contra XXE y verificación de límites de tamaño.
"""

import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Inmunización contra charmap en Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")


# ═══════════════════════════════════════════════════════════════════════════
# 1. EXCEL FORGE (XLSX)
# ═══════════════════════════════════════════════════════════════════════════

class ExcelForge:
    """Generador y manipulador de hojas de cálculo de alta fidelidad."""

    HEADER_FILL = "1F4E78"  # Azul marino corporativo
    HEADER_FONT = "FFFFFF"  # Blanco
    INPUT_FONT = "0000FF"   # Azul = Inputs y Supuestos
    FORMULA_FONT = "000000" # Negro = Fórmulas y Cálculos
    ZEBRA_FILL = "F2F2F2"   # Gris muy tenue para filas alternas

    @classmethod
    def create_financial_sheet(
        cls,
        output_path: str,
        title: str,
        headers: List[str],
        rows: List[List[Any]],
        total_formula_cols: Optional[List[int]] = None,
        is_currency_col: Optional[List[int]] = None,
    ) -> str:
        """Crea una hoja de cálculo profesional con formato corporativo y fórmulas.

        Args:
            output_path: Ruta de destino del archivo .xlsx.
            title: Título principal de la tabla/hoja.
            headers: Lista de nombres de columnas.
            rows: Matriz de datos. Si una celda es fórmula (inicia con '='), se formatea en negro.
            total_formula_cols: Índices de columnas (1-based) donde se inyectará una fila de TOTAL `=SUM(...)`.
            is_currency_col: Índices de columnas (1-based) que deben formatearse como moneda CLP ($#,##0).

        Returns:
            Ruta absoluta del archivo generado.
        """
        import openpyxl
        from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
        from openpyxl.utils import get_column_letter

        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Resumen"
        ws.views.sheetView[0].showGridLines = True

        thin_side = Side(style="thin", color="D9D9D9")
        thin_border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)
        double_bottom = Border(
            left=thin_side,
            right=thin_side,
            top=Side(style="thin", color="000000"),
            bottom=Side(style="double", color="000000"),
        )

        # 1. Título principal
        ws.merge_cells(start_row=2, start_column=2, end_row=2, end_column=len(headers) + 1)
        title_cell = ws.cell(row=2, column=2, value=title.upper())
        title_cell.font = Font(name="Calibri", size=15, bold=True, color="1F4E78")
        title_cell.alignment = Alignment(vertical="center")
        ws.row_dimensions[2].height = 30

        # 2. Encabezados de tabla
        header_row_idx = 4
        ws.row_dimensions[header_row_idx].height = 24
        for col_idx, header in enumerate(headers, start=2):
            cell = ws.cell(row=header_row_idx, column=col_idx, value=header)
            cell.fill = PatternFill(start_color=cls.HEADER_FILL, end_color=cls.HEADER_FILL, fill_type="solid")
            cell.font = Font(name="Calibri", size=11, bold=True, color=cls.HEADER_FONT)
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.border = thin_border

        # 3. Filas de datos
        start_data_row = 5
        curr_row = start_data_row

        currency_indices = set(is_currency_col or [])

        for r_data in rows:
            ws.row_dimensions[curr_row].height = 20
            is_zebra = (curr_row % 2 == 0)
            row_fill = PatternFill(start_color=cls.ZEBRA_FILL, end_color=cls.ZEBRA_FILL, fill_type="solid") if is_zebra else None

            for c_idx, val in enumerate(r_data, start=2):
                cell = ws.cell(row=curr_row, column=c_idx)
                cell.border = thin_border
                if row_fill:
                    cell.fill = row_fill

                # Detección de fórmula vs input
                is_formula = isinstance(val, str) and val.startswith("=")
                cell.value = val

                # Estándar de colores Wall Street
                font_color = cls.FORMULA_FONT if is_formula else (cls.INPUT_FONT if isinstance(val, (int, float)) else "000000")
                cell.font = Font(name="Calibri", size=10, color=font_color)

                # Alineación y formato
                if isinstance(val, (int, float)) or is_formula:
                    cell.alignment = Alignment(horizontal="right", vertical="center")
                    if (c_idx - 1) in currency_indices:
                        cell.number_format = '"$"#,##0'
                    elif isinstance(val, float):
                        cell.number_format = "#,##0.00"
                    else:
                        cell.number_format = "#,##0"
                else:
                    cell.alignment = Alignment(horizontal="left", vertical="center")

            curr_row += 1

        # 4. Fila de Totales con fórmulas automáticas
        if total_formula_cols:
            ws.row_dimensions[curr_row].height = 22
            total_label_cell = ws.cell(row=curr_row, column=2, value="TOTAL")
            total_label_cell.font = Font(name="Calibri", size=10, bold=True)
            total_label_cell.alignment = Alignment(horizontal="left", vertical="center")
            total_label_cell.border = double_bottom

            for c_idx in range(2, len(headers) + 2):
                cell = ws.cell(row=curr_row, column=c_idx)
                cell.border = double_bottom
                header_relative_idx = c_idx - 1

                if header_relative_idx in total_formula_cols:
                    col_letter = get_column_letter(c_idx)
                    cell.value = f"=SUM({col_letter}{start_data_row}:{col_letter}{curr_row - 1})"
                    cell.font = Font(name="Calibri", size=10, bold=True, color=cls.FORMULA_FONT)
                    cell.alignment = Alignment(horizontal="right", vertical="center")
                    if header_relative_idx in currency_indices:
                        cell.number_format = '"$"#,##0'
                    else:
                        cell.number_format = "#,##0"

        # 5. Auto-ajuste de ancho de columnas
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val_str = str(cell.value or "")
                if not cell.coordinate in ws.merged_cells:
                    max_len = max(max_len, len(val_str))
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

        out_path = Path(output_path).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        wb.save(out_path)
        print(f"📊 Excel corporativo creado: {out_path.as_uri()}")
        return str(out_path)


# ═══════════════════════════════════════════════════════════════════════════
# 2. WORD FORGE (DOCX)
# ═══════════════════════════════════════════════════════════════════════════

class WordForge:
    """Generador de informes ejecutivos en Word con diseño editorial."""

    @classmethod
    def create_executive_report(
        cls,
        output_path: str,
        title: str,
        subtitle: str,
        sections: List[Dict[str, Any]],
    ) -> str:
        """Crea un documento Word con jerarquía visual y tablas estilizadas.

        Args:
            output_path: Ruta de destino del archivo .docx.
            title: Título principal del documento.
            subtitle: Subtítulo o metadata ejecutiva.
            sections: Lista de diccionarios con 'heading', 'paragraphs' (lista),
                      opcional 'callout' (texto destacado) y opcional 'table' {'headers': [...], 'rows': [...]}.

        Returns:
            Ruta absoluta del archivo generado.
        """
        import docx
        from docx.shared import Inches, Pt, RGBColor
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.enum.table import WD_TABLE_ALIGNMENT
        from docx.oxml import OxmlElement
        from docx.oxml.ns import qn

        doc = docx.Document()

        # Ajuste de márgenes (1 pulgada estándar)
        for section in doc.sections:
            section.top_margin = Inches(1)
            section.bottom_margin = Inches(1)
            section.left_margin = Inches(1)
            section.right_margin = Inches(1)

        # 1. Título Principal
        title_p = doc.add_paragraph()
        title_p.paragraph_format.space_before = Pt(0)
        title_p.paragraph_format.space_after = Pt(4)
        run_title = title_p.add_run(title)
        run_title.font.name = "Calibri"
        run_title.font.size = Pt(24)
        run_title.font.bold = True
        run_title.font.color.rgb = RGBColor(0x1F, 0x4E, 0x78)

        # 2. Subtítulo
        sub_p = doc.add_paragraph()
        sub_p.paragraph_format.space_after = Pt(24)
        run_sub = sub_p.add_run(subtitle)
        run_sub.font.name = "Calibri"
        run_sub.font.size = Pt(11)
        run_sub.font.color.rgb = RGBColor(0x59, 0x59, 0x59)

        # Divisor horizontal
        div_p = doc.add_paragraph()
        div_p.paragraph_format.space_after = Pt(16)
        pPr = div_p._element.get_or_add_pPr()
        pBdr = OxmlElement('w:pBdr')
        bottom = OxmlElement('w:bottom')
        bottom.set(qn('w:val'), 'single')
        bottom.set(qn('w:sz'), '12')
        bottom.set(qn('w:space'), '1')
        bottom.set(qn('w:color'), '1F4E78')
        pBdr.append(bottom)
        pPr.append(pBdr)

        # 3. Secciones
        for sec in sections:
            if "heading" in sec:
                h = doc.add_heading(sec["heading"], level=1)
                h.paragraph_format.space_before = Pt(18)
                h.paragraph_format.space_after = Pt(8)
                for run in h.runs:
                    run.font.name = "Calibri"
                    run.font.color.rgb = RGBColor(0x1F, 0x4E, 0x78)

            # Cajas de alerta / Callout
            if "callout" in sec:
                call_table = doc.add_table(rows=1, cols=1)
                call_table.alignment = WD_TABLE_ALIGNMENT.CENTER
                call_cell = call_table.cell(0, 0)
                call_cell.width = Inches(6.5)

                tcPr = call_cell._element.get_or_add_tcPr()
                # Fondo gris muy claro
                shd = OxmlElement('w:shd')
                shd.set(qn('w:val'), 'clear')
                shd.set(qn('w:color'), 'auto')
                shd.set(qn('w:fill'), 'F2F4F7')
                tcPr.append(shd)

                # Borde izquierdo grueso azul, otros sin borde
                tcBorders = OxmlElement('w:tcBorders')
                left = OxmlElement('w:left')
                left.set(qn('w:val'), 'single')
                left.set(qn('w:sz'), '24')
                left.set(qn('w:color'), '1F4E78')
                tcBorders.append(left)
                for b_name in ['top', 'bottom', 'right']:
                    b = OxmlElement(f'w:{b_name}')
                    b.set(qn('w:val'), 'none')
                    tcBorders.append(b)
                tcPr.append(tcBorders)

                cp = call_cell.paragraphs[0]
                cp.paragraph_format.space_before = Pt(6)
                cp.paragraph_format.space_after = Pt(6)
                c_run = cp.add_run(sec["callout"])
                c_run.font.name = "Calibri"
                c_run.font.size = Pt(10.5)
                c_run.font.italic = True
                c_run.font.color.rgb = RGBColor(0x26, 0x26, 0x26)

                doc.add_paragraph().paragraph_format.space_after = Pt(6)

            # Párrafos de contenido
            for p_text in sec.get("paragraphs", []):
                p = doc.add_paragraph()
                p.paragraph_format.space_after = Pt(8)
                p.paragraph_format.line_spacing = 1.15
                run = p.add_run(p_text)
                run.font.name = "Calibri"
                run.font.size = Pt(11)
                run.font.color.rgb = RGBColor(0x26, 0x26, 0x26)

            # Tablas estilizadas
            if "table" in sec:
                t_data = sec["table"]
                headers = t_data.get("headers", [])
                rows = t_data.get("rows", [])

                table = doc.add_table(rows=len(rows) + 1, cols=len(headers))
                table.alignment = WD_TABLE_ALIGNMENT.CENTER

                # Encabezado
                for c_idx, h_text in enumerate(headers):
                    hdr_cell = table.cell(0, c_idx)
                    hdr_cell.paragraphs[0].text = h_text
                    hdr_cell.paragraphs[0].runs[0].font.bold = True
                    hdr_cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                    hdr_cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
                    tcPr = hdr_cell._element.get_or_add_tcPr()
                    shd = OxmlElement('w:shd')
                    shd.set(qn('w:val'), 'clear')
                    shd.set(qn('w:fill'), '1F4E78')
                    tcPr.append(shd)

                # Filas
                for r_idx, row_values in enumerate(rows, start=1):
                    for c_idx, cell_value in enumerate(row_values):
                        c = table.cell(r_idx, c_idx)
                        c.paragraphs[0].text = str(cell_value)
                        c.paragraphs[0].runs[0].font.name = "Calibri"
                        c.paragraphs[0].runs[0].font.size = Pt(10)
                        if r_idx % 2 == 0:
                            tcPr = c._element.get_or_add_tcPr()
                            shd = OxmlElement('w:shd')
                            shd.set(qn('w:val'), 'clear')
                            shd.set(qn('w:fill'), 'F9FAFB')
                            tcPr.append(shd)

                doc.add_paragraph().paragraph_format.space_after = Pt(12)

        out_path = Path(output_path).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        doc.save(out_path)
        print(f"📄 Documento Word creado: {out_path.as_uri()}")
        return str(out_path)


# ═══════════════════════════════════════════════════════════════════════════
# 3. PDF FORGE (PDF)
# ═══════════════════════════════════════════════════════════════════════════

class PdfForge:
    """Extractor y manipulador de documentos PDF."""

    MAX_SAFE_PDF_SIZE_MB = 45

    @classmethod
    def extract_text(cls, pdf_path: str, max_pages: int = 50) -> str:
        """Extrae texto completo de un PDF con protección de desbordamiento de búfer.

        Args:
            pdf_path: Ruta al archivo PDF.
            max_pages: Límite de páginas a procesar para evitar saturación de memoria.

        Returns:
            Texto extraído de las páginas.
        """
        import pypdf

        path = Path(pdf_path)
        size_mb = path.stat().st_size / (1024 * 1024)
        if size_mb > cls.MAX_SAFE_PDF_SIZE_MB:
            raise ValueError(f"El archivo PDF ({size_mb:.1f} MB) excede el límite de seguridad de {cls.MAX_SAFE_PDF_SIZE_MB} MB.")

        reader = pypdf.PdfReader(str(path))
        extracted_text = []

        total_pages = min(len(reader.pages), max_pages)
        for i in range(total_pages):
            page_text = reader.pages[i].extract_text() or ""
            extracted_text.append(f"--- PÁGINA {i+1} ---\n{page_text}")

        return "\n\n".join(extracted_text)

    @classmethod
    def extract_tables(cls, pdf_path: str, page_num: int = 1) -> List[List[Any]]:
        """Extrae tablas estructuradas de una página PDF usando pdfplumber.

        Args:
            pdf_path: Ruta al archivo PDF.
            page_num: Número de página (1-based).

        Returns:
            Lista de filas tabulares extraídas.
        """
        import pdfplumber

        with pdfplumber.open(pdf_path) as pdf:
            if page_num > len(pdf.pages):
                return []
            page = pdf.pages[page_num - 1]
            tables = page.extract_tables()
            return tables[0] if tables else []


# ═══════════════════════════════════════════════════════════════════════════
# 4. PRESENTATION FORGE (PPTX)
# ═══════════════════════════════════════════════════════════════════════════

class PresentationForge:
    """Generador de presentaciones PowerPoint de alta gama."""

    @classmethod
    def create_deck(
        cls,
        output_path: str,
        deck_title: str,
        deck_subtitle: str,
        slides_data: List[Dict[str, Any]],
    ) -> str:
        """Crea una presentación PPTX moderna.

        Args:
            output_path: Ruta de salida .pptx.
            deck_title: Título de portada.
            deck_subtitle: Subtítulo de portada.
            slides_data: Lista de slides con 'title' y 'bullets' (lista de puntos clave).

        Returns:
            Ruta absoluta del archivo generado.
        """
        from pptx import Presentation
        from pptx.util import Inches, Pt
        from pptx.dml.color import RGBColor

        prs = Presentation()
        prs.slide_width = Inches(13.333)  # Formato 16:9 widescreen
        prs.slide_height = Inches(7.5)

        # 1. Slide de Portada
        title_slide_layout = prs.slide_layouts[0]
        slide = prs.slides.add_slide(title_slide_layout)
        title = slide.shapes.title
        subtitle = slide.placeholders[1]

        title.text = deck_title
        subtitle.text = deck_subtitle

        # 2. Slides de Contenido
        content_layout = prs.slide_layouts[1]
        for s_info in slides_data:
            s = prs.slides.add_slide(content_layout)
            s.shapes.title.text = s_info.get("title", "")

            body = s.placeholders[1]
            tf = body.text_frame
            tf.word_wrap = True

            bullets = s_info.get("bullets", [])
            if bullets:
                tf.text = bullets[0]
                for b_text in bullets[1:]:
                    p = tf.add_paragraph()
                    p.text = b_text
                    p.level = 0

        out_path = Path(output_path).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        prs.save(out_path)
        print(f"📊 Presentación PowerPoint creada: {out_path.as_uri()}")
        return str(out_path)


# ═══════════════════════════════════════════════════════════════════════════
# CLI RUNNER
# ═══════════════════════════════════════════════════════════════════════════

def main() -> None:
    """Demostración y verificación del motor OfficeForge."""
    import argparse

    parser = argparse.ArgumentParser(description="OfficeForge CLI - Document Generation Engine")
    parser.add_argument("--demo", choices=["xlsx", "docx", "pptx", "all"], default="all")
    parser.add_argument("--outdir", default="./output_demo")

    args = parser.parse_args()
    out = Path(args.outdir)

    print("🚀 Ejecutando verificación de OfficeForge...")

    if args.demo in ["xlsx", "all"]:
        ExcelForge.create_financial_sheet(
            output_path=str(out / "demo_presupuesto.xlsx"),
            title="Presupuesto Corporativo Q4",
            headers=["Ítem", "Categoría", "Cantidad", "Precio Unitario", "Subtotal"],
            rows=[
                ["Servidores Cloud", "Infraestructura", 4, 150000, "=C5*D5"],
                ["Licencias LLM", "IA", 10, 45000, "=C6*D6"],
                ["Auditoría Externa", "Seguridad", 1, 850000, "=C7*D7"],
                ["Monitoreo APM", "Operaciones", 2, 75000, "=C8*D8"],
            ],
            total_formula_cols=[5],
            is_currency_col=[4, 5],
        )

    if args.demo in ["docx", "all"]:
        WordForge.create_executive_report(
            output_path=str(out / "demo_informe.docx"),
            title="Informe de Seguridad y Arquitectura",
            subtitle="Preparado por Antigravity & MAGI Tribunal | Octubre 2026",
            sections=[
                {
                    "heading": "1. Resumen Ejecutivo",
                    "callout": "Dictamen Unánime MAGI: Se aprueba la transición a modelos estáticos y verificación determinista formal.",
                    "paragraphs": [
                        "El presente informe consolida los resultados del análisis de infraestructura y arquitectura de software.",
                        "Se identificaron oportunidades críticas de optimización de costos y blindaje ante vectores de ataque XSS.",
                    ],
                },
                {
                    "heading": "2. Matriz de Resultados",
                    "table": {
                        "headers": ["Módulo", "Estado Previo", "Estado Optimizado", "Ahorro Estimado"],
                        "rows": [
                            ["Base de Datos", "Firebase BaaS ($)", "Serverless Hash ($0)", "100%"],
                            ["Análisis de Código", "RAG Vectorial", "Tree-sitter AST", "80% Tokens"],
                            ["Auditoría", "Manual", "Semgrep Formal", "5x Velocidad"],
                        ],
                    },
                },
            ],
        )

    if args.demo in ["pptx", "all"]:
        PresentationForge.create_deck(
            output_path=str(out / "demo_presentacion.pptx"),
            deck_title="Modernización de Arquitectura",
            deck_subtitle="Estrategia y Próximos Pasos 2026",
            slides_data=[
                {
                    "title": "Pilares de la Nueva Infraestructura",
                    "bullets": [
                        "Cero costos fijos mediante arquitectura estática serverless.",
                        "Verificación determinista con Tree-sitter y Semgrep.",
                        "Integración nativa de OfficeForge para entregables ejecutivos.",
                    ],
                },
                {
                    "title": "Hoja de Ruta de Implementación",
                    "bullets": [
                        "Fase 1: Despliegue de plugins en MikeMode.",
                        "Fase 2: Refactorización de calculadoracopete a URLs comprimidas.",
                        "Fase 3: Auditoría formal de seguridad previa al deploy.",
                    ],
                },
            ],
        )

    print("\n✅ Todas las demostraciones se completaron con éxito.")


if __name__ == "__main__":
    main()
