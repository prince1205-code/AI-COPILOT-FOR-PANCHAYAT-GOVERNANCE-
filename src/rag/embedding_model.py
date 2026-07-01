"""
=========================================================
Sahayak AI - Embedding Model
=========================================================

Purpose:
    Loads SentenceTransformer model and
    generates embeddings for RAG.

Author : Prince Kumar
Project : AI Copilot for Panchayat Governance
=========================================================
"""

from sentence_transformers import SentenceTransformer


class EmbeddingModel:

    def __init__(self):

        print("\nLoading Embedding Model...\n")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("✅ Embedding Model Loaded Successfully\n")

    # --------------------------------------------------

    def embed(self, texts):

        """
        Generate embeddings.

        Parameters
        ----------
        texts : list[str] | str

        Returns
        -------
        numpy.ndarray
        """

        return self.model.encode(

            texts,

            convert_to_numpy=True,

            normalize_embeddings=True

        )


# =====================================================
# Testing
# =====================================================

if __name__ == "__main__":

    model = EmbeddingModel()

    sample = [

        "Pradhan Mantri Awas Yojana",

        "Ayushman Bharat",

        "MGNREGA"

    ]

    embeddings = model.embed(sample)

    print("=" * 60)

    print("Embedding Shape")

    print("=" * 60)

    print(embeddings.shape)

    print()

    print("First Vector (first 10 values):")

    print(embeddings[0][:10])