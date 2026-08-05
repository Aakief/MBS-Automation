# statement_builder.py

from .member_builder import build_member
from .salary_builder import build_salary
from .investment_builder import build_investment
from .benefits_builder import build_benefits
from .transactions_builder import build_contributions_history, build_transaction_summary
from models import StatementContext

def build_statement_context(member_data, transactions_data, tp_investment_data) -> StatementContext:

    contributions_history = build_contributions_history(transactions_data)
    investments = build_investment(tp_investment_data)
    salary = build_salary(transactions_data)

    return StatementContext (

        member = build_member(member_data),

        salary = salary,

        contributions = contributions_history,
            
        transactions = build_transaction_summary(
                        transactions_data, 
                        tp_investment_data, 
                        contributions_history.totals.retirement_funding
                        ),    

        investments = investments,
        
        benefits = build_benefits(investments, salary)
    )