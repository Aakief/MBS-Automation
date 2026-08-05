from models import Salary

def build_salary(transactions_data) -> Salary:
    
    return Salary (
        
        pensionable_salary = (
            transactions_data.sort_values("contribution_dt").iloc[-1]["ann_pen_salary"] 
            if not transactions_data.empty else 0
        ),
        
        annual_risk_salary = (
            transactions_data.sort_values("contribution_dt").iloc[-1]["ann_risk_salary"] 
            if not transactions_data.empty else 0                           
        ),
        
        member_contribution_rate = (
            transactions_data.sort_values("contribution_dt").iloc[-1]["member_contrib_rate"] 
            if not transactions_data.empty else 0
        ),
        
        employer_contribution_rate = (
            transactions_data.sort_values("contribution_dt").iloc[-1]["employer_contrib_rate"] 
            if not transactions_data.empty else 0
        )
    )