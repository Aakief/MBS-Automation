
from reportlab.lib.units import mm
from reportlab.platypus import Spacer, Table, TableStyle
from reportlab.lib import colors

from utils import money, section_header
from statement_templates.saccawu.styles import BLACK

def build(context, reporting_dt, start_dt, P):

    short_date = reporting_dt.strftime("%B %Y")
    full_date = reporting_dt.strftime("%d %B %Y")
    
    rows = [[
        P("Details", "TinyBold"),
        P("Date Paid", "TinyBold"),
        P("Member", "TinyBold"),
        P("Employer", "TinyBold"),
        P("Member Voluntary", "TinyBold"),
        ""
    ]]

    rows.append([
        P("Contributions paid to Fund:", "Tiny"),
        "", "", "", "", ""
    ])
    
    for contribution in sorted(
        context.contributions.history, key=lambda x:x.month_no):

            rows.append([
                P(f"&nbsp;&nbsp;&nbsp;&nbsp;Month {contribution.month}", "Tiny"),
                P(contribution.payment_date, "TinyRight"),
                P(money(contribution.member), "TinyRight"),
                P(money(contribution.employer), "TinyRight"),
                P(money(contribution.voluntary), "TinyRight"),
                "",
    ])
    
    rows += [[
        "",
        "",
        P(money(context.contributions.totals.member), "TinyRight"),
        P(money(context.contributions.totals.employer), "TinyRight"),
        P(money(context.contributions.totals.voluntary), "TinyRight"),
        P(money(context.contributions.totals.grand_total), "TinyRight")
    ],
                
    [P("Adjusting Transactions for the year:", "Tiny"), "", "", "", "", ""]]
    
    for _ in range(1, 2):
        rows.append([
            P(f""),
            P(""),
            P(""),
            P(""),
            P(""),
            ""])

    rows += [
        [P("Total Adjusting Transactions", "Tiny"), "", "", "", "", P(money(context.contributions.totals.adjusting_transactions), "TinyRight")],
        [P("Less Insurance Premiums & Administration Fees:", "Tiny"), "", "", P(money(context.contributions.totals.admin_fee, negative=True), "TinyRight"), "", P(money(context.contributions.totals.admin_fee, negative=True), "TinyRight")],
        [P("Contributions to Retirement Funding", "Tiny"), "", 
         P(f"<b>{money(context.contributions.totals.member_contributions)}</b>", "TinyRight"), 
         P(f"<b>{money(context.contributions.totals.employer_contributions)}</b>", "TinyRight"), 
         P(f"<b>{money(context.contributions.totals.voluntary)}</b>", "TinyRight"), 
         P(f"<b>{money(context.contributions.totals.retirement_funding)}</b>", "TinyRight")]
        ]
    
    details_width = 170 * mm
    cont = Table(
        rows,
        colWidths=[
            details_width * 0.28,
            details_width * 0.16,
            details_width * 0.14,
            details_width * 0.14,
            details_width * 0.18,
            details_width * 0.10],
        rowHeights=[6.4 * mm] * len(rows),
        hAlign="CENTER")
    
    cont.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.35, BLACK),
        ("BACKGROUND", (0, 0), (-1, 0), colors.white),
        ("TEXTCOLOR", (0, 0), (-1, 0), BLACK),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 1.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5),
        ]))
    
    rows = [
        [P(f"Opening Balance {start_dt.strftime("%d/%m/%Y")}", "Tiny"), P(money(context.transactions.opening_balance), "TinyRight")],

        [P("Plus:", "Tiny"), ""],
        [P("&nbsp;&nbsp;&nbsp;&nbsp; Contributions to Retirement Funding", "Tiny"), P(money(context.transactions.total_contributions), "TinyRight")],
        [P("&nbsp;&nbsp;&nbsp;&nbsp; Transfer Value In (Approved Fund – S14, voluntary transfer-in)", "Tiny"), P(money(context.transactions.transfer_in), "TinyRight")],
        [P("&nbsp;&nbsp;&nbsp;&nbsp; Transfer Value In (Internal)", "Tiny"), P(money(context.transactions.internal_transfer), "TinyRight")],
        
        [P("Less:", "Tiny"), ""],
        [P("&nbsp;&nbsp;&nbsp;&nbsp; Court Order/Divorce Order", "Tiny"), P(money(context.transactions.court_divorce, negative=True), "TinyRight")],
        [P("&nbsp;&nbsp;&nbsp;&nbsp; Savings Pot Withdrawal", "Tiny"), P(money(context.transactions.spot_withdrawals, negative=True), "TinyRight")],
        
        [P("Plus:", "Tiny"), ""],
        [P("&nbsp;&nbsp;&nbsp;&nbsp; Investment Returns", "Tiny"), P(money(context.transactions.investment_returns), "TinyRight")],
        
        [P(f"Accumulated Credit {reporting_dt.strftime("%d/%m/%Y")}", "TinyBold"),P(f"<b>{money(context.transactions.accumulated_credit)}</b>", "TinyRight")]       
    ]
    
    acc = Table(
        rows,
        colWidths=[details_width * 0.78, details_width * 0.22],
        rowHeights=[7 * mm] * len(rows),
        hAlign="CENTER"
    )
    
    acc.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.45, BLACK),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),]))
    
    return [
        section_header(P(f"CONTRIBUTIONS FOR THE PERIOD {start_dt.strftime("%d/%m/%Y")} TO {reporting_dt.strftime("%d/%m/%Y")}", "SectionWhite"), width=details_width,bg_col=BLACK,box_col=BLACK),
        cont,
        Spacer(1, 5 * mm),
        P(f"<br/><b><i>Please note that the {short_date} contributions may not be included in the Accumulated Credit, "
        f"if the contributions were not received and allocated prior to {full_date}.</i></b>", "BodySmall"),
        Spacer(1, 14 * mm),
        section_header(P(f"ACCOUNT TRANSACTIONS {start_dt.strftime("%d/%m/%Y")} - {reporting_dt.strftime("%d/%m/%Y")}", "SectionWhite"), width=details_width,bg_col=BLACK,box_col=BLACK),
        acc
    ]