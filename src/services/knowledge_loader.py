"""
=========================================================
Sahayak AI - Knowledge Loader
=========================================================

Purpose:
    Load and manage the Government Knowledge Base
    stored as JSON files.

Author : Prince Kumar
Project : AI Copilot for Panchayat Governance
=========================================================
"""

import json
from pathlib import Path

from src.core.config import KNOWLEDGE_BASE_DIR


class KnowledgeLoader:
    """
    Loads JSON files from the knowledge base.
    """

    def __init__(self):

        self.scheme_directory = KNOWLEDGE_BASE_DIR / "schemes"

    def load_scheme(self, filename: str):
        """
        Load a single scheme JSON file.

        Parameters
        ----------
        filename : str

        Returns
        -------
        dict
        """

        file_path = self.scheme_directory / filename

        if not file_path.exists():

            raise FileNotFoundError(
                f"{filename} not found."
            )

        with open(file_path, "r", encoding="utf-8") as file:

            data = json.load(file)

        return data

    def load_all_schemes(self):

        schemes = []

        print("Searching in:", self.scheme_directory)

        files = list(self.scheme_directory.glob("*.json"))

        print("Files Found:", files)

        for file in files:

            with open(file, "r", encoding="utf-8") as f:
                schemes.append(json.load(f))

        return schemes
    
    def search_scheme(self, keyword: str):
        """
        Search a scheme by multiple fields.

        Parameters
        ----------
        keyword : str

        Returns
        -------
        dict | None
        """

        keyword = keyword.lower().strip()

        schemes = self.load_all_schemes()

        for scheme in schemes:

            searchable_text = " ".join([
                scheme.get("scheme_name", ""),
                scheme.get("scheme_id", ""),
                scheme.get("category", ""),
                scheme.get("description", ""),
                scheme.get("objective", ""),
                " ".join(scheme.get("keywords", []))
            ]).lower()

            if keyword in searchable_text:
                return scheme

        return None
    
# ---------------------------------------------------------
# Testing
# ---------------------------------------------------------
if __name__ == "__main__":

    loader = KnowledgeLoader()

    print("=" * 60)
    print("Knowledge Loader")
    print("=" * 60)

    test_queries = [

        "PMAY",

        "Housing",

        "Awas",

        "Home",

        "House"

    ]

    for query in test_queries:

        result = loader.search_scheme(query)

        print(f"\nSearching : {query}")

        if result:
            print("Found :", result["scheme_name"])
        else:
            print("Not Found")