from reportlab.lib.units import mm
from reportlab.platypus import Spacer, Table, TableStyle
from reportlab.lib import colors

from utils import money, section_header, boxed_notice, note_box
from statement_templates.saccawu.styles import BLACK, LIGHT_GREEN, CONTENT_W

def build(context, reporting_dt, P):
    
    table_width = 170 * mm
     
    overview = Table(
        [
            ["", "", P("Insured Risk Benefits", "TinyBold"), "", ""],
            [
                P("Event", "TinyBoldCenter"),
                P("Fund<br/>Account<br/>Balance", "TinyBoldCenter"),
                P("Fund Benefit", "TinyBoldCenter"),
                P("Employer Owned<br/>Benefit", "TinyBoldCenter"),
                P("Total Benefit Due<br/>", "TinyBoldCenter"),
            ],
            [P("Resignation,<br/>Retrenchment/Dismissal", "Tiny"), 
                P(money(context.benefits.accumulated_credit), "TinyRight"), 
                "", 
                "", 
                P(money(context.benefits.resignation_total), "TinyRight")],
            [P("Retirement", "Tiny"), 
                P(money(context.benefits.accumulated_credit), "TinyRight"), 
                "", 
                "", 
                P(money(context.benefits.retirement_total), "TinyRight")],
            [P("Death in Service", "Tiny"), 
                P(money(context.benefits.accumulated_credit), "TinyRight"), 
                P(money(context.benefits.death_benefit), "TinyRight"), 
                "", 
                P(money(context.benefits.death_total), "TinyRight")]
        ],
        colWidths=[
            table_width * 0.30,
            table_width * 0.18,
            table_width * 0.17,
            table_width * 0.17,
            table_width * 0.18,
        ],
        rowHeights=[
            6 * mm,
            10 * mm,
            10 * mm,
            7 * mm,
            7 * mm
        ],
        hAlign="CENTER",
    )
    
    overview.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.45, BLACK),
    
        ("SPAN", (2, 0), (4, 0)),
    
        ("BACKGROUND", (0, 0), (-1, 1), colors.white),
    
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ALIGN", (0, 2), (0, -1), "LEFT"),
        ("ALIGN", (1, 2), (-1, -1), "RIGHT"),
    
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    
    insured = Table(
        [
            [
                P("<b>Death Benefits</b><br/>(4 X Annual Earnings)", "BodySmall"),
                P(money(context.benefits.death_benefit), "BodySmall"),
                P(
                    "<b>Funeral Benefits</b><br/><br/>"
                    "Member<br/>"
                    "Spouse<br/>"
                    "Child 15 - 21<br/>"
                    "Child 6 - 14<br/><br/>"
                    
                    "Child 0 - 5<br/>"
                    "Stillborn",
                    "BodySmall"
                ),
                P(  "<b> </b><br/><br/>"
                    "R 50 000<br/>"
                    "R 50 000<br/>"
                    "R 25 000<br/>"
                    "R 10 500<br/><br/>"

                    "R 5 000<br/>"
                    "R 5 000",
                    "BodySmall"
                ),
            ],

            [
                P("<b>Disability Income Benefit</b> (Annual)", "BodySmall"),
                P(money(context.benefits.disability_benefit), "BodySmall"),
                "",
                "",
            ],

            [
                P("<b>Spouse Assurance</b><br/>(1 X Annual Earnings)", "BodySmall"),
                P(money(context.benefits.spouse_assurance), "BodySmall"),
                "",
                "",
            ],
        ],

        colWidths=[
            table_width * 0.36,
            table_width * 0.18,
            table_width * 0.28,
            table_width * 0.18,
        ],

        hAlign="CENTER"
    )
    
    insured.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.45, BLACK),
        ("LINEAFTER", (1, 0), (1, -1), 0.45, BLACK),
    
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))

    def death_benefit_section(death_benefit, accumulated_credit, width=170*mm):
    
        rows = [
            [P("<b>Should you die before retirement:</b>", "BodySmall"), ""],
    
            [
                P("A Life Assurance Benefit amounting to:", "BodySmall"),
                P(f"<b>R{death_benefit:,.2f}</b>", "BodySmallRight")
            ],
    
            [
                P("<b>PLUS,</b><br/>your Accumulated Credit:", "BodySmall"), #Formatting death benefits section
                P(f"<b>R{accumulated_credit:,.2f}</b>", "BodySmallRight")
            ],
    
            [
                P(
                    "will become payable to your dependants and/or nominated "
                    "beneficiaries (as determined by the Management Board). "
                    "This benefit can be paid in cash and/or used to purchase a pension.",
                    "BodySmall"
                ),
                ""
            ]
        ]
    
        tbl = Table(
            rows,
            colWidths=[width * 0.75, width * 0.25]
        )
    
        tbl.setStyle(TableStyle([
            ("SPAN", (0,0), (1,0)),
            ("SPAN", (0,3), (1,3)),
    
            ("VALIGN", (0,0), (-1,-1), "TOP"),
    
            ("LEFTPADDING", (0,0), (-1,-1), 0),
            ("RIGHTPADDING", (0,0), (-1,-1), 0),
    
            ("TOPPADDING", (0,0), (-1,-1), 4),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
    
            ("ALIGN", (1,1), (1,2), "RIGHT"),
        ]))
 
        return tbl
    
    return [
        section_header(P("BENEFIT OVERVIEW", "SectionWhite"), width=table_width,bg_col=BLACK,box_col=BLACK),
        overview,
        Spacer(1, 2 * mm),
    
        section_header(P(f"INSURED BENEFITS AT {reporting_dt.strftime("%d/%m/%Y")}", "SectionWhite"), width=table_width,bg_col=BLACK,box_col=BLACK),
        insured,
        Spacer(1, 2 * mm),
    
        section_header(P("DISABILITY INCOME BENEFIT PLAN", "SectionWhite"), width=table_width,bg_col=BLACK,box_col=BLACK),
        P("Should you, on medical grounds, become totally unable to continue working after a waiting period, you may qualify for a Disability Income benefit of 75% of your monthly salary. This is subject to the assessment by the Insurer.", "BodySmall"),
        Spacer(1, 1 * mm),

        note_box(
            P("<b><i>Please note:</i></b> "
            "<i>"
            "If a disability income benefit becomes payable to you, you remain a member "
            "of the Fund and continue to participate in all the benefits. Therefore, "
            "the percentage required to continue the Employee contributions will be "
            "deducted from the Disability Income Benefit and the remainder will be "
            "payable to you.<br/>"
            "The Employer contributions (i.e. retirement funding, risk benefit "
            "premiums and administration fees) to the Fund are covered by the "
            "insurance policy and paid on your behalf."
            "</i>", "BodySmall"),
            width=table_width, 
            box_col = BLACK
        ),
        Spacer(1, 2 * mm),
    
        section_header(P("DEATH BENEFITS", "SectionWhite"), width=table_width, bg_col=BLACK,box_col=BLACK),
        death_benefit_section(
            context.benefits.death_benefit,
            context.benefits.accumulated_credit,
            width=table_width
        ),
        Spacer(1, 2 * mm),
    
        boxed_notice(
            text=P("IT IS VERY IMPORTANT FOR YOU TO NOMINATE BENEFICIARIES AND TO KEEP YOUR NOMINATED BENEFICIARIES’ DETAILS UP TO DATE. " \
            "This will only function as a guide to the Fund when allocating your death benefit. " \
            "Please remember to update the beneficiaries at least once a year and to also identify your financial dependants," \
            " especially if your personal circumstances change i.e. marriage, divorce, birth of child, death of a beneficiary or a dependant.","TinyBold"),
            width=CONTENT_W,
            fillColor=LIGHT_GREEN,
            strokeColor=LIGHT_GREEN,
            boxColor=LIGHT_GREEN,
            icon=True
        ),
        Spacer(1, 4 * mm),
    
        P("PLEASE NOTE", "TinyBold"),
        P(  "1.<i>The disability income, spouse's assurance and family (funeral) benefits are</i> provided from separate "
            "risk policies issued by the insurer of this benefit."
            "<br/>2. As a member of the Fund, you need to make sure that the"
            "amount of cover for death and disability is right for you"
            "and your family. If you feel it may not be adequate, you may want to buy additional cover in your personal capacity."
            "Please consult an accredited financial adviser to assist you."
            "<br/>3. Your insured benefits are displayed for illustrative purposes only and are subject to the terms and conditions of the"            #formatting page 5
            "risk policy. In case of a discrepancy between this document and the Fund rules and risk policy, the Fund rules and"
            "risk policy will always prevail."
            "<br/>4. The annual earnings for calculation of risk benefit purposes will be the earnings in the month preceding (before)"
            "the date of the event, provided that it is not lower than the average earnings earned over the 12-month period prior"
            "to the date of the event."
            "<br/>5. If your risk benefit on death or disablement (where applicable) exceeds the risk provider's free cover limit for the"
            "Fund, that portion of the cover in excess of the free cover limit will be subject to meeting the risk provider's medical underwriting requirements."  ,
            "BodySmall",)
    ]