from dataclasses import dataclass, field
from typing import List

# ----------------------------
# Member
# ----------------------------

@dataclass
class Member:
    name: str
    member_number: str
    participating_employer: str
    scheme_code: str
    bill_group: str
    payroll_number: str
    prior_number: str
    retirement_date: str
    date_of_birth: str
    join_fund: str
    join_company: str
    id_number: str
    tax_number: str
    client_number: str
    cell_phone: str
    email: str
    pay_centre: str

# ----------------------------
# Salary
# ----------------------------

@dataclass
class Salary:
    pensionable_salary: float
    annual_risk_salary: float
    member_contribution_rate: float
    employer_contribution_rate: float

# ----------------------------
# Contributions
# ----------------------------

@dataclass
class ContributionMonth:
    month: str
    month_no: str
    payment_date: str
    member: float
    employer: float
    voluntary: float
    admin_fee: float


@dataclass
class ContributionTotals:
    member: float
    employer: float
    voluntary: float
    grand_total: float
    admin_fee: float
    member_contributions: float
    employer_contributions: float
    retirement_funding: float
    adjusting_transactions: float
    
@dataclass
class ContributionHistory:
    history: List[ContributionMonth] = field(default_factory=list)
    totals: ContributionTotals | None = None

# ----------------------------
# Transactions
# ----------------------------

@dataclass
class TransactionSummary:
    opening_balance: float
    transfer_in: float
    internal_transfer: float
    court_divorce: float
    spot_withdrawals: float
    investment_returns: float
    total_contributions: float
    accumulated_credit: float

# ----------------------------
# Investments
# ----------------------------

@dataclass
class InvestmentPortfolio:
    growth: float
    moderate: float
    conservative: float
    trading_fund: float
    accumulated_credit: float
    
@dataclass
class TwoPotInvestment:
    vested_provident: float
    vested_pension: float
    savings_pot: float
    retirement_pot: float

@dataclass
class InvestmentSummary:
    portfolio: InvestmentPortfolio | None = None
    two_pot: TwoPotInvestment | None = None

# ----------------------------
# Benefits
# ----------------------------

@dataclass
class BenefitOverview:
    accumulated_credit: float
    employer_benefit: float
    death_benefit: float
    disability_benefit: float
    spouse_assurance: float
    resignation_total: float
    retirement_total: float
    death_total: float

# ----------------------------
# Root Context
# ----------------------------

@dataclass
class StatementContext:
    member: Member
    salary: Salary
    contributions: ContributionHistory
    transactions: TransactionSummary
    investments: InvestmentSummary
    benefits: BenefitOverview