from models import Member
from utils import safe_str, safe_date

def build_member(member_data) -> Member:

    first_name = safe_str(member_data["firstname"].iloc[0], str.title)
    last_name = safe_str(member_data["lastname"].iloc[0], str.title)

    nat_id = safe_str(member_data["natlidno"].iloc[0], str.upper)
    passport = safe_str(member_data["passport_no"].iloc[0], str.upper)

    return Member(

        name = f"{first_name} {last_name}".strip(),

        member_number = safe_str(member_data["mbr_no"].iloc[0], str.upper),

        participating_employer = safe_str(member_data["plan_nm"].iloc[0], str.title),

        scheme_code = safe_str(member_data["cont_no"].iloc[0], str.upper),

        bill_group = safe_str(member_data["mbr_bill_grp"].iloc[0], str.title),

        payroll_number = safe_str(member_data["pyrl_no"].iloc[0], str.upper),

        prior_number = safe_str(member_data["pr_mbr_no"].iloc[0], str.upper),

        retirement_date = safe_date(member_data["nrd"].iloc[0]),

        date_of_birth = safe_date(member_data["birthdt"].iloc[0]),

        join_fund = safe_date(member_data["past_service_dt"].iloc[0]),

        join_company = safe_date(member_data["join_scheme_dt"].iloc[0]),

        id_number = nat_id if nat_id else passport,

        tax_number = safe_str(member_data["tax_ref_no_payroll"].iloc[0], str.upper),

        client_number = safe_str(member_data["nameid"].iloc[0], str.upper),

        cell_phone = safe_str(member_data["recent_phone"].iloc[0]),

        email = safe_str(member_data["recent_email"].iloc[0], str.lower),

        pay_centre = ""
    )