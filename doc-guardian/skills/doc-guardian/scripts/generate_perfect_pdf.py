#!/usr/bin/env python3
"""Generador universal de documentos PDF editoriales a partir de Markdown con Playwright.

Este módulo forma parte de la suite Doc-Guardian. Compila archivos Markdown
(reportes técnicos, informes ejecutivos, artículos de investigación o documentación técnica)
en documentos PDF con estándar de publicación editorial de alta resolución.

Características principales:
- Paginación estricta y predecible delimitada por '---'.
- Incrustación atómica de imágenes y capturas locales en Base64 para prevenir bloqueos de CORS.
- Control milimétrico de saltos de página evitando particiones accidentales en tablas y código.
- Sanitización de emojis informales y rutas locales de depuración.
- Soporte para fórmulas matemáticas KaTeX / MathJax 3.
- Cumplimiento riguroso de PEP 8 y PEP 257.
"""

import argparse
import base64
import mimetypes
import os
import re
import sys
from typing import Optional, Tuple

import markdown_it
from playwright.sync_api import sync_playwright

# Configurar salida segura en consolas Windows (cp1252 / PowerShell)
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def extract_title_from_markdown(content: str) -> str:
    """Extrae el primer encabezado de nivel 1 como título formal del documento.

    Args:
        content (str): Texto plano del archivo Markdown.

    Returns:
        str: Título extraído sin etiquetas de formato o valor por defecto.
    """
    match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if match:
        raw_title = match.group(1).strip()
        return re.sub(r"\[(.*?)\]\(.*?\)", r"\1", raw_title)
    return "Documento Técnico"


def sanitize_markdown_content(raw_text: str) -> str:
    """Limpia emojis informales y referencias a rutas locales del sistema de archivos.

    Args:
        raw_text (str): Texto Markdown sin procesar.

    Returns:
        str: Texto sanitizado con formato apto para presentación formal.
    """
    cleaned = raw_text.replace("❌", "[NO IMPLEMENTADO]").replace("✅", "[CORRECTO]")
    emoji_pattern = re.compile(
        r"[\U00010000-\U0010ffff]|[\u2600-\u27ff]", flags=re.UNICODE
    )
    cleaned = emoji_pattern.sub("", cleaned)

    # Eliminar referencias directas a rutas locales en enlaces de texto
    cleaned = re.sub(r"\*\(Evidencia:\s*\[.*?\]\(.*?\)\)\*\s*\n*", "", cleaned)
    cleaned = re.sub(r"\[.*?\]\(file:///.*?\)", "", cleaned)

    return cleaned


def embed_local_images_as_base64(content: str, base_dir: str) -> str:
    """Convierte referencias a imágenes locales en Data URIs Base64 con clases semánticas.

    Garantiza que el motor Chromium renderice las imágenes sin restricciones de seguridad
    de origen local ni enlaces rotos al compartir o mover el documento.

    Args:
        content (str): Contenido Markdown sanitizado.
        base_dir (str): Directorio base para resolver rutas relativas.

    Returns:
        str: Texto con etiquetas HTML figure optimizadas para paginación estricta.
    """
    def replacer(match: re.Match) -> str:
        alt_text = match.group(1).strip()
        src = match.group(2).strip()

        clean_src = src
        if clean_src.startswith("file:///"):
            clean_src = clean_src[8:]
        if re.match(r"^/[a-zA-Z]:", clean_src):
            clean_src = clean_src[1:]

        if os.path.isabs(clean_src) and os.path.exists(clean_src):
            img_path = clean_src
        else:
            candidate = os.path.join(base_dir, clean_src)
            img_path = candidate if os.path.exists(candidate) else None

        if img_path and os.path.exists(img_path):
            mime_type, _ = mimetypes.guess_type(img_path)
            if not mime_type:
                mime_type = "image/png"
            with open(img_path, "rb") as f_img:
                b64 = base64.b64encode(f_img.read()).decode("utf-8")
            data_uri = f"data:{mime_type};base64,{b64}"

            is_mobile = any(
                term in alt_text.lower() for term in ["móvil", "movil", "smartphone"]
            )
            img_class = "fig-mobile" if is_mobile else "fig-desktop"

            return (
                f"\n<div class='figure-container'>"
                f"<img src='{data_uri}' alt='{alt_text}' class='{img_class}' />"
                f"<div class='figure-caption'>{alt_text}</div>"
                f"</div>\n"
            )

        return match.group(0)

    return re.sub(r"!\[(.*?)\]\((.*?)\)", replacer, content)


