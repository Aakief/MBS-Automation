from reportlab.lib.units import mm
from reportlab.platypus import Spacer, Table, TableStyle

from statement_templates.saccawu.styles import BLACK, CONTENT_W

def build(P):
    
    fund = P("<b>FUND DETAILS</b><br/>Principal Officer<br/>Mbusi Manyoni: <font color='blue'><u>mbusi@snpf.co.za</u></font><br/><br/>Fund Office<br/>Telephone: 011 463 - 5337<br/>Facsimile: 011 706 - 6243"
    "<br/>E-Mail: <font color='blue'><u>info@snpf.co.za</u></font><br/><br/>Fund Registration with Financial Sector Conduct Authority:"
    "<br/>12/8/31217/1<br/><br/>Registered address of the Fund:<br/>The Braes, First Floor<br/>Moraine House<br/>193 Bryanston Drive<br/>Bryanston, 2191<br/>", "BodySmall")

    admin = P("<b>FUND ADMINISTRATOR DETAILS</b><br/>Old Mutual Service Centre:<br/>0860 45 54 55 or 0860 20 30 40<br/><br/>" \
    "General Queries:<br/><font color='blue'><u>umbrellastandalone@oldmutual.com</u></font><br/><br/>Claims:<br/><font color='blue'><u>" \
    "CASclaims@oldmutual.com</u></font><br/><br/>Complaints:<br/><font color='blue'><u>membercomplaints@oldmutual.com</u></font><br/><br/>" \
    "Administrator address:<br/>Mutualpark,<br/>Jan Smuts Avenue,<br/>Pinelands, 7405", "BodySmall")
    
    details = Table(
        [[fund, admin]], 
        colWidths=[CONTENT_W/2, CONTENT_W/2], 
        rowHeights=[95*mm]
    )
    
    details.setStyle(
        TableStyle([
            ("GRID",(0,0),(-1,-1),0.45,BLACK),
            ("VALIGN",(0,0),(-1,-1),"TOP"),
            ("LEFTPADDING",(0,0),(-1,-1),8),
            ("TOPPADDING",(0,0),(-1,-1),6)
        ]))
    
    pfa = Table([
        [P("<b>Tel:</b> 086 066 2837 / 012 748 4000", "BodySmall"), 
         P("<b>Fax:</b> 086 693 7472", "BodySmall")], 
        [P("<b>Postal address:</b><br/>PO Box 580, MENLYN, 0063", "BodySmall"), 
         P("<b>Email:</b><font color='blue'><u>enquiries@pfa.org.za</u></font><br/><b>Web:</b><font color='blue'><u>www.pfa.org.za</u></font>", "BodySmall")]
        ], 
        colWidths=[CONTENT_W/2, CONTENT_W/2], 
        rowHeights=[12*mm,18*mm]
    )
    
    pfa.setStyle(
        TableStyle([
            ("GRID",(0,0),(-1,-1),0.45,BLACK),
            ("VALIGN",(0,0),(-1,-1),"TOP")
        ]))
    
    return [
        P("CONTACT DETAILS & COMPLAINTS", "Bold"), 
        Spacer(1,8*mm), 
        P("If you need to contact the Fund or are dissatisfied with any aspect of the Fund, please contact the Fund Office or the Fund Administrator.", "BodySmall"), 
        Spacer(1,8*mm), 
        details, 
        Spacer(1,5*mm), 
        P("You have the right to receive a reply within 30 days of your complaint being received. " \
        "If you remain dissatisfied, you may lodge your complaint with the Pension Funds Adjudicator.", "BodySmall"), 
        Spacer(1,9*mm), 
        P("PENSION FUNDS ADJUDICATOR DETAILS", "Bold"), 
        Spacer(1,5*mm), 
        pfa, 
        Spacer(1,12*mm), 
        P("COMPLIANCE WITH THE PROTECTION OF PERSONAL INFORMATION ACT (POPIA)", "Bold"), 
        Spacer(1,7*mm), 
        P("Contact the Fund Office for particulars of the Fund’s privacy policy.<br/><br/>" \
          "To view Old Mutual’s full Privacy Policy, visit: <font color='blue'><u>Customer Privacy Notice | Old Mutual</u></font><br/><br/>You also have the right to complain to the Information Regulator:<br/>Website: <font color='blue'><u>https://inforegulator.org.za/</u></font><br/>" \
          "Complaints email: <font color='blue'><u>POPIAComplaints@inforegulator.org.za</u></font><br/>General enquiries: 010 023 5200 or <font color='blue'><u>enquiries@inforegulator.org.za</u></font>", "BodySmall")
    ]
