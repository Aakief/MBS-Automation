import pandas as pd
from io import BytesIO
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table, TableStyle, Image as RLImage
from reportlab.graphics.shapes import Drawing, Circle, String
from datetime import date

def safe_str(value, transform=None):
    if pd.isna(value):
        return ""
    value = str(value).strip()
    if not value:
        return ""
    return transform(value) if transform else value

def safe_date(value):
    dt = pd.to_datetime(value, errors="coerce")
    return dt.strftime("%d/%m/%Y") if pd.notna(dt) else ""

def total(data, column):
    if data.empty:
        return 0
    return data[column].sum()

def money(value, negative=False):
    if value in (None, ""):
        return ""

    amount = f"{abs(value):,.2f}".replace(",", " ")

    if negative:
        return f"-R {amount}"

    return f"R {amount}"

def image_to_buffer(image):
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def create_paragraph_factory(styles):
    def P(text, style="Body"):
        return Paragraph(text, styles[style])
    return P

def section_header(title, width, bg_col, box_col):
    """Reusable black section title bar."""
    return Table(
        [[title]], 
        colWidths=[width], 
        rowHeights=[7 * mm], 
        style=TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg_col),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("BOX", (0, 0), (-1, -1), 0.5, box_col),
        ])
    )
    
def boxed_notice(text, width, fillColor, strokeColor, boxColor, icon=True):
    """Green bordered notice box with a simple drawn check icon."""
    icon_cell = Drawing(20, 20)
    icon_cell.add(Circle(10, 10, 8, fillColor = fillColor, strokeColor = strokeColor))
    icon_cell.add(String(6, 5, "✓", fontName="Helvetica-Bold", fontSize=16, fillColor=colors.white))
    data = [[icon_cell if icon else "", text]]
    return Table(data, colWidths=[22 * mm, width - 22 * mm], style=TableStyle([
        ("BOX", (0, 0), (-1, -1), 0.6, boxColor),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (1, 0), (1, 0), "MIDDLE"),
        ("ALIGN", (1, 0), (1, 0), "LEFT"),
    ]))

def note_box(text, width, box_col):

    t = Table([[text]], colWidths=[width])
    t.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, box_col),
        ("LEFTPADDING", (0, 0), (-1, -1), 2),  #formating the box around the disability income benefit plan
        ("RIGHTPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ]))
    return t

def draw_round_logo(logo_image, width, height):
    logo = RLImage(
        image_to_buffer(logo_image),
        width=width,
        height=height
    )

    # Centre the logo in the available space
    logo.hAlign = "CENTER"
 
    return logo

def create_data_profile(df):
    validation_date = date.today().strftime("%d/%m/%Y")
    profile = []

    for column in df.columns:
        series = df[column]

        # Determine data type
        if column.lower() == "gender":
            dtype = "CATEGORICAL"
        elif pd.api.types.is_integer_dtype(series):
            dtype = "INT"
        elif pd.api.types.is_float_dtype(series):
            dtype = "FLOAT"
        elif pd.api.types.is_datetime64_any_dtype(series):
            dtype = "DATE"
        elif pd.api.types.is_bool_dtype(series):
            dtype = "BOOL"
        else:
            dtype = "STR"

        count = series.count()
        nulls = series.isna().sum()
        unique = series.nunique(dropna=True)

        non_null = series.dropna()

        example = (
            non_null.iloc[0]
            if not non_null.empty
            else None
        )

        # Default values
        min_value = None
        max_value = None
        mean_value = None
        median_value = None
        std_dev = None
        zero_count = None
        negative_count = None

        # Min / Max
        if not non_null.empty:
            try:
                min_value = non_null.min()
                max_value = non_null.max()
            except TypeError:
                pass

        # Numeric statistics
        numeric_series = pd.to_numeric(series, errors="coerce")

        if numeric_series.notna().any():
            mean_value = round(numeric_series.mean(), 2)
            median_value = round(numeric_series.median(), 2)
            std_dev = round(numeric_series.std(), 2)
            zero_count = (numeric_series == 0).sum()
            negative_count = (numeric_series < 0).sum()

        profile.append({

            "Date": validation_date,
            "Field": column,
            "Data Type": dtype,

            "COUNT": count,
            "NULLS": nulls,
            "Unique Count": unique,

            "Min": min_value,
            "Max": max_value,
            "Mean": mean_value,
            "Median": median_value,
            "Std Dev": std_dev,

            "Zero Count": zero_count,
            "Negative Count": negative_count,

            "Example": example
        })
    return pd.DataFrame(profile)

def normalize_dates(df, columns): # Convert specified columns to dates. Invalid values become NaT.
    df = df.copy()
    for column in columns:
        df[column] = pd.to_datetime(df[column], errors="coerce")
    return df

def add_reason(results, case_mbr_keys, reason):
    if len(case_mbr_keys) == 0:
        return
    results.append(pd.DataFrame({"case_mbr_key": case_mbr_keys, "reason": reason}))

# This is a function which will be used to check for NULLS.
def validate_required_field(df, field, results, reason):
    mask = (df[field].isna() | (df[field].astype(str).str.strip() == ""))
    add_reason(results, df.loc[mask, "case_mbr_key"], reason)

def build_validation_output(results):
    if results:
        return (pd.concat(results, ignore_index=True).sort_values(["case_mbr_key", "reason"], ignore_index=True))
    return pd.DataFrame(columns=["case_mbr_key", "reason"])

# Function to do a checksum ID validation
def valid_sa_id_checksum(natlidno):
    natlidno = str(natlidno).strip()

    # ID no. must be exactly 13 digits
    if len(natlidno) != 13 or not natlidno.isdigit():
        return False

    # Sum odd positions: 1,3,5,7,9,11,13
    odd_sum = sum(int(natlidno[i])
        for i in [0, 2, 4, 6, 8, 10, 12])

    # Even positions 2,4,6,8,10,12
    # Python indexes are 1,3,5,7,9,11
    even_sum = 0
    for i in [1, 3, 5, 7, 9, 11]:  
        doubled = int(natlidno[i]) * 2
        if doubled > 9:
            doubled -= 9
        even_sum += doubled

    # Sum both odd position total and processed even position total
    total = odd_sum + even_sum
    return total % 10 == 0