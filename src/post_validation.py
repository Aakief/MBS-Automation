from pypdf import PdfReader
import difflib
import pandas as pd
from utils import normalise_text, normalise_currency_value

def extract_pdf_metadata(pdf_path):
    reader = PdfReader(pdf_path)
    page_count = len(reader.pages)
    page_texts = {}
    full_text = ""

    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        page_texts[i] = text
        full_text += text + "\n"

    word_count = len(full_text.split())

    return {
        "page_count": page_count,
        "word_count": word_count,
        "page_texts": page_texts,
        "full_text": full_text
    }

def validate_pdf_word_counts(case_mbr_key, pdf_path, expected_counts):
    reader = PdfReader(pdf_path)
    results = []

    for page_num, expected in expected_counts.items():
        text = reader.pages[page_num - 1].extract_text() or ""
        text = text.replace("\x7f", "")
        actual = len(text.split())

        results.append({
            "case_mbr_key": case_mbr_key,
            "Page": page_num,
            "Expected": expected,
            "Actual": actual,
            "Difference": actual - expected,
            "Status": "PASS" if actual == expected else "FAIL"
        })

    return results

def validate_page_count(
        case_mbr_key,
        expected_pages,
        actual_pages):

    return [{
        "case_mbr_key": case_mbr_key,
        "field_name": "Page Count",
        "expected": expected_pages,
        "found": actual_pages,
        "status": (
            "PASS"
            if expected_pages == actual_pages
            else "FAIL")}]

def validate_member_fields(case_mbr_key, member_row, pdf_text):

    pdf_text = normalise_text(pdf_text)
    results = []
    checks = [
        {"field_name": "Member Name",
        "expected": f"{member_row['firstname']} {member_row['lastname']}".strip().lower()},

        {"field_name": "Tax Number",
         "expected": str(member_row["tax_ref_no"]).lower()},

        {"field_name": "Member Number",
         "expected": str(member_row["mbr_no"]).lower()},

        {"field_name": "Plan Name",
         "expected": str(member_row["plan_nm"]).lower()},

        {"field_name": "Contract Number",
         "expected": str(member_row["cont_no"]).lower()},

        {"field_name": "Billing Group",
         "expected": str(member_row["bill_group"]).lower()},

        {"field_name": "Payroll Number",
         "expected": str(member_row["pyrl_no"]).lower()},

        {"field_name": "Prior Number",
         "expected": str(member_row["pr_mbr_no"]).lower()},

        {"field_name": "Retirement Date",
         "expected": pd.to_datetime(member_row["nrd"]).strftime("%d/%m/%Y").lower()},

        {"field_name": "Date Of Birth",
         "expected": pd.to_datetime(member_row["birthdt"]).strftime("%d/%m/%Y").lower()},

        {"field_name": "Join Fund",
         "expected": pd.to_datetime(member_row["join_scheme_dt"]).strftime("%d/%m/%Y").lower()},

        {"field_name": "Join Company",
         "expected": pd.to_datetime(member_row["join_dt"]).strftime("%d/%m/%Y").lower()},

        {"field_name": "ID Number",
         "expected": str(member_row["natlidno"]).lower()},

        {"field_name": "Client Number",
         "expected": str(member_row["nameid"]).lower()},

        {"field_name": "Cell Phone",
         "expected": str(member_row["mobilephone"]).lower()},

        {"field_name": "Email",
         "expected": str(member_row["email_addr"]).lower()}]

    for check in checks:
        expected = normalise_text(check["expected"])

        if expected in pdf_text:
            found = check["expected"]
            status = "PASS"
        else:
            found = "NOT FOUND"
            status = "FAIL"

        results.append({
            "case_mbr_key": case_mbr_key,
            "field_name": check["field_name"],
            "expected": expected,
            "found": found,
            "status": status})

    return results

def validate_salary(case_mbr_key, salary, pdf_text):
    results = []
    pdf_text = normalise_text(pdf_text)

    salary_checks = [
        ("Pensionable Salary", salary.pensionable_salary),
        ("Risk Salary", salary.annual_risk_salary),
        ("Member Contribution rate", salary.member_contribution_rate),
        ("Employer Contribution rate", salary.employer_contribution_rate)
    ]

    for field_name, expected in salary_checks:
        salary_expected = normalise_currency_value(expected)

        results.append({
            "case_mbr_key": case_mbr_key,
            "section": "Salary and Contribution",
            "field_name": field_name,
            "expected": expected,
            "found": (expected if salary_expected in pdf_text else "NOT FOUND"),
            "status": ("PASS" if salary_expected in pdf_text else "FAIL")})

    return results

