"""
=========================================================
Sahayak AI - Knowledge Loader
=========================================================

Purpose:
    Loads the Government Schemes Knowledge Base
    from enriched_schemes.json and provides search utilities.

Author : Prince Kumar
Project : AI Copilot for Panchayat Governance
=========================================================
"""

import json
from difflib import get_close_matches

from src.core.config import KNOWLEDGE_BASE_DIR


class KnowledgeLoader:
    """
    Loads and searches the Government Schemes dataset.
    """

    def __init__(self):

        self.dataset_path = KNOWLEDGE_BASE_DIR / "enriched_schemes.json"

        self.schemes = self._load_dataset()

        print(f"✅ Loaded {len(self.schemes)} schemes.")


    # --------------------------------------------------
    # Load Dataset
    # --------------------------------------------------

    def _load_dataset(self):

        with open(self.dataset_path, "r", encoding="utf-8") as file:

            return json.load(file)


    # --------------------------------------------------
    # Search Scheme
    # --------------------------------------------------
    def search_scheme(self, query: str):

        original_query = query

        query = self.clean_query(query)

        # -----------------------------
        # Exact Name Match
        # -----------------------------

        for scheme in self.schemes:

            name = scheme.get("scheme_name", "").lower()

            if query == name:
                return scheme

        # -----------------------------
        # Search in search_text
        # -----------------------------

        candidates = []

        for scheme in self.schemes:

            searchable = scheme.get("search_text", "").lower()

            score = 0

            for word in query.split():

                if word in searchable:
                    score += 1

            if score > 0:

                candidates.append((score, scheme))

        if candidates:

            candidates.sort(key=lambda x: x[0], reverse=True)

            return candidates[0][1]

        # -----------------------------
        # Fuzzy Search
        # -----------------------------

        names = [

            scheme.get("scheme_name", "")

            for scheme in self.schemes

        ]

        matches = get_close_matches(

            original_query,

            names,

            n=1,

            cutoff=0.45

        )

        if matches:

            for scheme in self.schemes:

                if scheme["scheme_name"] == matches[0]:

                    return scheme

        return None    

    def clean_query(self, query: str) -> str:
        """
        Clean natural language query into searchable keywords.
        """

        query = query.lower()

        stop_words = [
            "tell", "me", "about", "what", "is", "the",
            "of", "scheme", "schemes", "yojana",
            "please", "benefits", "benefit",
            "eligibility", "eligible",
            "information", "details",
            "explain", "give", "show",
            "for", "to", "how", "can", "i",
            "do", "know"
        ]

        for word in stop_words:
            query = query.replace(word, " ")

        return " ".join(query.split())
# ---------------------------------------------------------
# Testing
# ---------------------------------------------------------

if __name__ == "__main__":

    loader = KnowledgeLoader()

    print("=" * 60)
    print("Knowledge Loader")
    print("=" * 60)

    test_queries = [

        "Tell me about Ayushman Bharat",

        "Benefits of PM Kisan",

        "Explain Ujjwala Yojana",

        "Housing Schemes",

        "PMAY",

        "MGNREGA"

    ]
    
    for query in test_queries:

        print("\n" + "=" * 50)

        print("Searching :", query)

        result = loader.search_scheme(query)

        if result:

            print("\n✅ Scheme Found\n")

            print("Scheme Name :", result.get("scheme_name", ""))

            print("Category    :", result.get("category", ""))

            print("Level       :", result.get("level", ""))

            print("Slug        :", result.get("slug", ""))

        else:

            print("\n❌ No Scheme Found")


    print("\n================ DEBUG ================\n")

    count = 0

    for scheme in loader.schemes:

        if "ayushman" in scheme.get("search_text", "").lower():

            count += 1

            print(scheme["scheme_name"])

    print("\nTotal Matches :", count)