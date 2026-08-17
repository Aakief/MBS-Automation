
from reportlab.lib.units import mm
from reportlab.platypus import Spacer, Table, TableStyle
from reportlab.lib import colors

from utils import money, section_header, boxed_notice, note_box
from statement_templates.saccawu.styles import BLACK, LIGHT_GREEN, CONTENT_W


def build(context, reporting_dt, P):
    
    full_date = reporting_dt.strftime("%d %B %Y")
    short_date = reporting_dt.strftime("%b %Y")

    table_width = 180 * mm

    portfolio_table = Table(
        [
            [
                P("PORTFOLIO<br/>","TinyBold"),
                P("GROWTH<br/>PORTFOLIO","TinyBold"),
                P("MODERATE<br/>PORTFOLIO","TinyBold"),
                P("CONSERVATIVE<br/>PORTFOLIO","TinyBold"),
                P(f"TRADING FUND<br/><font size='7'>(contributions received in {short_date} not invested yet)</font>", "TinyBold"),          
                P("ACCUMULATED<br/>CREDIT","TinyBold")
            ],
            [
                P("Amount per Portfolio","Tiny"),
                P(money(context.investments.portfolio.growth), "TinyRight"),
                P(money(context.investments.portfolio.moderate), "TinyRight"),
                P(money(context.investments.portfolio.conservative), "TinyRight"),
                P(money(context.investments.portfolio.trading_fund), "TinyRight"),          
                P(money(context.investments.portfolio.accumulated_credit), "TinyRight")
            ]
        ],
        colWidths = [
            table_width * 0.167,
            table_width * 0.167,
            table_width * 0.167,
            table_width * 0.167,
            table_width * 0.167,
            table_width * 0.167
        ]
    )
    
    portfolio_table.setStyle(TableStyle([
            ("GRID",(0,0),(-1,-1),0.5,BLACK),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("ALIGN",(1,0),(-1,-1),"CENTER"),
    ]))
    
    member = Table(
        [
            [
                "",
                P("VESTED POT", "TinyBoldCenter"),
                "",
                P("SAVINGS<br/>POT", "TinyBoldCenter"),
                P("RETIREMENT<br/>POT", "TinyBoldCenter")
            ],
            [
                "",
                P("PROVIDENT FUND", "TinyBoldCenter"),
                P("PENSION FUND", "TinyBoldCenter"),
                "",
                ""
            ],
            [
                P("Accumulated Credit", "Tiny"),
                P(money(context.investments.two_pot.vested_provident), "TinyRight"),
                P(money(context.investments.two_pot.vested_pension), "TinyRight"),
                P(money(context.investments.two_pot.savings_pot), "TinyRight"),
                P(money(context.investments.two_pot.retirement_pot), "TinyRight")
            ]
        ],
        colWidths=[
            table_width * 0.24,   # Description
            table_width * 0.19,   # Provident
            table_width * 0.19,   # Pension
            table_width * 0.19,   # Savings
            table_width * 0.19    # Retirement
        ],
        rowHeights=[
            7 * mm,
            7 * mm,
            8 * mm
        ],
        hAlign="CENTER"
    )
    
    member.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.45, BLACK),
        # Merge VESTED POT
        ("SPAN", (1,0), (2,0)),
        # Merge left blank cell
        ("SPAN", (0,0), (0,1)),
        # Savings Pot spans two rows
        ("SPAN", (3,0), (3,1)),
        # Retirement Pot spans two rows
        ("SPAN", (4,0), (4,1)),
        ("BACKGROUND", (0,0), (-1,1), colors.whitesmoke),
        ("FONTNAME", (0,0), (-1,1), "Helvetica-Bold"),
        ("ALIGN", (0,0), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    
    ]))
    
    returns_width = 180 * mm
    
    returns_table = Table(
        [
            [
                "Portfolio",
                "Growth",
                "Moderate",
                "Conservative"
            ],
            [
                P("Return 1 year","Tiny"),
                P("22.7%","Tiny"),
                P("18.4%","Tiny"),
                P("10.0%","Tiny")
            ],
            [
                P("Target","Tiny"),
                P("CPI +4.5% over 3-year<br/>rolling periods", "Tiny"),
                P("CPI +3% over 3-year<br/>rolling periods", "Tiny"),
                P("CPI +1% over 3-year<br/>rolling periods", "Tiny")
            ]
        ],
        colWidths=[
            returns_width * 0.18,
            returns_width * 0.27,
            returns_width * 0.27,
            returns_width * 0.28
        ]
    )
    
    returns_table.setStyle(TableStyle([
    ("GRID",(0,0),(-1,-1),0.5,BLACK),
    ("BACKGROUND",(0,0),(-1,0),BLACK),
    ("TEXTCOLOR",(0,0),(-1,0),colors.white),
    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
    ]))
    
    return [
        section_header(P("INVESTMENT STRATEGY","SectionWhite"), width=table_width, bg_col=BLACK,box_col=BLACK),
        note_box(P(
            "The number of years that you have until your normal retirement age determines where your Accumulated Credit is invested. " \
            f"Based on the Lifestage Investment Strategy and the number of years you have until your normal retirement age, your Accumulated Credit as at {full_date} is invested in the following portfolios",
            "BodySmall"
        ), width=table_width, box_col=BLACK),

        Spacer(1,4 *mm),
    
        portfolio_table,
    
        Spacer(1, 4* mm),
    
        P(f"The gross portfolio returns as at {full_date} are:", "BodySmall"),
    
        returns_table,
    
        Spacer(1, 8*mm),

        P("Depending on where in the Lifestage you are, your return will be different. Please note that you could be invested in a mix of portfolios given the phasing as one approaches "
            "retirement. As you are member of a defined contribution fund, you carry the risk of investment performance, i.e. your retirement savings can be impacted by positive or "
            "negative investment returns. Should there be a decline in the value of the assets underlying the Fund’s investments, the Management Board may, in terms of the Rules, "
            "declare a negative fund interest rate in which case your benefits will be reduced accordingly. For more information on the investment strategy and returns, contact the Fund "
            "Office.", "BodySmall"),

        Spacer(1, 8*mm),
    
        section_header(P("YOUR TOTAL RETIREMENT SAVINGS = VESTED POT + SAVINGS POT + RETIREMENT POT", "SectionWhite"), width=table_width, bg_col=BLACK,box_col=BLACK),
        
        member,
        Spacer(1, 6 * mm),
        P("<b>Please note:</b>", "BodySmall"),
        P(
            "The Savings Pot includes a once-off transfer from your retirement "
            "savings balance as of 31 August 2024 (applicable to eligible members).",
            "BodySmall"
        ),
        Spacer(1, 6 * mm),
        P(
            "For your latest retirement savings balance, "
            "refer to your <b>Statement of Benefits</b> via WhatsApp 0860 933 333 or the Member Web (on Old Mutual Secure Services at " \
            "<font color='blue'><u>https://secure.oldmutual.co.za</u></font>).",
            "BodySmall"
        ),
        Spacer(1, 6 * mm),
    
        P(
            "When you retire, your Retirement Savings need to provide you with a monthly income for the rest of your life. Make sure that you are on track to meet your retirement income goals. " \
            "Start planning today by contacting a Retirement Benefits Counsellor (RBC) for guidance, information and quotations by calling 021 503 0069. "
            "or booking a session via the Fund WhatsApp 072 833 2333. Alternatively, contact your personal financial adviser.",
            "BodySmall"
        ),
        Spacer(1, 7 * mm),
        boxed_notice(
            text=P("WE STRONGLY ENCOURAGE YOU TO CONSULT A TRUSTED ACCREDITED FINANCIAL ADVISER TO PLAN FOR YOUR RETIREMENT", "TinyBold"), 
            width=CONTENT_W,
            fillColor=LIGHT_GREEN,
            strokeColor=LIGHT_GREEN,
            boxColor=LIGHT_GREEN,
            icon=True
        )
    ]