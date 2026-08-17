from reportlab.lib.units import mm
from reportlab.platypus import Spacer, Table, TableStyle

from utils import money, boxed_notice, draw_round_logo, section_header
from statement_templates.saccawu.styles import BLACK, CONTENT_W, LIGHT_GREEN

def build(context, logo_image, reporting_dt, P):
      
    member_data = [
        [P("Member Name", "TinyBold"), P(context.member.name, "Tiny"), P("Member number", "TinyBold"), P(context.member.member_number, "Tiny")],
        [P("Participating Employer", "TinyBold"), P(context.member.participating_employer, "Tiny"), P("Participating Employer Scheme", "TinyBold"), P(context.member.scheme_code, "Tiny")],
        [P("Pay point/Bill group", "TinyBold"), P(context.member.bill_group, "Tiny"), P("Payroll number", "TinyBold"), P(context.member.payroll_number, "Tiny")],
        [P("Pay centre", "TinyBold"), P(context.member.pay_centre, "Tiny"), P("Prior number", "TinyBold"), P(context.member.prior_number, "Tiny")],
        [P("Normal retirement date", "TinyBold"), P(context.member.retirement_date, "Tiny"), "", ""],
        [P("Date of birth", "TinyBold"), P(context.member.date_of_birth, "Tiny"), P("Date joining Fund", "TinyBold"), P(context.member.join_fund, "Tiny")],
        [P("SA ID or Passport number", "TinyBold"), P(context.member.id_number, "Tiny"), P("Date joining company", "TinyBold"), P(context.member.join_company, "Tiny")],
        [P("Income tax number", "TinyBold"), P(context.member.tax_number, "Tiny"), P("Client number", "TinyBold"), P(context.member.client_number, "Tiny")],
        [P("Cell phone number", "TinyBold"), P(context.member.cell_phone, "Tiny"), P("Email Address", "TinyBold"), P(context.member.email, "Tiny")],
        [P("<b>IMPORTANT:</b> Contact the <b>Old Mutual Service Centre</b> "
                       "on <b>0860 45 54 55</b> or <b>0860 20 30 40</b> if any of this information "
                       "is missing, incorrect or has changed. Your employer can also assist by updating the information on payroll",
                       "BodySmall"
                   ), "", "", ""],
    ]
    
    personal_table_width = 170 * mm

    member_table = Table(
        member_data, 
        colWidths=[personal_table_width * 0.30, personal_table_width * 0.22, personal_table_width * 0.28, personal_table_width * 0.20], 
        rowHeights=[7*mm, 13*mm, 7*mm, 7*mm, 14*mm, 7*mm, 7*mm, 7*mm, 7*mm, 13*mm],
        hAlign="CENTER"
    )
    member_table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.45, BLACK), ("FONTNAME", (0,0), (-1,-1), "Helvetica"),
        ("FONTNAME", (0,0), (0,-1), "Helvetica-Bold"), ("FONTNAME", (2,0), (2,-1), "Helvetica-Bold"),
        ("SPAN", (0,9), (-1,9)), ("ALIGN", (0,9), (-1,9), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"), ("LEFTPADDING", (0,0), (-1,-1), 3), ("RIGHTPADDING", (0,0), (-1,-1), 3),
    ]))

    salary = Table(
        [
        [P("Annual pensionable salary", "Tiny"), P(money(context.salary.pensionable_salary), "TinyRight")],
        [P("Annual risk salary", "Tiny"), P(money(context.salary.annual_risk_salary), "TinyRight")],
        [P("Monthly member contribution rate", "Tiny"), P(f"{context.salary.member_contribution_rate}%", "TinyRight")],
        [P("Monthly employer contribution rate (before risk benefit premiums and Fund expense deductions)", "Tiny"), P(f"{context.salary.employer_contribution_rate}%", "TinyRight")],
        ], 
        colWidths=[personal_table_width * 0.70, personal_table_width * 0.30], 
        rowHeights=[7*mm,7*mm,7*mm,14*mm], 
        hAlign="CENTER",
    )
    
    salary.setStyle(
        TableStyle([
            ("GRID",(0,0),(-1,-1),0.45,BLACK),
            ("ALIGN",(1,0),(1,-1),"RIGHT"),
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("LEFTPADDING",(0,0),(-1,-1),3)
            ])
        )
    
    return [draw_round_logo(logo_image, width=50*mm, height=30*mm), 
            Spacer(1, 5*mm), 
            P("SACCAWU NATIONAL PROVIDENT FUND", "PageTitle"), 
            P("Pension Funds Act Registration Number P.F. 12/8/31217/1", "SubTitle"), 
            Spacer(1, 9*mm), 
            P(f"MEMBER BENEFIT STATEMENT AS AT {reporting_dt.strftime("%d %B %Y")}", "PageTitle"), 
            Spacer(1, 9*mm), 
            section_header(P("PERSONAL INFORMATION","SectionWhite"), width=170*mm, bg_col=BLACK, box_col=BLACK), 
            member_table, 
            Spacer(1, 7*mm), 
            section_header(P("SALARY AND CONTRIBUTION RATE","SectionWhite"),width=CONTENT_W,bg_col=BLACK,box_col=BLACK), 
            salary, 
            boxed_notice(
                text=P("RETIREMENT FUND CONTRIBUTIONS ARE TAX DEDUCTIBLE UP TO 27.5% OF THE GREATER OF YOUR REMUNERATION OR TAXABLE INCOME. ANNUAL TAX DEDUCTIONS ARE LIMITED TO R350 000.","TinyBold"),
                width=CONTENT_W,
                fillColor=LIGHT_GREEN,
                strokeColor=LIGHT_GREEN,
                boxColor=LIGHT_GREEN,
                icon=True
            )
    ]