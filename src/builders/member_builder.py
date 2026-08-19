from models import Member
from utils import safe_str, safe_date

def build_member(mbs_data) -> Member:

    # Take the latest member information
    latest_mbs_data = mbs_data.loc[mbs_data["pyrl_dt"].idxmax()]
    
    first_name = safe_str(latest_mbs_data["firstname"], str.title)
    last_name = safe_str(latest_mbs_data["lastname"], str.title)

    nat_id = safe_str(latest_mbs_data["natlidno"], str.upper)
    passport = safe_str(latest_mbs_data["passport_no"], str.upper)

    return Member(

        name = f"{first_name} {last_name}".strip(),

        member_number = safe_str(latest_mbs_data["mbr_no"], str.upper),

        participating_employer = safe_str(latest_mbs_data["plan_nm"], str.title),

        scheme_code = safe_str(latest_mbs_data["cont_no"], str.upper),

        bill_group = safe_str(latest_mbs_data["mbr_bill_grp"], str.title),

        payroll_number = safe_str(latest_mbs_data["pyrl_no"], str.upper),

        prior_number = safe_str(latest_mbs_data["pr_mbr_no"], str.upper),

        retirement_date = safe_date(latest_mbs_data["nrd"]),

        date_of_birth = safe_date(latest_mbs_data["birthdt"]),

        join_fund = safe_date(latest_mbs_data["join_scheme_dt"]),

        join_company = safe_date(latest_mbs_data["join_company_dt"]),

        id_number = nat_id if nat_id else passport,

        tax_number = safe_str(latest_mbs_data["tax_ref_no_payroll"], str.upper),

        client_number = safe_str(latest_mbs_data["nameid"], str.upper),

        cell_phone = safe_str(latest_mbs_data["recent_phone"]),

        email = safe_str(latest_mbs_data["recent_email"], str.lower),

        pay_centre = safe_str(latest_mbs_data["pay_centre"], str.title)
    )