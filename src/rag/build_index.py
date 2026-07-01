"""
=========================================================
Sahayak AI - Build Vector Index
=========================================================

Purpose:
    Build FAISS vector index from Government Schemes.

Author : Prince Kumar
Project : AI Copilot for Panchayat Governance
=========================================================
"""

from src.rag.document_processor import DocumentProcessor
from src.rag.embedding_model import EmbeddingModel
from src.rag.vector_store import VectorStore


def main():

    print("=" * 60)
    print("Building Vector Index")
    print("=" * 60)

    # --------------------------------------------------
    # Load Documents
    # --------------------------------------------------

    processor = DocumentProcessor()

    documents = processor.create_documents()

    print(f"\nLoaded Documents : {len(documents)}")

    # --------------------------------------------------
    # Generate Embeddings
    # --------------------------------------------------

    model = EmbeddingModel()

    texts = [

        document["text"]

        for document in documents

    ]

    print("\nGenerating Embeddings...")

    embeddings = model.embed(texts)

    print("Embeddings Shape :", embeddings.shape)

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    metadata = []

    for document in documents:

        metadata.append({

            "id": document["id"],

            "title": document["title"],

            "text": document["text"],

            "metadata": document["metadata"]

        })

    # --------------------------------------------------
    # Build FAISS Index
    # --------------------------------------------------

    store = VectorStore()

    store.create_index(

        embeddings,

        metadata

    )

    store.save()

    print("\n" + "=" * 60)

    print("RAG Index Built Successfully")

    print("=" * 60)


if __name__ == "__main__":

    main()