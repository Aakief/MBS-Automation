from builders.statement_builder import build_statement_context
from utils import image_to_buffer, create_paragraph_factory
from statement_templates.saccawu.styles import style, MARGIN_X, MARGIN_TOP, MARGIN_BOTTOM

from statement_templates.saccawu.pages import (
    cover_letter,
    member_details,
    contributions,
    investments,
    benefits,
    member_services,
    contact_details)

# ReportLab imports
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, PageBreak

P = create_paragraph_factory(style())

def draw_cover_letter_header(c, doc, old_mutual_header):
    c.saveState() 
    page_width = doc.pagesize[0]
    page_height = doc.pagesize[1]
    header = ImageReader(image_to_buffer(old_mutual_header))
    header_height = 26 * mm 
    c.drawImage(
        header,
        0,
        page_height - header_height,
        width=page_width,
        height=header_height,
        preserveAspectRatio=True,
        mask='auto'
    )
    c.restoreState()

def generate_statement(member_data, contributions_data, investment_data, output_path, old_mutual_header, logo, reporting_dt, start_dt):
    
    context = build_statement_context(
        member_data,
        contributions_data,
        investment_data
    )
    
    story = []
    pages = [
        cover_letter.build(reporting_dt, P),
        member_details.build(context, logo, reporting_dt, P),
        contributions.build(context, reporting_dt, start_dt, P),
        investments.build(context, reporting_dt, P),
        benefits.build(context, reporting_dt, P),
        member_services.build(P),
        contact_details.build(P)
    ]

    for i, page in enumerate(pages):
        story.extend(page)
        
        if i != len(pages) - 1:
            story.append(PageBreak())

    doc = SimpleDocTemplate(str(output_path), 
                            pagesize=A4, 
                            rightMargin=MARGIN_X, 
                            leftMargin=MARGIN_X, 
                            topMargin=MARGIN_TOP, 
                            bottomMargin=MARGIN_BOTTOM
                        )

    def on_page(c, d):
            # Apply the banner only to page 1. Other pages stay clean like the source layout.
            if d.page == 1:
                draw_cover_letter_header(c, d, old_mutual_header)
    
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
