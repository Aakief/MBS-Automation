from utils import total
from models import InvestmentSummary, InvestmentPortfolio, TwoPotInvestment

def build_investment(mbs_data) -> InvestmentSummary:
    
    # Take the latest member information
    latest_mbs_data = mbs_data.loc[mbs_data["reporting_dt"].idxmax()]
    
    return InvestmentSummary (
        portfolio = InvestmentPortfolio (
            growth = total(latest_mbs_data, "growth"),   
            moderate = total(latest_mbs_data, "moderate"),       
            conservative = total(latest_mbs_data, "conservative"),      
            accumulated_credit = total(latest_mbs_data, "total_rbal")       
        ),
        
        two_pot = TwoPotInvestment (
            vested_provident = total(latest_mbs_data, "tlaa_prov_bal"),
            vested_pension = total(latest_mbs_data, "vested_pot_bal"),
            savings_pot = total(latest_mbs_data, "savings_pot_bal"),
            retirement_pot = total(latest_mbs_data, "retirement_pot_bal")     
        )
    )