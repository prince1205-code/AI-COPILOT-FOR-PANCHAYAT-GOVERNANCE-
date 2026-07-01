"""
=========================================================
Sahayak AI - Eligibility Engine
=========================================================

Purpose:
    Recommend Government Schemes using enriched metadata.
    Modular design: metadata extraction, rule-based scoring,
    priority scoring, and ranking are independent components.

Author : Prince Kumar
Project : AI Copilot for Panchayat Governance
=========================================================
"""
import re
import json

from src.core.config import KNOWLEDGE_BASE_DIR
from src.services.knowledge_loader import KnowledgeLoader


# ----------------------------------------------------------
# Flagship scheme priority table  (slug → bonus points)
# ----------------------------------------------------------
_FLAGSHIP_PRIORITY: dict[str, int] = {
    "pm-kisan":  50,
    "pmfby":     45,
    "kcc":       45,
    "pmksy":     40,
    "pkvy":      35,   # Paramparagat Krishi Vikas Yojana
    "pmay":      30,
    "pmjay":     30,
    "nrega":     25,
    "mgnregs":   25,
    "atal-pension": 20,
    "sukanya":   20,
}

# Occupation target-groups — used to filter when occupation is empty
_OCCUPATION_GROUPS = {"Farmer", "Student", "Labour", "Business", "Women"}


def _wb(word: str) -> re.Pattern:
    """Compile a case-insensitive whole-word regex pattern."""
    return re.compile(r"\b" + re.escape(word) + r"\b", re.IGNORECASE)


def _matches(pattern_or_word: str, text: str) -> bool:
    """Return True if the whole word/phrase is present in text."""
    return bool(_wb(pattern_or_word).search(text))


