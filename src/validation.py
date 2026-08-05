import pandas as pd
from utils import validate_required_field, add_reason, build_validation_output, normalize_dates, create_data_profile

# MEMBER DETAILS VALIDATION============================================================================================================#
def validate_member_details(df):
    results = []

    # Scheme Numbers (cont_no) are not NULL.
    validate_required_field(df, "cont_no", results, "Scheme Number is null or empty")

    # Plan Name (plan_nm) is not NULL.
    validate_required_field(df, "plan_nm", results, "Plan Name is null or empty")

    # Members (mbr_no) are not NULL.
    validate_required_field(df, "mbr_no", results, "Member Number is null or empty")

    # Join Scheme date (join_scheme_dt) must be NOT NULL
    mask = df["join_scheme_dt"].isna()
    add_reason(results, df.loc[mask, "case_mbr_key"], "Join Scheme Date is null")

    # Birth date (birthdt) must be NOT NULL
    mask = df["birthdt"].isna()
    add_reason(results, df.loc[mask, "case_mbr_key"], "Birth Date is null")

    # Join Scheme date (join_scheme_dt) must be NOT NULL and NOT less than birth date (birthdt).
    mask = (df["join_scheme_dt"].notna() & df["birthdt"].notna() & (df["join_scheme_dt"] < df["birthdt"]))
    add_reason(results, df.loc[mask, "case_mbr_key"], "Join Scheme Date is before Birth Date")

    # NRD (nrd) must be NOT NULL
    mask = df["nrd"].isna()
    add_reason(results, df.loc[mask, "case_mbr_key"], "NRD is null")

    # NRD (nrd) must be GREATER than the join scheme date (join_scheme_dt).
    mask = (df["nrd"].notna() & df["join_scheme_dt"].notna() & (df["nrd"] <= df["join_scheme_dt"]))
    add_reason(results, df.loc[mask, "case_mbr_key"], "NRD is not greater than Join Scheme Date")

    # National ID validations
    natlidno = df["natlidno"].astype("string").str.strip()
    passport_no = df["passport_no"].astype("string").str.strip()
    
    # National ID AND passport Number must NOT be BOTH NULL.
    mask = ((natlidno.isna() | (natlidno == "")) & (passport_no.isna() | (passport_no == "")))
    add_reason(results, df.loc[mask, "case_mbr_key"], "Both National ID Number and Passport Number are null")

    # National ID Number must be 13 digits.
    mask = (natlidno.notna() & (natlidno != "") & ~natlidno.str.fullmatch(r"\d{13}"))
    add_reason(results, df.loc[mask, "case_mbr_key"], "National ID Number is not 13 digits")

    # First 6 digits of ID must match birth date (YYMMDD)
    valid_id_mask = (df["birthdt"].notna() & natlidno.notna() & (natlidno != "") & natlidno.str.fullmatch(r"\d{13}"))
    birth_date_string = pd.to_datetime(df["birthdt"], errors="coerce").dt.strftime("%y%m%d")

    mask = (valid_id_mask & (natlidno.str[:6] != birth_date_string))
    add_reason(results, df.loc[mask, "case_mbr_key"], "First 6 digits of National ID Number do not match Birth Date")

    # Gender must be populated
    gender = df["gender"].astype("string").str.strip().str.lower()

    mask = gender.isna() | (gender == "")
    add_reason(results, df.loc[mask, "case_mbr_key"], "Gender is null or empty")

    # Gender must match ID number
    gender_number = pd.to_numeric(natlidno.str[6:10], errors="coerce")

    derived_gender = gender_number.where(gender_number >= 5000, other=-1)
    derived_gender = derived_gender.apply(lambda x: "male" if x >= 5000 else "female")

    # Only compare gender when it is Male or Female
    valid_gender_mask = gender.isin(["male", "female"])
    mask = (valid_id_mask & valid_gender_mask & (gender != derived_gender))
    add_reason(results, df.loc[mask, "case_mbr_key"], "Gender does not match National ID Number")

    return build_validation_output(results)

