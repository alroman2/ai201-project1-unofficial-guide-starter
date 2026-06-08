"""
Milestone 5 — Grounded generation.

End-to-end test:
    python rag.py

Import in app.py:
    from rag import ask
"""

import os

from dotenv import load_dotenv
from groq import Groq

from embed_and_store import load_vectorstore, retrieve

load_dotenv()

# Loaded once at import time so the UI starts with a warm model
collection, model = load_vectorstore()
client = Groq(api_key=os.environ["GROQ_API_KEY"])

SYSTEM_PROMPT = """You are a helpful assistant answering questions about DACA \
(Deferred Action for Childhood Arrivals) policy and procedures in 2026.

Answer ONLY using the information in the context documents provided below. \
Do not use any knowledge from outside those documents.

If the context does not contain enough information to answer the question, \
respond with exactly:
"I don't have enough information on that based on my sources."

Do not speculate, infer, or fill gaps with general knowledge."""


def ask(question: str, k: int = 5) -> dict:
    """Return a grounded answer and its source URLs for a given question."""
    chunks = retrieve(question, collection, model, k=k)

    context_block = "\n\n".join(
        f"[{i}] (source: {c['filename']})\n{c['text']}"
        for i, c in enumerate(chunks, 1)
    )

    user_message = f"Context documents:\n{context_block}\n\nQuestion: {question}"

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
    )

    answer_text = response.choices[0].message.content

    # Sources are taken from retrieved chunks — not delegated to the LLM
    sources = list(dict.fromkeys(c["source_url"] for c in chunks))

    return {"answer": answer_text, "sources": sources}


def main():
    test_queries = [
        "When should I submit my DACA renewal?",
        "What happened with DACA and deportation in April 2026?",
        "How do I apply for a marriage-based green card?",  # out of scope
    ]

    for question in test_queries:
        print(f"\n{'='*70}")
        print(f"Q: {question}")
        print("=" * 70)
        result = ask(question)
        print(result["answer"])
        print("\nSources:")
        for url in result["sources"]:
            print(f"  - {url}")


if __name__ == "__main__":
    main()
