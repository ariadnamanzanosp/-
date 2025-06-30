import os
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

# Rutas
DIR_TXT = "/root/codigos/bloques_txt"
DIR_PDF = os.path.join(DIR_TXT, "pdfs")
os.makedirs(DIR_PDF, exist_ok=True)

# Configuración del PDF
MARGEN_IZQ = 20 * mm
MARGEN_SUP = 20 * mm
ANCHO_PAGINA, ALTO_PAGINA = LETTER
LINE_HEIGHT = 11  # espacio entre líneas
FONT_SIZE = 9
MAX_LINE_LENGTH = 90  # menor para evitar desbordes

def wrap_text(text, max_chars):
    """Divide una línea larga en varias más cortas respetando palabras."""
    lines = []
    while len(text) > max_chars:
        wrap_pos = text.rfind(" ", 0, max_chars)
        if wrap_pos == -1:
            wrap_pos = max_chars
        lines.append(text[:wrap_pos])
        text = text[wrap_pos:].lstrip()
    lines.append(text)
    return lines

def txt_a_pdf(ruta_txt):
    nombre_base = os.path.splitext(os.path.basename(ruta_txt))[0]
    ruta_pdf = os.path.join(DIR_PDF, f"{nombre_base}.pdf")

    c = canvas.Canvas(ruta_pdf, pagesize=LETTER)
    c.setFont("Courier", FONT_SIZE)

    y = ALTO_PAGINA - MARGEN_SUP

    with open(ruta_txt, 'r', encoding='utf-8') as f:
        for linea in f:
            for sub_linea in wrap_text(linea.strip(), MAX_LINE_LENGTH):
                if y < MARGEN_SUP:
                    c.showPage()
                    c.setFont("Courier", FONT_SIZE)
                    y = ALTO_PAGINA - MARGEN_SUP
                c.drawString(MARGEN_IZQ, y, sub_linea)
                y -= LINE_HEIGHT

    c.save()
    print(f"✅ PDF generado: {ruta_pdf}")

# Procesar todos los .txt
for archivo in os.listdir(DIR_TXT):
    if archivo.endswith(".txt"):
        txt_a_pdf(os.path.join(DIR_TXT, archivo))