class EligibilityEngine:
    """
    Rule-based Government Scheme Recommendation Engine.

    Scoring pipeline (independent components):
        1. _score_occupation  – target-group match
        2. _score_demographics – state / gender / age / income
        3. _score_keywords    – boost & penalty via whole-word regex
        4. _score_priority    – flagship scheme bonus
    """

    def __init__(self):
        self.loader = KnowledgeLoader()
        self.schemes = self.loader.schemes

        rules_path = KNOWLEDGE_BASE_DIR / "recommendation_rules.json"
        with open(rules_path, "r", encoding="utf-8") as f:
            self.rules = json.load(f)

        print(f"✅ Eligibility Engine Loaded {len(self.schemes)} schemes.")

    # ----------------------------------------------------------
    # Public API
    # ----------------------------------------------------------

    def recommend(self, profile: dict, top_k: int = 10) -> list[dict]:
        occupation = profile.get("occupation", "").strip()
        rules      = self.rules.get(occupation, {})

        scored = []
        for scheme in self.schemes:
            # Fix 3: skip occupation-specific schemes when occupation is empty
            if not occupation:
                target_groups = scheme.get("target_groups", [])
                if any(g in _OCCUPATION_GROUPS for g in target_groups):
                    continue

            score, reasons = self._score_scheme(scheme, profile, rules)
            if score <= 0:
                continue
            scored.append({
                "scheme_name": scheme.get("scheme_name"),
                "category":    scheme.get("category"),
                "level":       scheme.get("level"),
                "score":       score,
                "reason":      ", ".join(reasons),
            })

        scored.sort(key=lambda x: x["score"], reverse=True)

        # Fix 4: confidence relative to best score in this result set
        top_score = scored[0]["score"] if scored else 1
        for r in scored:
            conf = min(95, round(r["score"] / top_score * 95))
            r["confidence"] = f"{conf}%"

        # Fix 5: diversity cap — max 3 per category
        seen: dict[str, int] = {}
        diverse = []
        for r in scored:
            cat = r.get("category", "")
            if seen.get(cat, 0) < 3:
                diverse.append(r)
                seen[cat] = seen.get(cat, 0) + 1
            if len(diverse) == top_k:
                break

        return diverse

    # ----------------------------------------------------------
    # Component 1 – Occupation / target-group scoring
    # ----------------------------------------------------------

    def _score_occupation(
        self, scheme: dict, occupation: str
    ) -> tuple[int, list[str]]:
        target_groups = scheme.get("target_groups", [])
        group_map = {
            "farmer":   ("Farmer",   40, "Farmer Scheme"),
            "student":  ("Student",  40, "Student Scheme"),
            "labour":   ("Labour",   40, "Labour Welfare"),
            "labor":    ("Labour",   40, "Labour Welfare"),
            "business": ("Business", 40, "Business Support"),
            "women":    ("Women",    40, "Women Scheme"),
        }
        entry = group_map.get(occupation.lower())
        if entry and entry[0] in target_groups:
            return entry[1], [entry[2]]
        return 0, []

    # ----------------------------------------------------------
    # Component 2 – Demographics scoring
    # ----------------------------------------------------------

    def _score_state(self, scheme: dict, state: str) -> tuple[int, list[str]]:
        states = scheme.get("states", [])
        if not states:
            return 20, []  # central / national scheme
        if state and state in states:
            return 80, ["State Match"]
        return -30, ["State Mismatch"]

    def _score_gender(self, scheme: dict, gender: str) -> tuple[int, list[str]]:
        gender_group = scheme.get("gender_group", "All")
        # Fix 2: only award bonus when scheme explicitly targets a gender
        if gender_group in ("", "All", None):
            return 0, []
        if gender and gender_group.lower() == gender.lower():
            return 15, ["Gender Match"]
        return 0, []

    def _score_age(self, scheme: dict, age) -> tuple[int, list[str]]:
        age_group = scheme.get("age_group", "All")
        if age is None:
            return 0, []
        if age_group == "Senior" and age >= 60:
            return 15, ["Senior Citizen"]
        if age_group == "Youth" and age <= 30:
            return 15, ["Youth Scheme"]
        return 0, []

    def _score_income(self, scheme: dict, income) -> tuple[int, list[str]]:
        income_group = scheme.get("income_group", "General")
        if income and income_group == "Low" and income <= 200000:
            return 10, ["Low Income"]
        return 0, []

    def _score_demographics(
        self, scheme: dict, profile: dict
    ) -> tuple[int, list[str]]:
        state   = profile.get("state", "")
        gender  = profile.get("gender", "").lower()
        age     = profile.get("age")
        income  = profile.get("income")

        score   = 0
        reasons = []

        for func, args in [
            (self._score_state,  (scheme, state)),
            (self._score_gender, (scheme, gender)),
            (self._score_age,    (scheme, age)),
            (self._score_income, (scheme, income)),
        ]:
            partial_score, partial_reasons = func(*args)
            score += partial_score
            reasons.extend(partial_reasons)

        return score, reasons

    # ----------------------------------------------------------
    # Component 3 – Keyword boost / penalty (whole-word regex)
    # ----------------------------------------------------------

    def _score_keywords(
        self, scheme: dict, rules: dict
    ) -> tuple[int, list[str]]:
        score   = 0
        reasons = []

        boost_rules   = rules.get("boost", {})
        penalty_rules = rules.get("penalty", {})

        # Build search text from eligibility first, then name + description
        eligibility = scheme.get("eligibility", "")
        name        = scheme.get("scheme_name", "")
        description = scheme.get("description", "")
        text        = f"{eligibility} {name} {description}"

        # Track matched tokens to prevent double-counting overlapping phrases.
        # Rules are ordered longest-first in the JSON, so the first match for
        # any token wins; shorter sub-phrases that share a token are skipped.
        matched_tokens: set[str] = set()

        for keyword, weight in boost_rules.items():
            if _matches(keyword, text):
                tokens = set(keyword.lower().split())
                # Skip if every token in this keyword was already claimed
                # by a longer (higher-priority) phrase
                if tokens & matched_tokens == tokens:
                    continue
                score += weight
                reasons.append(f"+{weight}: {keyword}")
                matched_tokens.update(tokens)

        for keyword, weight in penalty_rules.items():
            if _matches(keyword, text):
                score -= weight
                reasons.append(f"-{weight}: {keyword}")

        return score, reasons

    # ----------------------------------------------------------
    # Component 4 – Flagship priority bonus
    # ----------------------------------------------------------

    def _score_priority(self, scheme: dict) -> tuple[int, list[str]]:
        slug = scheme.get("slug", "").lower()
        name = scheme.get("scheme_name", "").lower()

        for key, bonus in _FLAGSHIP_PRIORITY.items():
            if _matches(key, slug) or _matches(key, name):
                return bonus, [f"Flagship Scheme (+{bonus})"]

        return 0, []

    # ----------------------------------------------------------
    # Negative keyword hard filter
    # ----------------------------------------------------------

    def _is_penalised(self, scheme: dict, occupation: str) -> bool:
        """
        Return True only when the scheme's own negative_keywords list
        is non-empty AND the occupation is one that should avoid them.
        Uses whole-word matching on scheme name + description.
        """
        if occupation.lower() not in ("farmer", "student"):
            return False

        negative_keywords = scheme.get("negative_keywords", [])
        if not negative_keywords:
            return False

        text = f"{scheme.get('scheme_name', '')} {scheme.get('description', '')}"
        return any(_matches(kw, text) for kw in negative_keywords)

    # ----------------------------------------------------------
    # Orchestrator
    # ----------------------------------------------------------

    def _score_scheme(
        self, scheme: dict, profile: dict, rules: dict
    ) -> tuple[int, list[str]]:
        occupation = profile.get("occupation", "")

        if self._is_penalised(scheme, occupation):
            return 0, []

        s1, r1 = self._score_occupation(scheme, occupation)
        s2, r2 = self._score_demographics(scheme, profile)
        s3, r3 = self._score_keywords(scheme, rules)
        s4, r4 = self._score_priority(scheme)

        total   = s1 + s2 + s3 + s4
        reasons = r1 + r2 + r3 + r4
        return total, reasons


# =====================================================
# Testing
# =====================================================

if __name__ == "__main__":

    engine = EligibilityEngine()

    profile = {
        "age":        24,
        "state":      "Uttar Pradesh",
        "occupation": "Farmer",
        "income":     180000,
        "gender":     "male",
    }

    results = engine.recommend(profile)

    print("=" * 60)
    print("Eligibility Engine")
    print("=" * 60)
    print("\nProfile\n")
    print(profile)
    print("\nRecommended Schemes")
    print("-" * 60)

    for i, scheme in enumerate(results, start=1):
        print(f"\n{i}. {scheme['scheme_name']}")
        print(f"Category   : {scheme['category']}")
        print(f"Level      : {scheme['level']}")
        print(f"Score      : {scheme['score']}")
        print(f"Confidence : {scheme['confidence']}")
        print(f"Reason     : {scheme['reason']}")
