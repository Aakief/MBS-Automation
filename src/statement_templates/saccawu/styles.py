from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.lib import colors

PAGE_W, PAGE_H = A4
BLACK = colors.black
GREEN = colors.HexColor("#009B77")
LIGHT_GREEN = colors.HexColor("#8CC63E")
BLUE = colors.HexColor("#4F86C6")
GRID = colors.HexColor("#1A1A1A")

# Keep all layout numbers together so you can tune the template easily.
MARGIN_X = 20 * mm
MARGIN_TOP = 10 * mm
MARGIN_BOTTOM = 20 * mm
CONTENT_W = PAGE_W - 2 * MARGIN_X

def style():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("BodySmall", fontName="Helvetica", fontSize=8.2, leading=10.1, alignment=TA_LEFT))
    styles.add(ParagraphStyle("Body", fontName="Helvetica", fontSize=10, leading=12.5, alignment=TA_LEFT))
    styles.add(ParagraphStyle("BodyJustify", fontName="Helvetica", fontSize=10, leading=12.5, alignment=TA_JUSTIFY))
    styles.add(ParagraphStyle("Bold", fontName="Helvetica-Bold", fontSize=10, leading=12.5))
    styles.add(ParagraphStyle("TitleGreen", fontName="Helvetica-Bold", fontSize=14, leading=17, textColor=GREEN))
    styles.add(ParagraphStyle("PageTitle", fontName="Helvetica-Bold", fontSize=12, leading=15, alignment=TA_CENTER))
    styles.add(ParagraphStyle("SectionWhite", fontName="Helvetica-Bold", fontSize=8.5, leading=12, alignment=TA_CENTER, textColor=colors.white))
    styles.add(ParagraphStyle("NoteItalic", fontName="Helvetica-Oblique", fontSize=8.5, leading=10.5))
    styles.add(ParagraphStyle("Tiny", fontName="Helvetica", fontSize=7.1, leading=8.4))
    styles.add(ParagraphStyle("TinyBold", fontName="Helvetica-Bold", fontSize=7.1, leading=8.4))
    styles.add(ParagraphStyle("Link", fontName="Helvetica", fontSize=10, leading=12, textColor=colors.blue))
    styles.add(ParagraphStyle("SubTitle", fontName="Helvetica", fontSize=8.2, leading=10.1, alignment=TA_CENTER))
    styles.add(ParagraphStyle("TinyBoldCenter", parent=styles["TinyBold"], alignment=TA_CENTER))
    styles.add(
        ParagraphStyle(
            "TinyRight",
            parent=styles["Tiny"],
            alignment=TA_RIGHT,
        )
    )
    styles.add(
        ParagraphStyle(
            "BodySmallRight",
            parent=styles["BodySmall"],
            alignment=TA_RIGHT,
        )
    )
    
    return styles