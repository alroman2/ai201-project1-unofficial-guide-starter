"""
Milestone 3 — Document ingestion and chunking.

Usage (verification):
    python ingest.py
"""

import os
from pathlib import Path

SOURCE_METADATA: dict[str, str] = {
    "01-uscis-i821d": "https://www.uscis.gov/i-821d",
    "02-uscis-expedite-requests": "https://www.uscis.gov/forms/filing-guidance/expedite-requests",
    "04-npr-doj-daca-deportation-april-2026": "https://www.npr.org/2026/04/25/nx-s1-5798943/justice-department-makes-it-easier-to-deport-those-with-daca-status",
    "05-cnn-daca-processing-delays-may-2026": "https://www.cnn.com/2026/05/16/business/daca-processing-delays",
    "06-npr-daca-generation-limbo-may-2026": "https://www.npr.org/2026/05/19/g-s1-121405/immigration-trump-daca-generation-limbo",
    "07-presidents-alliance-uscis-policy-alert": "https://www.presidentsalliance.org/explainer-uscis-policy-alert-on-deferred-action-and-possible-implications-for-daca/",
    "08-national-immigration-forum-policy-bulletin-may-15-2026": "https://forumtogether.org/article/policy-bulletin-friday-may-15-2026/",
    "09-ilabacalaw-daca-renewal-2026": "https://ilabacalaw.com/blog/immigration-help/daca-renewal-in-2026-fees-process-and-what-every-dreamer-should-know/",
    "10-novo-legal-daca-renewal-timeline-2026": "https://www.novo-legal.com/en/news/daca-renewal-timeline-2026",
    "11-abogado-lozano-expedite-uscis-case": "https://abogadolozano.com/expedite-uscis-case-premium-processing/",
    "12-shoreline-immigration-uscis-expedite-request": "https://shorelineimmigration.com/uscis-expedite-request/",
    "13-boundless-contact-representative-uscis": "https://www.boundless.com/blog/how-to-contact-your-representative-to-speed-up-your-visa-processing-time",
    "14-ilrc-daca-resource-hub": "https://www.ilrc.org/daca",
    "15-nilc-daca-renewals-taking-longer": "https://www.nilc.org/articles/why-some-daca-renewals-are-taking-longer-and-what-you-can-do/",
    "16-immigrants-rising-steps-to-renew-daca": "https://immigrantsrising.org/resource/steps-to-renew-daca/",
    "18-reddit-uscis-writ-of-mandamus-guide": "https://www.reddit.com/r/USCIS/comments/1ho0adh/stepbystep_guide_on_how_i_filed_a_writ_of/",
    "19-reddit-daca-writ-of-mandamus": "https://www.reddit.com/r/DACA/comments/1taqsru/hey_yall_i_did_it_i_filed_a_writ_of_mandamus/",
    "20-Congressional-Inquiries-Refresher_extracted-text": "https://www.uscis.gov/sites/default/files/document/guides/Congressional-Inquiries-Refresher.pdf",
    "daca-resources-2026-extracted": "https://www.ilrc.org/daca",
}


def load_documents(docs_dir: str = "documents") -> list[dict]:
    """Load all .txt files from documents/sources/ and the documents/ root."""
    docs_path = Path(docs_dir)
    search_paths = [
        docs_path / "sources",
        docs_path,
    ]

    documents = []
    seen_files = set()

    for search_dir in search_paths:
        if not search_dir.exists():
            continue
        for txt_file in sorted(search_dir.glob("*.txt")):
            if txt_file.name in seen_files:
                continue
            seen_files.add(txt_file.name)

            text = txt_file.read_text(encoding="utf-8")
            stem = txt_file.stem
            source_url = SOURCE_METADATA.get(stem, txt_file.name)

            documents.append({
                "text": text,
                "filename": txt_file.name,
                "source_url": source_url,
            })

    return documents


def chunk_text(text: str, chunk_size: int = 2048, overlap: int = 512) -> list[str]:
    """Split text into overlapping character-level chunks."""
    chunks = []
    start = 0
    step = chunk_size - overlap
    while start < len(text):
        chunks.append(text[start: start + chunk_size])
        start += step
    return chunks


def chunk_documents(documents: list[dict]) -> list[dict]:
    """Apply chunk_text to each document and return a flat list of chunk dicts."""
    chunks = []
    for doc in documents:
        stem = Path(doc["filename"]).stem
        for i, chunk_text_content in enumerate(chunk_text(doc["text"])):
            chunks.append({
                "text": chunk_text_content,
                "source_url": doc["source_url"],
                "filename": doc["filename"],
                "chunk_id": f"{stem}_chunk_{i}",
            })
    return chunks


def main():
    documents = load_documents()
    chunks = chunk_documents(documents)

    print(f"Documents loaded : {len(documents)}")
    print(f"Total chunks     : {len(chunks)}")
    print()

    for doc in documents:
        doc_chunks = [c for c in chunks if c["filename"] == doc["filename"]]
        print(f"  {doc['filename']:<60} {len(doc['text']):>7} chars  ->  {len(doc_chunks)} chunks")

    # Overlap verification on the first multi-chunk document
    first_multi = next((d for d in documents if len(chunk_text(d["text"])) > 1), None)
    if first_multi:
        doc_chunks = [c for c in chunks if c["filename"] == first_multi["filename"]]
        tail = doc_chunks[0]["text"][-512:]
        head = doc_chunks[1]["text"][:512]
        overlap_match = tail == head
        print(f"\nOverlap check on '{first_multi['filename']}': {'PASS' if overlap_match else 'FAIL'}")

    # Metadata check: count chunks that have a real URL (not just filename fallback)
    url_chunks = sum(1 for c in chunks if c["source_url"].startswith("http"))
    print(f"Chunks with URL metadata: {url_chunks}/{len(chunks)}")

    # Save chunks to file for review (overwrites on each run)
    import json
    output_path = Path("chunks_review.json")
    output_path.write_text(json.dumps(chunks, indent=2), encoding="utf-8")
    print(f"\nChunks saved to {output_path} ({len(chunks)} total)")


if __name__ == "__main__":
    main()
