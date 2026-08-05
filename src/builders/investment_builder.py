from utils import total
from models import InvestmentSummary, InvestmentPortfolio, TwoPotInvestment

def build_investment(tp_investment_data) -> InvestmentSummary:
    
    return InvestmentSummary (
        portfolio = InvestmentPortfolio (
            growth = total(tp_investment_data, "growth"),   
            moderate = total(tp_investment_data, "moderate"),       
            conservative = total(tp_investment_data, "conservative"),        
            trading_fund = total(tp_investment_data, "trading_fund"),        
            accumulated_credit = total(tp_investment_data, "accumulated_credit")       
        ),
        
        two_pot = TwoPotInvestment (
            vested_provident = total(tp_investment_data, "tlaa_prov_bal"),
            vested_pension = total(tp_investment_data, "vested_pot_bal"),
            savings_pot = total(tp_investment_data, "savings_pot_bal"),
            retirement_pot = total(tp_investment_data, "retirement_pot_bal")     
        )
    )