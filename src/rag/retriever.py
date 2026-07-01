"""
=========================================================
Sahayak AI - Retriever
=========================================================

Purpose:
    Retrieves the most relevant schemes using
    semantic search with FAISS.

Author : Prince Kumar
Project : AI Copilot for Panchayat Governance
=========================================================
"""

from src.rag.embedding_model import EmbeddingModel
from src.rag.vector_store import VectorStore


class Retriever:

    def __init__(self):

        self.embedding_model = EmbeddingModel()

        self.vector_store = VectorStore()

        self.vector_store.load()

    # --------------------------------------------------

    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ):

        query_embedding = self.embedding_model.embed([query])

        results = self.vector_store.search(

            query_embedding,

            top_k=top_k

        )

        return results


# =====================================================
# Testing
# =====================================================

if __name__ == "__main__":

    retriever = Retriever()

    while True:

        query = input("\nQuery : ")

        if query.lower() in ["exit", "quit"]:

            break

        results = retriever.retrieve(query)

        print("\nTop Results\n")

        for i, result in enumerate(results, start=1):

            print("-" * 60)

            print(f"Rank : {i}")

            print(f"Score : {result['score']:.4f}")

            print(f"Title : {result['document']['title']}")

            print(f"Category : {result['document']['metadata']['category']}")

            print(f"Level : {result['document']['metadata']['level']}")