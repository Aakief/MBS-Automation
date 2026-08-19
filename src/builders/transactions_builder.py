import pandas as pd
from utils import total
from models import ContributionHistory, ContributionTotals, ContributionMonth, TransactionSummary

def build_contributions_history(mbs_data) -> ContributionHistory:

    if mbs_data is None or mbs_data.empty:
        return ContributionHistory (
            history = [],
            totals = ContributionTotals (
                member = 0,
                employer = 0,
                voluntary = 0,
                grand_total = 0,
                admin_fee = 0,
                member_contributions = 0,
                employer_contributions = 0,
                retirement_funding = 0,
                adjusting_transactions = 0
            )
        )

    history = []

    total_member = 0
    total_employer = 0
    total_voluntary = 0
    total_admin_fee = 0

    for _, row in mbs_data.iterrows():

        payroll_date = pd.to_datetime(row["reporting_dt"])

        member_amount = row["ee_contribs"]
        employer_amount = row["er_contribs"]
        voluntary_amount = row["member_voluntary"]
        admin_fee = row["admin_fee"]

        total_member += member_amount
        total_employer += employer_amount
        total_voluntary += voluntary_amount
        total_admin_fee += admin_fee

        history.append(
            ContributionMonth (
                month = payroll_date.strftime("%b-%y"),
                month_no = payroll_date.strftime("%m"),
                payment_date = payroll_date.strftime("%d/%m/%Y"),
                member = member_amount,
                employer = employer_amount,
                voluntary = voluntary_amount,
                admin_fee = admin_fee
            )
        )

    total_member_contributions = total_member
    total_employer_contributions = total_employer - total_admin_fee

    retirement_funding = (
        total_member_contributions
        + total_employer_contributions
        + total_voluntary
    )

    grand_total = (
        total_member
        + total_employer
        + total_voluntary
    )

    return ContributionHistory (
        history = history,
        totals = ContributionTotals (
            member = total_member,
            employer = total_employer,
            voluntary = total_voluntary,
            grand_total = grand_total,
            admin_fee = total_admin_fee,
            member_contributions = total_member_contributions,
            employer_contributions = total_employer_contributions,
            retirement_funding = retirement_funding,
            adjusting_transactions = 0
        )
    )
    
def build_transaction_summary(mbs_data, accumulated_credit, total_contributions) -> TransactionSummary:
    
    s14_trf_in = total(mbs_data, "member_s14_in")
    int_trf_in = total(mbs_data, "employer_s14_in")
    court_divorce = abs(total(mbs_data, "divore_court_order"))
    spot_withdrawals = abs(total(mbs_data, "spot_withdrawal"))
    
    # Take the latest member information
    first_mbs_data = mbs_data.loc[mbs_data["reporting_dt"].idxmin()]

    opening_balance = total(first_mbs_data, "opening_balance")
    investment_returns = accumulated_credit - opening_balance + spot_withdrawals + court_divorce - s14_trf_in - int_trf_in - total_contributions

    return TransactionSummary (
        
        opening_balance = opening_balance,
        transfer_in = s14_trf_in,
        internal_transfer = int_trf_in,
        court_divorce = court_divorce,
        spot_withdrawals = spot_withdrawals,
        investment_returns = investment_returns,  
        total_contributions = total_contributions,
        accumulated_credit = accumulated_credit
    )