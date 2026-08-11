from models import Salary

def build_salary(mbs_data) -> Salary:
    
    # Take the latest member information
    latest_mbs_data = mbs_data.loc[mbs_data["pyrl_dt"].idxmax()]
    
    return Salary (
        
        pensionable_salary = (
            latest_mbs_data["ann_salar"] 
            if not latest_mbs_data.empty else 0
        ),
        
        annual_risk_salary = (
            latest_mbs_data["ann_risk"] 
            if not latest_mbs_data.empty else 0                           
        ),
        
        member_contribution_rate = (
            latest_mbs_data["ee_perc"] 
            if not latest_mbs_data.empty else 0
        ),
        
        employer_contribution_rate = (
            latest_mbs_data["er_perc"] 
            if not latest_mbs_data.empty else 0
        )
    )