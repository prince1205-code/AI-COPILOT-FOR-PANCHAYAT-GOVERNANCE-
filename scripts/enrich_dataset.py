"""
=========================================================
Sahayak AI - Dataset Enrichment
=========================================================

Purpose:
    Enrich government schemes dataset using
    MetadataExtractor.

Author : Prince Kumar
Project : AI Copilot for Panchayat Governance
=========================================================
"""

import json
from pathlib import Path

from src.recommendation.metadata_extractor import MetadataExtractor


# =====================================================
# Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "knowledge_base" / "clean_schemes.json"

OUTPUT_FILE = BASE_DIR / "knowledge_base" / "enriched_schemes.json"


# =====================================================
# Main
# =====================================================

print("=" * 60)
print("Dataset Enrichment Started")
print("=" * 60)

# Load Dataset

with open(INPUT_FILE, "r", encoding="utf-8") as file:

    schemes = json.load(file)

print(f"\nLoaded {len(schemes)} schemes.\n")


# Metadata Extractor

extractor = MetadataExtractor()


# Enrich Dataset

for scheme in schemes:

    metadata = extractor.extract(scheme)

    scheme.update(metadata)


# Save Dataset

with open(
    OUTPUT_FILE,
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        schemes,
        file,
        indent=4,
        ensure_ascii=False
    )


print("Dataset Enriched Successfully.\n")

print("Output File")

print(OUTPUT_FILE)

print()

print("Sample Metadata\n")

sample = schemes[0]

print("Scheme :", sample.get("scheme_name"))

print("States :", sample.get("states"))

print("Target Groups :", sample.get("target_groups"))

print("Income Group :", sample.get("income_group"))

print("Age Group :", sample.get("age_group"))

print("Gender Group :", sample.get("gender_group"))

print("Negative Keywords :", sample.get("negative_keywords"))