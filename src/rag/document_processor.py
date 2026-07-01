"""
=========================================================
Sahayak AI - Document Processor
=========================================================

Purpose:
    Convert Government Scheme dataset into
    RAG-ready documents.

Author : Prince Kumar
Project : AI Copilot for Panchayat Governance
=========================================================
"""

import json
from pathlib import Path

from src.core.config import KNOWLEDGE_BASE_DIR


class DocumentProcessor:

    def __init__(self):

        self.dataset_path = KNOWLEDGE_BASE_DIR / "clean_schemes.json"

        self.documents = []

    # --------------------------------------------------

    def load_dataset(self):

        with open(self.dataset_path, "r", encoding="utf-8") as file:

            return json.load(file)

    # --------------------------------------------------

    def create_documents(self):

        schemes = self.load_dataset()

        self.documents = []

        for scheme in schemes:

            document = f"""
Scheme Name:
{scheme.get("scheme_name","")}

Category:
{scheme.get("category","")}

Level:
{scheme.get("level","")}

Description:
{scheme.get("description","")}

Benefits:
{scheme.get("benefits","")}

Eligibility:
{scheme.get("eligibility","")}

Application Process:
{scheme.get("application_process","")}

Required Documents:
{scheme.get("required_documents","")}

Tags:
{scheme.get("tags","")}
"""

            self.documents.append({

                "id": scheme.get("slug", ""),

                "title": scheme.get("scheme_name", ""),

                "text": document,

                "metadata": {

                    "category": scheme.get("category", ""),

                    "level": scheme.get("level", "")

                }

            })

        return self.documents


# =====================================================
# Testing
# =====================================================

if __name__ == "__main__":

    processor = DocumentProcessor()

    docs = processor.create_documents()

    print("=" * 60)
    print("Document Processor")
    print("=" * 60)

    print()

    print("Total Documents :", len(docs))

    print()

    print("=" * 60)
    print("Sample Document")
    print("=" * 60)

    sample = docs[0]

    print()

    print("ID :", sample["id"])

    print()

    print("TITLE :", sample["title"])

    print()

    print(sample["text"][:1200])

    print()

    print("Metadata :", sample["metadata"])