def validate_contribution_history(case_mbr_key, contribution_history, transaction_summary, pdf_text):
    
    results = []
    pdf_text = normalise_text(pdf_text)

    for row_num, row in enumerate(
        contribution_history.history, start=1):

        checks = [
        ("Month", row.month),
        ("Payment Date", row.payment_date),
        ("Member", row.member),
        ("Employer", row.employer),
        ("Voluntary", row.voluntary)
        ]

        for field_name, expected in checks:
            expected_text = normalise_text(str(expected))

            results.append({
                "case_mbr_key": case_mbr_key,
                "section": "Contribution History",
                "month number": row_num,
                "field_name": field_name,
                "expected": expected,
                "found": (expected if expected_text in pdf_text else "NOT FOUND"),
                "status": ("PASS" if expected_text in pdf_text else "FAIL")})
        
    acc_checks = [
    ("Opening Balance", transaction_summary.opening_balance),
    ("Retirement", round(transaction_summary.total_contributions, 2)),
    ("Transfer-In", transaction_summary.transfer_in),
    ("Internal", transaction_summary.internal_transfer),
    ("Court-Divorce", transaction_summary.court_divorce),
    ("TwoPot withdrawal", transaction_summary.spot_withdrawals),
    ("Returns", transaction_summary.investment_returns),
    ("Accumulated credit", transaction_summary.accumulated_credit)
    ]
    
    for transaction_field_name, acc_expected in acc_checks:
        expected_acc_text = normalise_currency_value(acc_expected)

        results.append({
            "case_mbr_key": case_mbr_key,
            "section": "Account Transactions",
            "field_name": transaction_field_name,
            "expected": acc_expected,
            "found": (acc_expected if expected_acc_text in pdf_text else "NOT FOUND"),
            "status": ("PASS" if expected_acc_text in pdf_text else "FAIL")})

    admin_fee_total = contribution_history.totals.admin_fee
    admin_fee_expected = normalise_currency_value(admin_fee_total)
    admin_fee_pdf = normalise_currency_value(pdf_text)

    results.append({
    "case_mbr_key": case_mbr_key,
    "section": "Contribution Summary",
    "row_number": None,
    "field_name": "Total Admin Fee",
    "expected": admin_fee_expected,
    "found": (admin_fee_total if admin_fee_expected in admin_fee_pdf else "NOT FOUND"),
    "status": ("PASS" if admin_fee_expected in admin_fee_pdf else "FAIL")})

    return results

def validate_investment(case_mbr_key, investment_portfolio, investment_pot, pdf_text):
    results = []
    pdf_text = normalise_text(pdf_text)

    portfolio_checks = [
        ("Growth Portfolio", investment_portfolio.portfolio.growth),
        ("Moderate Portfolio", investment_portfolio.portfolio.moderate),
        ("Conservative Portfolio", investment_portfolio.portfolio.conservative),
        ("Trading Fund", investment_portfolio.portfolio.trading_fund),
        ("Accumulated Credit", investment_portfolio.portfolio.accumulated_credit)
    ]

    for field_name, portfolio_expected in portfolio_checks:
        portfolio_expected_amt = normalise_currency_value(portfolio_expected)

        results.append({
        "case_mbr_key": case_mbr_key,
        "section": "Investment Portfolios",
        "field_name": field_name,
        "expected": portfolio_expected,
        "found": (portfolio_expected if portfolio_expected_amt in pdf_text else "NOT FOUND"),
        "status": ("PASS" if portfolio_expected_amt in pdf_text else "FAIL")})

    pot_checks = [
        ("Provident Fund", investment_pot.two_pot.vested_provident),
        ("Pension Fund", investment_pot.two_pot.vested_pension),
        ("Savings Pot", investment_pot.two_pot.savings_pot),
        ("Retirement Pot", investment_pot.two_pot.retirement_pot)
    ]

    for pot_field_name, pot_expected in pot_checks:
        pot_expected_amt = normalise_currency_value(pot_expected)

        results.append({
        "case_mbr_key": case_mbr_key,
        "section": "Total Retirement Savings",
        "field_name": pot_field_name,
        "expected": pot_expected,
        "found": (pot_expected if pot_expected_amt in pdf_text else "NOT FOUND"),
        "status": ("PASS" if pot_expected_amt in pdf_text else "FAIL")})

    return results

def validate_benefits(case_mbr_key, benefits, pdf_text):
    results = []
    pdf_text = normalise_text(pdf_text)

    benefits_check = [
        ("Resignation Total", benefits.resignation_total),
        ("Retirment Total", benefits.retirement_total),
        ("Death in Service", round(benefits.death_total, 2)),
        ("Death Benefits", benefits.death_benefit),
        ("Disability Income Benefit", round(benefits.disability_benefit, 2)),
        ("Spouse's Assurance", benefits.spouse_assurance)]

    for field_name, expected in benefits_check:
        benefits_expected = normalise_currency_value(expected)

        results.append({
        "case_mbr_key": case_mbr_key,
        "section": "Benefit Overiview",
        "field_name": field_name,
        "expected": expected,
        "found": (expected if benefits_expected in pdf_text else "NOT FOUND"),
        "status": ("PASS" if benefits_expected in pdf_text else "FAIL")})

    return results