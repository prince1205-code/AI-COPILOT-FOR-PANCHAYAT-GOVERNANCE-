"""
=========================================================
Sahayak AI - Metadata Extractor
=========================================================
"""

import re


def _wb(word: str) -> re.Pattern:
    """Compile a case-insensitive whole-word regex pattern."""
    return re.compile(r"\b" + re.escape(word) + r"\b", re.IGNORECASE)


class MetadataExtractor:

    def __init__(self):

        self.states = [

            "Andhra Pradesh",
            "Arunachal Pradesh",
            "Assam",
            "Bihar",
            "Chhattisgarh",
            "Delhi",
            "Goa",
            "Gujarat",
            "Haryana",
            "Himachal Pradesh",
            "Jharkhand",
            "Karnataka",
            "Kerala",
            "Madhya Pradesh",
            "Maharashtra",
            "Manipur",
            "Meghalaya",
            "Mizoram",
            "Nagaland",
            "Odisha",
            "Punjab",
            "Rajasthan",
            "Sikkim",
            "Tamil Nadu",
            "Telangana",
            "Tripura",
            "Uttar Pradesh",
            "Uttarakhand",
            "West Bengal",
            "Puducherry"
        ]

    # --------------------------------------------------

    def extract(self, scheme):

        return {

            "states": self.extract_states(scheme),

            "target_groups": self.extract_target_groups(scheme),

            "income_group": self.extract_income_group(scheme),

            "age_group": self.extract_age_group(scheme),

            "gender_group": self.extract_gender_group(scheme),

            "negative_keywords": self.extract_negative_keywords(scheme)

        }

    # --------------------------------------------------

    def extract_states(self, scheme):

        text = " ".join([

            scheme.get("scheme_name", ""),

            scheme.get("description", ""),

            scheme.get("eligibility", "")

        ]).lower()

        found = []

        for state in self.states:

            if state.lower() in text:

                found.append(state)

        return found

    # --------------------------------------------------

    def extract_target_groups(self, scheme):
        """
        Use eligibility as primary source; fall back to title only.
        Never classify based on description or category alone.
        """
        eligibility = scheme.get("eligibility", "")
        title = scheme.get("scheme_name", "")
        text = eligibility if eligibility.strip() else title

        group_patterns = {
            "Farmer":   [_wb(w) for w in ["farmer", "farmers", "cultivator", "agriculturist", "tenant farmer", "kisan"]],
            "Student":  [_wb(w) for w in ["student", "students", "scholar"]],
            "Women":    [_wb(w) for w in ["women", "woman", "female", "widow", "girl child"]],
            "Labour":   [_wb(w) for w in ["labour", "labor", "worker", "labourer"]],
            "Business": [_wb(w) for w in ["entrepreneur", "startup", "msme", "micro enterprise", "small enterprise"]],
        }

        return [
            group
            for group, patterns in group_patterns.items()
            if any(p.search(text) for p in patterns)
        ]

    # --------------------------------------------------

    def extract_income_group(self, scheme):

        text = scheme.get("eligibility", "")

        patterns = [_wb(w) for w in ["bpl", "below poverty", "economically weaker", "poor"]]

        if any(p.search(text) for p in patterns):

            return "Low"

        return "General"

    # --------------------------------------------------

    def extract_age_group(self, scheme):

        text = scheme.get("eligibility", "").lower()

        if re.search(r"60\s*years|above\s*60|senior citizen", text):

            return "Senior"

        if any(word in text for word in [

            "student",

            "school",

            "college"

        ]):

            return "Youth"

        return "All"

    # --------------------------------------------------

    def extract_gender_group(self, scheme):

        text = scheme.get("eligibility", "")

        female_patterns = [_wb(w) for w in ["women", "woman", "female", "girl child"]]

        male_patterns = [_wb(w) for w in ["male", "men"]]

        if any(p.search(text) for p in female_patterns):

            return "Female"

        if any(p.search(text) for p in male_patterns):

            return "Male"

        return "All"

    # --------------------------------------------------

    def extract_negative_keywords(self, scheme):
        """Use whole-word matching to avoid false positives."""
        text = " ".join([
            scheme.get("scheme_name", ""),
            scheme.get("description", "")
        ])

        words = ["fish", "fisher", "fisheries", "boat", "marine", "aquaculture"]

        return [w for w in words if _wb(w).search(text)]