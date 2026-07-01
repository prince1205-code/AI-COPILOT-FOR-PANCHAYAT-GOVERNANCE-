"""
=========================================================
Sahayak AI - Search Index Builder
=========================================================

Purpose:
    Build a fast searchable index from clean_schemes.json

Author : Prince Kumar
Project : AI Copilot for Panchayat Governance
=========================================================
"""

import json
from pathlib import Path

# =====================================================
# Paths
# =====================================================

ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = ROOT / "knowledge_base" / "clean_schemes.json"

OUTPUT_FILE = ROOT / "knowledge_base" / "search_index.json"

# =====================================================
# Load Dataset
# =====================================================

print("=" * 60)
print("Building Search Index")
print("=" * 60)

with open(INPUT_FILE, "r", encoding="utf-8") as f:

    schemes = json.load(f)

print(f"Loaded {len(schemes)} schemes.\n")

# =====================================================
# Alias Dictionary
# =====================================================

ALIASES = {

    "Pradhan Mantri Awas Yojana Gramin": [
        "pmay",
        "pmay-g",
        "pm awas",
        "pm awas yojana",
        "pradhan mantri awas",
        "housing",
        "house",
        "home",
        "ghar",
        "awas"
    ],

    "Ayushman Bharat - Pradhan Mantri Jan Arogya Yojana": [
        "ayushman",
        "ayushman bharat",
        "pmjay",
        "ab-pmjay",
        "health insurance",
        "medical insurance"
    ],

    "Pradhan Mantri Kisan Samman Nidhi": [
        "pm kisan",
        "kisan",
        "farmer",
        "farmers",
        "kisan samman nidhi"
    ],

    "Mahatma Gandhi National Rural Employment Guarantee Act": [
        "mgnrega",
        "nrega",
        "employment",
        "job card",
        "100 days work"
    ],

    "Pradhan Mantri Ujjwala Yojana": [
        "ujjwala",
        "gas",
        "lpg",
        "cylinder"
    ]
}

# =====================================================
# Build Index
# =====================================================

search_index = []

for scheme in schemes:

    aliases = ALIASES.get(
        scheme.get("scheme_name", ""),
        []
    )

    searchable_text = (
        scheme.get("search_text", "")
        + " "
        + " ".join(aliases)
    ).lower()

    record = {

        "scheme_name": scheme.get("scheme_name", ""),

        "aliases": aliases,

        "search_text": searchable_text,

        "category": scheme.get("category", ""),

        "level": scheme.get("level", ""),

        "slug": scheme.get("slug", "")
    }

    search_index.append(record)

# =====================================================
# Save
# =====================================================

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:

    json.dump(

        search_index,

        f,

        indent=4,

        ensure_ascii=False

    )

print("Search Index Created Successfully.")

print("Total Indexed :", len(search_index))

print("Saved To :", OUTPUT_FILE)