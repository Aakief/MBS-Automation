from reportlab.lib.units import mm
from reportlab.platypus import Spacer, Table, TableStyle
from statement_templates.saccawu.styles import BLACK

def build(P):

    contact_details = Table(
            [
                [P("MEMBER SELF SERVICE CONTACT DETAILS:", "TinyBold")],
                [P(
                    "Members have access to the following channels provided by the Fund Administrator "
                    "to enable them to make enquiries:<br/>"
                    "1) Old Mutual Service Centre number: 0860 45 54 55 or 0860 20 30 40.<br/>"
                    "2) Old Mutual Member Support Services: "
                    "<font color='blue'>umbrellastandalone@oldmutual.com</font><br/>"
                    "3) Old Mutual Website "
                    "<font color='blue'>http://www.oldmutual.co.za/about-us/self-help-services/online-secure-services.aspx</font><br/>"
                    "4) Effective 30 September 2024, all retirement, resignation, retrenchment and "
                    "dismissals must be submitted online on the Old Mutual Website, Secure Services, "
                    "MyClaim. For assistance contact the Old Mutual Member Service Centre "
                    "0860 20 30 40.",
                    "BodySmall"
                )]
            ],
            colWidths=[170 * mm]
        )

    contact_details.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.5, BLACK),
        ("LINEBELOW", (0, 0), (0, 0), 0.5, BLACK),  # line under heading
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))

    return [
        contact_details,
        Spacer(1, 7*mm),
        P("GENERAL", "Bold"),
        Spacer(1, 3*mm),
        P("Great care has been taken to accurately prepare this Statement. The Administrator, the Management Board and other"
           "Fund office-bearers cannot accept liability for any error or omission. This Member Benefit Statement is issued for your"
          "information and the benefits stated remain subject to such specific terms and conditions in the Rules of the Fund and"
          "Risk Benefit Policies.", "BodySmall"),
        Spacer(1, 3*mm),
        P("The Rules, financial returns, and the most recent actuarial valuation report may be inspected at the registered office of"
           "the Fund. Should you require copies of these documents, contact the Fund Office (see address below).", "BodySmall"),        
        Spacer(1, 3*mm),
        P("Payment of a member's benefit in terms of the Rules will be reduced by any amount awarded to a divorced former"
           "spouse in terms of section 7(7) & 7(8) of the Divorce Act 7 of 1979, read with section 37D(4) of the Pension Funds Act"
           "24 of 1956 as amended. Your benefit may also be reduced by any amounts owing in terms of any surety provided by"
           "the Fund for housing loans, maintenance orders or any other allowed prior claims in terms of section 37D of the Pension"
           "Funds Act 24 of 1956, as amended.", "BodySmall"),        
        Spacer(1, 3*mm),
        P("Tax may be deducted from any cash benefits before they are paid, it is important that you register with the relevant tax"
          "authorities and provide your tax number to your payroll for it to be included in the data submitted to the Fund. All benefits"
          "are subject to taxation. For detailed information on the tax implications of the various benefits and benefit options,"
           "please consult your personal financial adviser. Savings Pot Withdrawals will be taxed at marginal tax rates at the time"
            "of making a withdrawal and a transaction fee is charged when you withdraw.", "BodySmall"),       
        Spacer(1, 3*mm),
        P("If you exit the Fund due to resignation, dismissal, or retrenchment and do not submit a fully completed claim notification"
          "(MyClaim), you will, after a period of three months from the date on which you became eligible for a benefit in terms of"
          "the Fund Rules, be deemed to have elected to continue your membership of the Fund as a Paid - Up Member."
          " As a Paid - Up Member, you will remain a member of the Fund and may claim your benefit at any time in the future."
          " However, you will not be covered under the Fund’s life assurance benefit policy.", "BodySmall"),        
        Spacer(1, 3*mm),
        P("Your retirement savings in other approved funds may be transferred to the Fund (consolidation of benefits) subject to"
           "what is allowed in terms of the Income Tax Act.", "BodySmall"),        
        Spacer(1, 3*mm),
        P("The Fund will provide you with ongoing communication and information about Fund related products or services that"
          "may be suitable to meet your Fund related financial needs.", "BodySmall")
    ]