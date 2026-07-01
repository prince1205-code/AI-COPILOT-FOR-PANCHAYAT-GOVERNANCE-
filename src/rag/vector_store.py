"""
=========================================================
Sahayak AI - Vector Store
=========================================================

Purpose:
    Handles FAISS vector index creation,
    saving, loading and searching.

Author : Prince Kumar
Project : AI Copilot for Panchayat Governance
=========================================================
"""

import json
from pathlib import Path

import faiss
import numpy as np

from src.core.config import KNOWLEDGE_BASE_DIR


class VectorStore:

    def __init__(self):

        self.index = None

        self.dimension = None

        self.metadata = []

        self.vector_dir = KNOWLEDGE_BASE_DIR / "vector_store"

        self.vector_dir.mkdir(exist_ok=True)

        self.index_path = self.vector_dir / "faiss.index"

        self.metadata_path = self.vector_dir / "metadata.json"

    # --------------------------------------------------

    def create_index(self,
                     embeddings: np.ndarray,
                     metadata: list):

        """
        Create FAISS index.
        """

        self.dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatIP(self.dimension)

        self.index.add(embeddings.astype("float32"))

        self.metadata = metadata

        print(f"✅ Index Created ({self.index.ntotal} vectors)")

    # --------------------------------------------------

    def save(self):

        """
        Save FAISS index and metadata.
        """

        faiss.write_index(

            self.index,

            str(self.index_path)

        )

        with open(

            self.metadata_path,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                self.metadata,

                file,

                indent=4,

                ensure_ascii=False

            )

        print("✅ Vector Store Saved")

    # --------------------------------------------------

    def load(self):

        """
        Load FAISS index.
        """

        self.index = faiss.read_index(

            str(self.index_path)

        )

        with open(

            self.metadata_path,

            "r",

            encoding="utf-8"

        ) as file:

            self.metadata = json.load(file)

        print(

            f"✅ Loaded {self.index.ntotal} vectors."

        )

    # --------------------------------------------------

    def search(self,
               query_embedding,
               top_k: int = 5):

        """
        Search similar vectors.
        """

        scores, indices = self.index.search(

            query_embedding.astype("float32"),

            top_k

        )

        results = []

        for score, idx in zip(

            scores[0],

            indices[0]

        ):

            if idx == -1:

                continue

            results.append({

                "score": float(score),

                "document": self.metadata[idx]

            })

        return results


# =====================================================
# Testing
# =====================================================

if __name__ == "__main__":

    print("=" * 60)

    print("Vector Store")

    print("=" * 60)

    store = VectorStore()

    print()

    print("Vector Directory:")

    print(store.vector_dir)