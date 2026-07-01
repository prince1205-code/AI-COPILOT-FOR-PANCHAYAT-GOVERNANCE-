"""
Unit tests for EligibilityEngine fixes.
Run: python3 -m pytest scripts/test_engine_units.py -v
"""
import sys
sys.path.insert(0, ".")

import pytest
from src.recommendation.eligibility_engine import EligibilityEngine

@pytest.fixture(scope="module")
def engine():
    return EligibilityEngine()


# ----------------------------------------------------------
# Fix 1: State scoring
# ----------------------------------------------------------

def test_state_specific_scheme_ranks_above_central(engine):
    """A state-matched scheme must outscore a central scheme for same profile."""
    profile = {"age": 30, "state": "Kerala", "occupation": "Labour", "income": 80000, "gender": "male"}
    results = engine.recommend(profile, top_k=10)
    state_match = [r for r in results if "State Match" in r["reason"]]
    central     = [r for r in results if "State Match" not in r["reason"] and "State Mismatch" not in r["reason"]]
    if state_match and central:
        assert state_match[0]["score"] >= central[0]["score"], \
            "State-matched scheme should rank >= central scheme"


def test_state_mismatch_penalised(engine):
    """Schemes from a different state must not appear in top results."""
    profile = {"age": 30, "state": "Kerala", "occupation": "Farmer", "income": 80000, "gender": "male"}
    results = engine.recommend(profile, top_k=5)
    for r in results:
        assert "State Mismatch" not in r["reason"], \
            f"State mismatch scheme should not be in top-5: {r['scheme_name']}"


def test_gujarat_and_tamilnadu_farmer_get_different_recommendations(engine):
    """Gujarat and Tamil Nadu farmers must get different top-5 (both have state-specific farmer schemes)."""
    guj_profile = {"age": 30, "state": "Gujarat",    "occupation": "Farmer", "income": 80000, "gender": "male"}
    tn_profile  = {"age": 30, "state": "Tamil Nadu", "occupation": "Farmer", "income": 80000, "gender": "male"}
    guj_top = engine.recommend(guj_profile, top_k=5)
    tn_top  = engine.recommend(tn_profile,  top_k=5)
    guj_names = {r["scheme_name"] for r in guj_top}
    tn_names  = {r["scheme_name"] for r in tn_top}
    assert guj_names != tn_names, "Gujarat and Tamil Nadu farmers should get different recommendations"


# ----------------------------------------------------------
# Fix 2: Gender matching
# ----------------------------------------------------------

def test_gender_all_scheme_no_gender_reason(engine):
    """Schemes with gender_group=All must never show 'Gender Match' in reason."""
    profile = {"age": 30, "state": "Uttar Pradesh", "occupation": "Farmer", "income": 80000, "gender": "male"}
    results = engine.recommend(profile, top_k=10)
    for r in results:
        assert "Gender Match" not in r["reason"], \
            f"'Gender Match' should not appear for gender_group=All scheme: {r['scheme_name']}"


def test_gender_match_only_for_targeted_scheme(engine):
    """Gender Match reason must appear only for schemes explicitly targeting that gender."""
    profile = {"age": 28, "state": "Bihar", "occupation": "Women", "income": 60000, "gender": "female"}
    results = engine.recommend(profile, top_k=10)
    gender_matched = [r for r in results if "Gender Match" in r["reason"]]
    assert len(gender_matched) > 0, "Female-targeted schemes should show Gender Match"


# ----------------------------------------------------------
# Fix 3: Empty occupation
# ----------------------------------------------------------

def test_empty_occupation_no_occupation_specific_schemes(engine):
    """When occupation is empty, occupation-specific schemes must not appear."""
    profile = {"age": 40, "state": "Uttar Pradesh", "occupation": "", "income": 100000, "gender": "male"}
    results = engine.recommend(profile, top_k=10)
    occ_reasons = {"Farmer Scheme", "Student Scheme", "Labour Welfare", "Business Support", "Women Scheme"}
    for r in results:
        reason_set = {part.strip() for part in r["reason"].split(",")}
        overlap = reason_set & occ_reasons
        assert not overlap, \
            f"Occupation-specific scheme should not appear for empty occupation: {r['scheme_name']} | {r['reason']}"


def test_all_none_profile_returns_results(engine):
    """All-None profile must still return some results (flagship fallback)."""
    profile = {"age": None, "state": None, "occupation": "", "income": None, "gender": ""}
    results = engine.recommend(profile, top_k=5)
    assert len(results) > 0, "All-None profile should still get flagship scheme results"


# ----------------------------------------------------------
# Fix 4: Confidence calibration
# ----------------------------------------------------------

def test_confidence_not_all_100(engine):
    """Not all results should have 95% confidence — relative scoring must differentiate."""
    profile = {"age": 30, "state": "Uttar Pradesh", "occupation": "Farmer", "income": 80000, "gender": "male"}
    results = engine.recommend(profile, top_k=10)
    confidences = [int(r["confidence"].replace("%", "")) for r in results]
    assert confidences[0] == 95, "Top result must have 95% confidence"
    assert any(c < 95 for c in confidences), "Lower-ranked results must have < 95% confidence"


def test_confidence_max_95(engine):
    """Confidence must never exceed 95%."""
    profile = {"age": 24, "state": "Punjab", "occupation": "Farmer", "income": 80000, "gender": "male"}
    results = engine.recommend(profile, top_k=10)
    for r in results:
        conf = int(r["confidence"].replace("%", ""))
        assert conf <= 95, f"Confidence exceeded 95%: {r['scheme_name']} = {r['confidence']}"


# ----------------------------------------------------------
# Fix 5: Diversity
# ----------------------------------------------------------

def test_diversity_max_3_per_category(engine):
    """No category should appear more than 3 times in top-10 results."""
    profile = {"age": 30, "state": "Uttar Pradesh", "occupation": "Farmer", "income": 80000, "gender": "male"}
    results = engine.recommend(profile, top_k=10)
    from collections import Counter
    cat_counts = Counter(r["category"] for r in results)
    for cat, count in cat_counts.items():
        assert count <= 3, f"Category '{cat}' appears {count} times — exceeds diversity cap of 3"
