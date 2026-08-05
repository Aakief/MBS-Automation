from datetime import datetime

from reportlab.lib.units import mm
from reportlab.platypus import Spacer

def build(reporting_dt, P):
    
    current_date = datetime.now().strftime("%d/%m/%Y")
    
    body = [Spacer(1, 12 * mm)]
    body += [P("Mutualpark, Jan Smuts Drive, Pinelands, 7405. PO Box 728, Cape Town, 8000, South Africa.<br/>Member Queries: 0860 45 54 55, www.oldmutual.co.za", "Tiny")]
    body += [Spacer(1, 8 * mm), 
             P("ABC NATIONAL PROVIDENT FUND", "TitleGreen"), 
             Spacer(1, 10 * mm)]
    body += [P(current_date, "Body"), 
             Spacer(1, 10 * mm), 
             P("Dear Member", "Body"), 
             Spacer(1, 9 * mm)]
    body += [P("MEMBER BENEFIT STATEMENT", "Bold"), Spacer(1, 9 * mm)]
    paras = [
        f"On behalf of the ABC National Provident Fund (&ldquo;the Fund&rdquo;), we enclose your latest Member Benefit Statement showing the value of your Retirement Savings (accumulated credit) as at <b>{reporting_dt.strftime("%d/%m/%Y")}</b>, as well as details of the death and disability benefits.",
        "When you read your statement, you should consider the following: <i>Are my Retirement Savings enough to meet my retirement needs?</i> We recommend that you meet with a financial advisor to assist you in planning for your retirement.",
        "As a member of the Fund, you can be sure that your Retirement Savings will be managed according to the highest standards. You can also take advantage of the tools and communication available from the Old Mutual website:",
    ]
    for para in paras:
        body += [P(para, "Body"), Spacer(1, 6 * mm)]
        
    bullets = [
        "Visit our website at oldmutual.co.za where you will find useful information and a retirement calculator, which will provide you with a guideline as to whether you are on target to retire.",
        "Register for secure access to the above website if you have not done so previously. This will allow you to monitor your Retirement Savings online.<br/>To register:<br/>&nbsp;&nbsp;&bull; "
        "Click ‘Login’ at the top right corner of the oldmutual.co.za website<br/>&nbsp;&nbsp;&bull; If you already have a profile, select ‘My Portfolio’ and continue<br/>&nbsp;&nbsp;&bull; No profile? "
        "Scroll down and click ‘Register for a service’<br/>&nbsp;&nbsp;&bull; Fill in your details<br/>&nbsp;&nbsp;&bull; Then select “login details”<br/>&nbsp;&nbsp;&bull; You will receive an OTP SMS to complete registration.",
    ]
    for b in bullets:
        body += [P("&bull;&nbsp;&nbsp;" + b, "Body"), Spacer(1, 2 * mm)]

    body += [Spacer(1, 12 * mm), 
        P("Yours sincerely", "Body"), 
        Spacer(1, 12 * mm), 
        P("Phumla Yebe", "Body"), Spacer(1, 2 * mm), 
        P("Head: Corporate Administration and Servicing", "Bold")
        ]
    return body
