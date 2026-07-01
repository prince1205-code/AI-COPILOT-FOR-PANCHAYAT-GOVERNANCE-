"""
=========================================================
Sahayak AI - Dataset Analysis
=========================================================

Purpose:
    Analyze Government Schemes Dataset

Author : Prince Kumar
Project : AI Copilot for Panchayat Governance
=========================================================
"""

from pathlib import Path
import json
from collections import Counter


# =====================================================
# Paths
# =====================================================

ROOT = Path(__file__).resolve().parent.parent

DATASET = ROOT / "knowledge_base" / "clean_schemes.json"


# =====================================================
# Load Dataset
# =====================================================

print("=" * 60)
print("Government Schemes Dataset Analysis")
print("=" * 60)

with open(DATASET, "r", encoding="utf-8") as f:

    schemes = json.load(f)

print(f"\nTotal Schemes : {len(schemes)}")


# =====================================================
# Level Analysis
# =====================================================

levels = Counter()

for scheme in schemes:

    level = scheme.get("level", "").strip()

    if level == "":
        level = "Unknown"

    levels[level] += 1

print("\n" + "=" * 60)
print("LEVEL DISTRIBUTION")
print("=" * 60)

for level, count in levels.most_common():

    print(f"{level:25} : {count}")


# =====================================================
# Category Analysis
# =====================================================

categories = Counter()

for scheme in schemes:

    category = scheme.get("category", "").strip()

    if category == "":
        category = "Unknown"

    categories[category] += 1

print("\n" + "=" * 60)
print("TOP 20 CATEGORIES")
print("=" * 60)

for category, count in categories.most_common(20):

    print(f"{category:45} : {count}")


# =====================================================
# Missing Data
# =====================================================

fields = [

    "scheme_name",

    "description",

    "benefits",

    "eligibility",

    "application_process",

    "required_documents",

    "category",

    "level"

]

print("\n" + "=" * 60)
print("MISSING DATA")
print("=" * 60)

for field in fields:

    missing = 0

    for scheme in schemes:

        if scheme.get(field, "").strip() == "":

            missing += 1

    print(f"{field:25} : {missing}")


# =====================================================
# PM Schemes
# =====================================================

pm_schemes = []

for scheme in schemes:

    name = scheme.get("scheme_name", "").lower()

    if "pradhan mantri" in name or "pm" in name:

        pm_schemes.append(scheme)

print("\n" + "=" * 60)
print("PM SCHEMES")
print("=" * 60)

print("Total PM Schemes :", len(pm_schemes))

print("\nFirst 20 PM Schemes:\n")

for scheme in pm_schemes[:20]:

    print("-", scheme["scheme_name"])


# =====================================================
# Housing Schemes
# =====================================================

housing = []

for scheme in schemes:

    text = (

        scheme.get("search_text", "")

    ).lower()

    if "housing" in text or "house" in text or "awas" in text:

        housing.append(scheme)

print("\n" + "=" * 60)
print("HOUSING SCHEMES")
print("=" * 60)

print("Total Housing Schemes :", len(housing))


# =====================================================
# Duplicate Names
# =====================================================

names = Counter()

for scheme in schemes:

    names[scheme["scheme_name"]] += 1

duplicates = {

    name: count

    for name, count in names.items()

    if count > 1

}

print("\n" + "=" * 60)
print("DUPLICATE NAMES")
print("=" * 60)

print("Duplicate Scheme Names :", len(duplicates))


# =====================================================
# Sample Record
# =====================================================

print("\n" + "=" * 60)
print("SAMPLE RECORD")
print("=" * 60)

sample = schemes[0]

for key, value in sample.items():

    print(f"{key:25} : {str(value)[:120]}")