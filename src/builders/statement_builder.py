# statement_builder.py

from .member_builder import build_member
from .salary_builder import build_salary
from .investment_builder import build_investment
from .benefits_builder import build_benefits
from .transactions_builder import build_contributions_history, build_transaction_summary
from models import StatementContext

def build_statement_context(mbs_data) -> StatementContext:

    contributions_history = build_contributions_history(mbs_data)
    investments = build_investment(mbs_data)
    salary = build_salary(mbs_data)

    return StatementContext (

        member = build_member(mbs_data),

        salary = salary,

        contributions = contributions_history,
            
        transactions = build_transaction_summary(
                        mbs_data,
                        investments.portfolio.accumulated_credit, 
                        contributions_history.totals.retirement_funding
                        ),    

        investments = investments,
        
        benefits = build_benefits(investments, salary)
    )