# CONTRIBUTIONS VALIDATION=============================================================================================================#
def validate_transactions(df):
    results = []

    # Contribution Date must not be NULL and must be a valid date.
    mask = df["contribution_dt"].isna()
    add_reason(results, df.loc[mask, "case_mbr_key"], "Contribution Date (contribution_dt) is null or invalid")

    # Annual Pension Salary must be numeric.
    ann_pen_salary = pd.to_numeric(df["ann_pen_salary"], errors="coerce")

    mask = ann_pen_salary.isna()
    add_reason(results, df.loc[mask, "case_mbr_key"], "Annual Pension Salary (ann_pen_salary) is not numeric")

    mask = ann_pen_salary == 0
    add_reason(results, df.loc[mask, "case_mbr_key"], "Annual Pension Salary (ann_pen_salary) is zero")

    # Annual Risk Salary must be numeric.
    ann_risk_salary = pd.to_numeric(df["ann_risk_salary"], errors="coerce")

    mask = ann_risk_salary.isna()
    add_reason(results, df.loc[mask, "case_mbr_key"], "Annual Risk Salary (ann_risk_salary) is not numeric")

    mask = ann_risk_salary == 0
    add_reason(results, df.loc[mask, "case_mbr_key"], "Annual Risk Salary (ann_risk_salary) is zero")

    # Employee Contribution must not be NULL or empty.
    validate_required_field(df, "member_contribution", results, "Member Contribution (member_contribution) is null or empty")

    member_contribution = pd.to_numeric(df["member_contribution"], errors="coerce")

    mask = (df["member_contribution"].notna() & (df["member_contribution"].astype(str).str.strip() != "") & member_contribution.isna())
    add_reason(results, df.loc[mask, "case_mbr_key"], "Member Contribution (member_contribution) is not numeric")

    # Employer Contribution must not be NULL or empty and must be a valid numeric.
    validate_required_field(df, "employer_contribution", results, "Employer Contribution (employer_contribution) is null or empty")

    employer_contribution = pd.to_numeric(df["employer_contribution"], errors="coerce")
    mask = (df["employer_contribution"].notna() & (df["employer_contribution"].astype(str).str.strip() != "") & employer_contribution.isna())
    add_reason(results, df.loc[mask, "case_mbr_key"], "Employer Contribution (employer_contribution) is not numeric")

    return build_validation_output(results)

# TWO POT AND INVESTMENTS VALIDATION===================================================================================================#
def validate_two_pot_investment(df):
    results = []

    # Case Member Key required
    validate_required_field(df, "case_mbr_key", results, "case_mbr_key is null or empty")
    return build_validation_output(results)

def validate_all(member_detail_df_raw, transactions_df_raw, tp_investment_df_raw):
    # MEMBER DETAILS
    member_detail_df_raw_copy = member_detail_df_raw.copy()
    member_detail_df_raw_copy = normalize_dates(member_detail_df_raw_copy, ["join_scheme_dt", "birthdt", "nrd"])
    member_details_profile_df = create_data_profile(member_detail_df_raw_copy)
    member_details_profile_df.to_csv("../data/primary/member_details_data_profile.csv", index=False)
    invalid_members_df = validate_member_details(member_detail_df_raw_copy)
    invalid_members_df.to_csv("../data/primary/invalid_member_details_case_key.csv", index=False)

    # Filter out invalid members
    invalid_member_case_mbr_keys = invalid_members_df["case_mbr_key"].unique()
    member_detail_df_validated = member_detail_df_raw[~member_detail_df_raw["case_mbr_key"].isin(invalid_member_case_mbr_keys)]

    member_detail_df_validated = member_detail_df_raw
    member_detail_df_validated.to_csv('../data/primary/member_detail_validated.csv', index=False)

    # TRANSACTIONS
    transactions_df_raw_copy = transactions_df_raw.copy()
    transactions_df_raw_copy = normalize_dates(transactions_df_raw_copy, ["contribution_dt"])
    transactions_profile_df = create_data_profile(transactions_df_raw_copy)
    transactions_profile_df.to_csv("../data/primary/transactions_data_profile.csv", index=False)
    invalid_transactions_df = validate_transactions(transactions_df_raw_copy)
    invalid_transactions_df.to_csv("../data/primary/invalid_transactions.csv", index=False)
    
    # Filter out invalid members
    invalid_member_case_mbr_keys = invalid_transactions_df["case_mbr_key"].unique()
    trasnsactions_df_validated = transactions_df_raw[~transactions_df_raw["case_mbr_key"].isin(invalid_member_case_mbr_keys)]

    # trasnsactions_df_validated = transactions_df_raw
    trasnsactions_df_validated.to_csv('../data/primary/transactions_validated.csv', index=False)

    # TWO POT AND INVESTMENT
    two_pot_investment_df_raw_copy = tp_investment_df_raw.copy()
    two_pot_investment_df_raw_copy = normalize_dates(two_pot_investment_df_raw_copy, ["latest_rbal_dt"])
    two_pot_profile_df = create_data_profile(two_pot_investment_df_raw_copy)
    two_pot_profile_df.to_csv("../data/primary/two_pot_investment_data_profile.csv", index=False)
    invalid_two_pot_investment_df = validate_two_pot_investment(two_pot_investment_df_raw_copy)
    invalid_two_pot_investment_df.to_csv("../data/primary/invalid_two_pot_investment.csv", index=False)
    
    # Filter out invalid members
    invalid_member_case_mbr_keys = invalid_two_pot_investment_df["case_mbr_key"].unique()
    two_pot_investment_validated = tp_investment_df_raw[~tp_investment_df_raw["case_mbr_key"].isin(invalid_member_case_mbr_keys)]

    # two_pot_investment_validated = tp_investment_df_raw
    two_pot_investment_validated.to_csv('../data/primary/two_pot_investment_validated.csv', index=False)