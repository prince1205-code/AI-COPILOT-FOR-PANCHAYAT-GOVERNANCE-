"""
Clean Government Schemes Dataset
"""

from pathlib import Path
import pandas as pd


# -----------------------------
# Paths
# -----------------------------

ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = ROOT / "data" / "updated_data.csv"

OUTPUT_FILE = ROOT / "knowledge_base" / "clean_schemes.json"


# -----------------------------
# Load CSV
# -----------------------------

print("Loading dataset...")

df = pd.read_csv(INPUT_FILE)

print(f"Rows    : {len(df)}")
print(f"Columns : {len(df.columns)}")


# -----------------------------
# Remove useless columns
# -----------------------------

df = df.drop(columns=["Unnamed: 9"], errors="ignore")


# -----------------------------
# Rename Columns
# -----------------------------

df.columns = [

    "scheme_name",

    "slug",

    "description",

    "benefits",

    "eligibility",

    "application_process",

    "required_documents",

    "level",

    "category",

    "tags"

]


# -----------------------------
# Fill Missing Values
# -----------------------------

df = df.fillna("")


# -----------------------------
# Remove Duplicate Schemes
# -----------------------------

df = df.drop_duplicates(subset=["scheme_name"])


# -----------------------------
# Strip Spaces
# -----------------------------

for column in df.columns:

    df[column] = df[column].astype(str).str.strip()


# -----------------------------
# Lowercase Search Columns
# -----------------------------

df["search_text"] = (

    df["scheme_name"]

    + " "

    + df["description"]

    + " "

    + df["tags"]

).str.lower()


# -----------------------------
# Save JSON
# -----------------------------

OUTPUT_FILE.parent.mkdir(exist_ok=True)

df.to_json(

    OUTPUT_FILE,

    orient="records",

    indent=4,

    force_ascii=False

)

print()

print("Dataset Cleaned Successfully")

print("Output :", OUTPUT_FILE)

print("Total Schemes :", len(df))