def paginate_sections_to_html(content: str, md_parser: markdown_it.MarkdownIt) -> str:
    """Divide el Markdown en páginas independientes delimitadas por '---'.

    Garantiza que cada sección temática o caso visual se ubique en su propia página.

    Args:
        content (str): Texto Markdown con figuras ya incrustadas.
        md_parser (markdown_it.MarkdownIt): Instancia configurada de Markdown-It.

    Returns:
        str: Fragmento HTML estructurado con divisiones por página.
    """
    raw_sections = content.split("\n---\n")
    html_pages = []

    for index, raw_sec in enumerate(raw_sections):
        trimmed = raw_sec.strip()
        if not trimmed:
            continue

        rendered = md_parser.render(trimmed)

        if index == 0:
            html_pages.append(f'<div class="doc-page cover-page">{rendered}</div>')
        else:
            html_pages.append(f'<div class="doc-page standard-page">{rendered}</div>')

    return "\n".join(html_pages)


def build_full_html_document(
    body_html: str, doc_title: str, has_math: bool = False
) -> str:
    """Construye el documento HTML con hojas de estilo CSS para paginación estricta.

    Args:
        body_html (str): Contenido HTML paginado.
        doc_title (str): Título oficial del documento.
        has_math (bool, optional): Indica si se debe incluir el script de MathJax.

    Returns:
        str: Documento HTML completo listo para renderizar con Playwright.
    """
    math_script = ""
    if has_math:
        math_script = """
    <script>
    window.MathJax = {
      tex: {
        inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
        displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
      },
      chtml: {
        scale: 0.95
      }
    };
    </script>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js" id="MathJax-script" async></script>
        """

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{doc_title}</title>
    {math_script}
    <style>
        @page {{
            size: letter;
            margin: 18mm 16mm 18mm 16mm;
            @bottom-right {{
                content: counter(page);
            }}
        }}
        * {{
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Times New Roman', Times, serif;
            font-size: 9.5pt;
            line-height: 1.40;
            color: #111111;
            margin: 0;
            padding: 0;
        }}
        .doc-page {{
            page-break-after: always;
            break-after: page;
            clear: both;
        }}
        .doc-page:last-child {{
            page-break-after: auto;
            break-after: auto;
        }}
        .cover-page {{
            padding-top: 36pt;
            text-align: center;
        }}
        .cover-page h1 {{
            font-size: 18pt;
            color: #0d1b2a;
            margin-bottom: 6pt;
            line-height: 1.25;
            text-align: center;
            font-weight: bold;
        }}
        .cover-page h2 {{
            font-size: 12pt;
            color: #1d3557;
            border-bottom: 2px solid #1d3557;
            padding-bottom: 6pt;
            margin-bottom: 22pt;
            text-align: center;
            font-weight: normal;
            text-transform: none;
            letter-spacing: normal;
        }}
        .cover-page p {{
            font-size: 10pt;
            line-height: 1.6;
            margin: 6pt 0;
            text-align: left;
            padding: 0 16pt;
        }}
        h2 {{
            font-size: 11.5pt;
            border-bottom: 1.5px solid #1d3557;
            padding-bottom: 2pt;
            margin-top: 0;
            margin-bottom: 8pt;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: #1d3557;
            page-break-after: avoid;
        }}
        h3 {{
            font-size: 10.5pt;
            font-weight: bold;
            margin-top: 0;
            margin-bottom: 6pt;
            color: #0d1b2a;
            page-break-after: avoid;
        }}
        h4 {{
            font-size: 9.5pt;
            font-weight: bold;
            margin-top: 6pt;
            margin-bottom: 3pt;
            color: #2b2d42;
            page-break-after: avoid;
        }}
        p {{
            margin-top: 0;
            margin-bottom: 5pt;
            text-align: justify;
        }}
        ul, ol {{
            margin-top: 0;
            margin-bottom: 5pt;
            padding-left: 18pt;
        }}
        li {{
            margin-bottom: 2.5pt;
            text-align: justify;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 8pt 0;
            font-size: 8pt;
            page-break-inside: avoid;
            table-layout: fixed;
        }}
        th, td {{
            border: 1px solid #cbd5e1;
            padding: 4.5pt 6pt;
            text-align: left;
            vertical-align: top;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }}
        th {{
            background-color: #f1f4f8;
            font-weight: bold;
            color: #1d3557;
            border-bottom: 2px solid #1d3557;
        }}
        tr:nth-child(even) {{
            background-color: #f8fafc;
        }}
        pre {{
            background-color: #f8fafc;
            border: 1px solid #cbd5e1;
            border-left: 3.5px solid #1d3557;
            padding: 5pt 7pt;
            font-family: 'Consolas', 'Courier New', Courier, monospace;
            font-size: 6.8pt;
            line-height: 1.30;
            overflow-x: hidden;
            white-space: pre-wrap;
            word-break: break-all;
            margin: 6pt 0;
            page-break-inside: avoid;
        }}
        code {{
            font-family: 'Consolas', 'Courier New', Courier, monospace;
            font-size: 7.5pt;
            background-color: #f0f2f5;
            padding: 1pt 3pt;
            border-radius: 2pt;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        blockquote {{
            border-left: 3.5px solid #2a9d8f;
            margin: 8pt 0;
            padding: 5pt 10pt;
            background-color: #f4fbf9;
            font-style: italic;
            page-break-inside: avoid;
        }}
        blockquote p {{
            margin: 0;
        }}
        .figure-container {{
            text-align: center;
            margin: 6pt auto 8pt auto;
            page-break-inside: avoid;
        }}
        .fig-desktop {{
            max-width: 90%;
            max-height: 235px;
            width: auto;
            height: auto;
            object-fit: contain;
            border: 1px solid #cbd5e1;
            border-radius: 3px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            display: block;
            margin: 0 auto;
        }}
        .fig-mobile {{
            max-width: 50%;
            max-height: 295px;
            width: auto;
            height: auto;
            object-fit: contain;
            border: 1px solid #cbd5e1;
            border-radius: 3px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.12);
            display: block;
            margin: 0 auto;
        }}
        .figure-caption {{
            font-size: 8pt;
            color: #4b5563;
            margin-top: 3pt;
            font-style: italic;
            text-align: center;
        }}
    </style>
</head>
<body>
{body_html}
</body>
</html>
"""


def generate_perfect_pdf(
    md_path: Optional[str] = None,
    pdf_path: Optional[str] = None,
    header_subtitle: Optional[str] = None,
) -> str:
    """Genera un archivo PDF con alineación estricta de páginas a partir de Markdown.

    Args:
        md_path (Optional[str]): Ruta al archivo Markdown de entrada.
        pdf_path (Optional[str]): Ruta de destino para el archivo PDF.
        header_subtitle (Optional[str]): Texto de cabecera superior personalizado.

    Returns:
        str: Ruta absoluta al archivo PDF generado.

    Raises:
        FileNotFoundError: Si el archivo Markdown de entrada no existe.
    """
    if not md_path:
        raise FileNotFoundError("Debe proporcionar la ruta a un archivo Markdown (.md).")

    if not os.path.exists(md_path):
        raise FileNotFoundError(f"No se encontró el archivo especificado: {md_path}")

    if not pdf_path:
        base_name = os.path.splitext(md_path)[0]
        pdf_path = f"{base_name}.pdf"

    html_path = f"{os.path.splitext(pdf_path)[0]}.html"

    with open(md_path, "r", encoding="utf-8") as f_in:
        raw_content = f_in.read()

    sanitized = sanitize_markdown_content(raw_content)
    has_math = ("$" in sanitized or "\\(" in sanitized)

    base_dir = os.path.dirname(os.path.abspath(md_path))
    content_with_images = embed_local_images_as_base64(sanitized, base_dir)

    md_parser = markdown_it.MarkdownIt("gfm-like")
    body_html = paginate_sections_to_html(content_with_images, md_parser)

    doc_title = extract_title_from_markdown(sanitized)
    full_html = build_full_html_document(body_html, doc_title, has_math=has_math)

    with open(html_path, "w", encoding="utf-8") as f_html:
        f_html.write(full_html)
    print(f"HTML generado en: {html_path}")

    header_text = header_subtitle if header_subtitle else doc_title
    if len(header_text) > 90:
        header_text = header_text[:87] + "..."

    header_html = (
        f'<div style="font-size: 7.5pt; font-family: \'Times New Roman\'; color: #666; '
        f'width: 100%; text-align: center; border-bottom: 0.5px solid #ddd; padding-bottom: 2mm;">'
        f'{header_text}'
        f'</div>'
    )
    footer_html = (
        '<div style="font-size: 7.5pt; font-family: \'Times New Roman\'; color: #666; '
        'width: 100%; border-top: 0.5px solid #ddd; padding-top: 2mm; padding-left: 16mm; '
        'padding-right: 16mm; box-sizing: border-box;">'
        '<span style="float: left;">Doc-Guardian · Informe Técnico y Documentación</span>'
        '<span style="float: right;">Página <span class="pageNumber"></span> de <span class="totalPages"></span></span>'
        '</div>'
    )

    print("Renderizando PDF editorial mediante Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"file:///{os.path.abspath(html_path).replace(os.sep, '/')}")
        page.wait_for_timeout(4500 if has_math else 1000)

        page.pdf(
            path=pdf_path,
            format="Letter",
            print_background=True,
            margin={
                "top": "18mm",
                "bottom": "18mm",
                "left": "16mm",
                "right": "16mm",
            },
            display_header_footer=True,
            header_template=header_html,
            footer_template=footer_html,
        )
        browser.close()

    print(f"PDF generado exitosamente en: {pdf_path}")
    print(f"Tamaño: {os.path.getsize(pdf_path)} bytes")
    return pdf_path


def parse_arguments() -> Tuple[Optional[str], Optional[str]]:
    """Parsea los argumentos de línea de comandos.

    Returns:
        Tuple[Optional[str], Optional[str]]: Tupla con (md_path, pdf_path).
    """
    parser = argparse.ArgumentParser(
        description="Doc-Guardian: Generador editorial de PDFs con paginación estricta y Playwright."
    )
    parser.add_argument(
        "markdown_file",
        nargs="?",
        default=None,
        help="Ruta al archivo Markdown (.md) a convertir.",
    )
    parser.add_argument(
        "output_pdf",
        nargs="?",
        default=None,
        help="Ruta al archivo PDF (.pdf) de salida.",
    )
    args = parser.parse_args()
    return args.markdown_file, args.output_pdf


if __name__ == "__main__":
    cli_md, cli_pdf = parse_arguments()
    try:
        generate_perfect_pdf(cli_md, cli_pdf)
    except FileNotFoundError as err:
        print(f"Error: {err}", file=sys.stderr)
        sys.exit(1)
