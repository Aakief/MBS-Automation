import pandas as pd
from utils import validate_required_field, add_reason, build_validation_output, normalize_dates, create_data_profile, valid_sa_id_checksum

# MEMBER STATEMENT TABLE VALIDATION================================================================================================#
def validate_member_statement(df):
    results = []

    # MEMBER DETAILS
    # There must be a case member key
    validate_required_field(df, "case_mbr_key", results, "case_mbr_key is null or empty")

    # There must be a scheme number.
    validate_required_field(df, "cont_no", results, "Scheme Number is null or empty")

    # Scheme Number must start with 1 uppercase letter, followed by 6 digits and 1 uppercase letter
    mask = (df["cont_no"].notna() & (~df["cont_no"].astype(str).str.strip().str.fullmatch(r"[A-Z]\d{6}[A-Z]")))
    add_reason(results, df.loc[mask, "case_mbr_key"], "Scheme Number format is invalid")

    # There must be a plan name.
    validate_required_field(df, "plan_nm", results, "Plan Name is null or empty")

    # There must be a member number
    validate_required_field(df, "mbr_no", results, "Member Number is null or empty")

    # There must be a join date
    mask = df["join_scheme_dt"].isna()
    add_reason(results, df.loc[mask, "case_mbr_key"], "Join Scheme Date is null")

    # There must be a birth date 
    mask = df["birthdt"].isna()
    add_reason(results, df.loc[mask, "case_mbr_key"], "Birth Date is null")

    # The join scheme date must be after the birth date.
    mask = (df["join_scheme_dt"].notna() & df["birthdt"].notna() & (df["join_scheme_dt"] < df["birthdt"]))
    add_reason(results, df.loc[mask, "case_mbr_key"], "Join Scheme Date is before Birth Date")

    # There must be an NRD (Next Retirement Date)
    mask = df["nrd"].isna()
    add_reason(results, df.loc[mask, "case_mbr_key"], "NRD is null")

    # NRD must be greater than the Join Scheme Date.
    mask = (df["nrd"].notna() & df["join_scheme_dt"].notna() & (df["nrd"] <= df["join_scheme_dt"]))
    add_reason(results, df.loc[mask, "case_mbr_key"], "NRD is not greater than Join Scheme Date")

    # NATIONAL ID VALIDATIONS
    natlidno = df["natlidno"].astype("string").str.strip()
    passport_no = df["passport_no"].astype("string").str.strip()

    # There must be either a passport or an ID number
    mask = ((natlidno.isna() | (natlidno == "")) & (passport_no.isna() | (passport_no == "")))
    add_reason(results, df.loc[mask, "case_mbr_key"], "Both National ID Number and Passport Number are null")

    # National ID must be 13 digits.
    mask = (natlidno.notna() & (natlidno != "") & ~natlidno.str.fullmatch(r"\d{13}"))
    add_reason(results, df.loc[mask, "case_mbr_key"], "National ID Number is not 13 digits")

    # National ID must pass the checksum (consistent with the heartbeat)
    valid_id_mask = (natlidno.notna() & (natlidno != "") & natlidno.str.fullmatch(r"\d{13}"))
    mask = (valid_id_mask & ~natlidno.apply(valid_sa_id_checksum))
    add_reason(results, df.loc[mask, "case_mbr_key"], "National ID Number checksum is invalid")

    # CONTRIBUTIONS
    # There must be an Annual Salary (must not be NULL)
    mask = (df["ann_salar"].isna() | (df["ann_salar"].astype(str).str.strip() == ""))
    add_reason(results, df.loc[mask, "case_mbr_key"], "Annual Salary is null or empty")

    # Annual Salary must be numeric
    ann_salar = pd.to_numeric(df["ann_salar"], errors="coerce")
    mask = (df["ann_salar"].notna() & (df["ann_salar"].astype(str).str.strip() != "") & ann_salar.isna())
    add_reason(results, df.loc[mask, "case_mbr_key"], "Annual Salary is not numeric")

    # Annual Salary must not be 0
    mask = ann_salar == 0
    add_reason(results, df.loc[mask, "case_mbr_key"], "Annual Salary is zero")

    # There must be an Annual Risk Salary (must not be NULL)
    mask = (df["ann_risk"].isna() | (df["ann_risk"].astype(str).str.strip() == ""))
    add_reason(results, df.loc[mask, "case_mbr_key"], "Annual Risk Salary is null or empty")

    # Annual Risk salary must be numeric
    ann_risk = pd.to_numeric(df["ann_risk"], errors="coerce")
    mask = (df["ann_risk"].notna() & (df["ann_risk"].astype(str).str.strip() != "") & ann_risk.isna())
    add_reason(results, df.loc[mask, "case_mbr_key"], "Annual Risk Salary is not numeric")

    # Annual Risk salary must not be 0.
    mask = ann_risk == 0
    add_reason(results, df.loc[mask, "case_mbr_key"], "Annual Risk Salary is zero")

    # ACCUMULATED CREDIT RECONCILIATION
    # Accumulated Credit = Trading Fund + Moderate + Conservative + Growth
    calculated_acc_credit = (
        pd.to_numeric(df["trading_fund"], errors="coerce").fillna(0)
        +
        pd.to_numeric(df["moderate"], errors="coerce").fillna(0)
        +
        pd.to_numeric(df["conservative"], errors="coerce").fillna(0)
        +
        pd.to_numeric(df["growth"], errors="coerce").fillna(0)
    )
    acc_credit = pd.to_numeric(df["acc_credit"], errors="coerce")
    mask = (acc_credit.notna() & ((acc_credit - calculated_acc_credit).abs() > 0.01))
    add_reason(results,df.loc[mask, "case_mbr_key"], "Accumulated Credit does not equal Trading Fund plus Moderate plus Conservative plus Growth")

    return build_validation_output(results)

def validate_all(member_statement_df_raw):

    # Create working copy
    member_statement_df_raw_copy = member_statement_df_raw.copy()

    # Normalise dates
    member_statement_df_raw_copy = normalize_dates(member_statement_df_raw_copy, ["birthdt","join_scheme_dt","nrd","join_company_dt","pyrl_dt"])

    # Create data profile
    member_statement_profile_df = create_data_profile(member_statement_df_raw_copy)
    member_statement_profile_df.to_csv("../data/primary/mbs_data_profile.csv", index=False)

    # Run validations
    invalid_members_df = validate_member_statement(member_statement_df_raw_copy)
    invalid_members_df.to_csv("../data/primary/mbs_validation.csv", index=False)

    # Remove invalid members
    invalid_case_mbr_keys = (invalid_members_df["case_mbr_key"].unique())
    member_statement_validated = (member_statement_df_raw[~member_statement_df_raw["case_mbr_key"].isin(invalid_case_mbr_keys)])
    member_statement_validated.to_csv("../data/primary/mbs_dataset_validated.csv", index=False)