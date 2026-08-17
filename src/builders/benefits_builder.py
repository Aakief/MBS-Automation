from models import BenefitOverview

def build_benefits(investments, salary) -> BenefitOverview: 

        accumulated_credit = investments.portfolio.accumulated_credit
        employer_benefit = 0
        death_benefit = 4 * salary.annual_risk_salary

        return BenefitOverview (
            accumulated_credit = accumulated_credit,
            employer_benefit = employer_benefit,
            death_benefit = death_benefit,
            disability_benefit = 0.75 * salary.annual_risk_salary,
            spouse_assurance = 1 *  salary.annual_risk_salary,
            resignation_total = accumulated_credit + employer_benefit,
            retirement_total = accumulated_credit + employer_benefit,
            death_total = accumulated_credit + death_benefit + employer_benefit
        )