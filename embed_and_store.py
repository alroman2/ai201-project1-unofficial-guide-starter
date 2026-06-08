"""
Milestone 4 — Embedding, vector store, and retrieval.

Build the store:
    python embed_and_store.py

Import in other modules:
    from embed_and_store import load_vectorstore, retrieve
"""

import chromadb
from sentence_transformers import SentenceTransformer

from ingest import chunk_documents, load_documents

COLLECTION_NAME = "daca_guide"


def build_vectorstore(
    chunks: list[dict], persist_dir: str = "chroma_db"
) -> tuple[chromadb.Collection, SentenceTransformer]:
    """Embed all chunks and persist them to ChromaDB. Overwrites any existing collection."""
    client = chromadb.PersistentClient(path=persist_dir)

    # Drop and recreate so re-runs are always clean
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(COLLECTION_NAME)
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print(f"Embedding {len(chunks)} chunks...")
    embeddings = model.encode(
        [c["text"] for c in chunks],
        show_progress_bar=True,
        convert_to_list=True,
    )

    collection.add(
        ids=[c["chunk_id"] for c in chunks],
        embeddings=embeddings,
        documents=[c["text"] for c in chunks],
        metadatas=[
            {
                "source_url": c["source_url"],
                "filename": c["filename"],
                "chunk_id": c["chunk_id"],
            }
            for c in chunks
        ],
    )

    print(f"Stored {collection.count()} chunks in '{COLLECTION_NAME}' -> {persist_dir}/")
    return collection, model


def load_vectorstore(
    persist_dir: str = "chroma_db",
) -> tuple[chromadb.Collection, SentenceTransformer]:
    """Load an existing ChromaDB collection without re-embedding."""
    client = chromadb.PersistentClient(path=persist_dir)
    collection = client.get_collection(COLLECTION_NAME)
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return collection, model


def retrieve(
    query: str,
    collection: chromadb.Collection,
    model: SentenceTransformer,
    k: int = 5,
) -> list[dict]:
    """Return the top-k most relevant chunks for a query."""
    query_embedding = model.encode([query], convert_to_list=True)
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for text, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append(
            {
                "text": text,
                "source_url": meta["source_url"],
                "filename": meta["filename"],
                "chunk_id": meta["chunk_id"],
                "distance": round(dist, 4),
            }
        )
    return chunks


def main():
    documents = load_documents()
    chunks = chunk_documents(documents)

    collection, model = build_vectorstore(chunks)

    test_queries = [
        "When should I submit my DACA renewal?",
        "Can i submit a new daca application in 2026?",
        "What happened with DACA and deportation protection in April 2026?",
    ]

    for query in test_queries:
        print(f"\n{'='*70}")
        print(f"QUERY: {query}")
        print("=" * 70)
        results = retrieve(query, collection, model, k=5)
        for i, r in enumerate(results, 1):
            print(f"\n  [{i}] distance={r['distance']}  |  {r['chunk_id']}")
            print(f"      source: {r['source_url']}")
            print(f"      {r['text'].strip()!r}")


if __name__ == "__main__":
    main()
