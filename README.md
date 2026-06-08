# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

This system covers **DACA (Deferred Action for Childhood Arrivals) policy, procedures, and 2026 developments** for recipients and advocates navigating the renewal process. The knowledge is valuable because the official USCIS website describes the formal rules but does not explain what actually happens when cases are delayed, what escalation tactics work in practice, or how rapidly-changing 2026 policy memos affect recipients. A person trying to figure out whether to file a Writ of Mandamus or submit a congressional inquiry will find USCIS.gov unhelpful which is information not supplied by USCIS. The system also covers reddit discussions that may me provide anecdotal information.

---

## Document Sources

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | USCIS — Form I-821D | Official government page | https://www.uscis.gov/i-821d |
| 2 | USCIS — Expedite Requests | Official government page | https://www.uscis.gov/forms/filing-guidance/expedite-requests |
| 3 | USCIS Congressional Inquiries Refresher | Official PDF guide | https://www.uscis.gov/sites/default/files/document/guides/Congressional-Inquiries-Refresher.pdf |
| 4 | NPR — DOJ Makes It Easier to Deport DACA Recipients (Apr 2026) | News article | https://www.npr.org/2026/04/25/nx-s1-5798943/justice-department-makes-it-easier-to-deport-those-with-daca-status |
| 5 | CNN Business — DACA Processing Delays (May 2026) | News article | https://www.cnn.com/2026/05/16/business/daca-processing-delays |
| 6 | NPR — DACA Recipients Stuck in Limbo (May 2026) | News feature | https://www.npr.org/2026/05/19/g-s1-121405/immigration-trump-daca-generation-limbo |
| 7 | Presidents' Alliance — USCIS Policy Alert Explainer | Nonprofit explainer | https://www.presidentsalliance.org/explainer-uscis-policy-alert-on-deferred-action-and-possible-implications-for-daca/ |
| 8 | National Immigration Forum — Policy Bulletin May 15, 2026 | Nonprofit bulletin | https://forumtogether.org/article/policy-bulletin-friday-may-15-2026/ |
| 9 | Ilabacalaw — DACA Renewal 2026: Fees, Process & Tips | Attorney blog | https://ilabacalaw.com/blog/immigration-help/daca-renewal-in-2026-fees-process-and-what-every-dreamer-should-know/ |
| 10 | Novo Legal — DACA Renewal Timeline 2026 | Attorney guide | https://www.novo-legal.com/en/news/daca-renewal-timeline-2026 |
| 11 | Abogado Lozano — How to Expedite Your USCIS Case 2026 | Attorney guide | https://abogadolozano.com/expedite-uscis-case-premium-processing/ |
| 12 | Shoreline Immigration — 2026 USCIS Expedite Request Guide | Attorney guide | https://shorelineimmigration.com/uscis-expedite-request/ |
| 13 | Boundless — How to Contact Your Representative | Nonprofit guide | https://www.boundless.com/blog/how-to-contact-your-representative-to-speed-up-your-visa-processing-time |
| 14 | ILRC — DACA Resource Hub | Nonprofit hub | https://www.ilrc.org/daca |
| 15 | NILC — Why DACA Renewals Are Taking Longer & What to Do | Nonprofit guide | https://www.nilc.org/articles/why-some-daca-renewals-are-taking-longer-and-what-you-can-do/ |
| 16 | Immigrants Rising — Steps to Renew DACA | Nonprofit checklist | https://immigrantsrising.org/resource/steps-to-renew-daca/ |
| 17 | TheDream.US — DACA Renewal Delays 2026 | Nonprofit PDF report | https://www.thedream.us/wp-content/uploads/2026/03/DACA-RENEWAL-DELAYS-2026.pdf |
| 18 | r/USCIS — Step-by-Step: How I Filed a Writ of Mandamus | Reddit thread | https://www.reddit.com/r/USCIS/comments/1ho0adh/stepbystep_guide_on_how_i_filed_a_writ_of/ |
| 19 | r/DACA — "I Filed a Writ of Mandamus" | Reddit thread | https://www.reddit.com/r/DACA/comments/1taqsru/hey_yall_i_did_it_i_filed_a_writ_of_mandamus/ |

---

## Chunking Strategy

**Chunk size:** 2,048 characters

**Overlap:** 512 characters

**Why these choices fit your documents:** The documents are of mixed types, qualities, and lengths. However because of the legal nature of the questions, maintaining context is critical. This is why a larger chuck size was chosen, however, this points a critical flaw in this chunking strategy for this such documents - that is, we should probably use recursive chunking to avoid splitting important chunks that may contain legal information. 

**Final chunk count:** 347 chunks across 19 source documents. Run `python ingest.py`.

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` via `sentence-transformers`

**Production tradeoff reflection:** `all-MiniLM-L6-v2` is a fast, lightweight model (22M parameters) with a 256-token context window, sufficient for 2,048-character chunks because most chunks average 300–400 tokens, but any chunk near the upper boundary gets silently truncated, potentially losing the last paragraph. For a production deployment, I would evaluate `text-embedding-3-large` (OpenAI) or a multilingual model like `paraphrase-multilingual-mpnet-base-v2`, which supports Spanish which is important here because many DACA recipients are Spanish-dominant and would benefit from querying in their native language. A larger model also handles legal terminology better: phrases like "deferred action," "BIA precedent decision," and "writ of mandamus" are domain-specific and may not be well-separated in a general-purpose small model's embedding space. The main tradeoff is latency and cost: a larger API-hosted embedding model is slower and adds per-token cost at query time, which matters if the guide is queried hundreds of times per day.

---

## Grounded Generation

**System prompt grounding instruction:** The system prompt passed to the LLM in `rag.py` reads:

> *"Answer ONLY using the information in the context documents provided below. Do not use any knowledge from outside those documents. If the context does not contain enough information to answer the question, respond with exactly: 'I don't have enough information on that based on my sources.' Do not speculate, infer, or fill gaps with general knowledge."*

This instructs the model to treat the retrieved chunks as the sole permitted knowledge source and to fail loudly (with a fixed string) rather than silently hallucinate when context is insufficient.

**How source attribution is surfaced in the response:** Source attribution is not delegated to the LLM — the `ask()` function in `rag.py` independently collects the `source_url` field from every retrieved chunk and returns them as a deduplicated list. The Gradio UI displays these URLs under a "Retrieved from" label, separate from the answer text. This means even if the LLM's answer omits citations, the user always sees which documents were consulted.

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Can I submit a new DACA application? | You can file one, but USCIS has paused processing all new (first-time) applications as of 2026. | "I don't have enough information on that based on my sources." | Partially relevant — retrieved renewal guides, not new-application sources | Inaccurate |
| 2 | If I already have DACA, when should I submit my renewal? | At least 120–150 days before your current DACA expires. | File 150–120 days before expiration; one source adds an ideal window of 180–120 days and categories for acceptable/urgent/expired timelines. | Relevant, retrieved renewal timeline guides and nonprofit checklists | Accurate |
| 3 | What can I do if my DACA renewal has been pending for over 6 months? | Escalation options in order: (1) expedite request to USCIS, (2) congressional inquiry, (3) USCIS Ombudsman, (4) Writ of Mandamus. | "I don't have enough information on that based on my sources." | Partially relevant — retrieved general renewal/delay sources but not the expedite-specific guides that contain the escalation ladder | Inaccurate |
| 4 | What happened with DACA and deportation protection in April 2026? | The DOJ/BIA issued a ruling that DACA status alone no longer prevents deportation. | The Board of Immigration Appeals published a precedent decision that DACA status is not sufficient grounds for deportation relief; case involved Catalina "Xochitl" Santiago. | Relevant — retrieved the NPR article directly covering the ruling | Accurate |
| 5 | Can you tell me whether I specifically qualify for DACA or give me legal advice on my case? | No, this guide provides general information only; consult a licensed immigration attorney. | "I don't have enough information on that based on my sources." | Off-target, retrieved general DACA policy documents rather than chunks containing legal-disclaimer language | Partially accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

**Question that failed:** Q3 — "What can I do if my DACA renewal has been pending for over 6 months?"

**What the system returned:** "I don't have enough information on that based on my sources."

**Root cause (tied to a specific pipeline stage):** The failure originates in the **retrieval stage** — specifically, a vocabulary mismatch between the user's query language and the language used in the most relevant documents. The query uses the phrase "pending for over 6 months," which describes a delay situation. The documents that contain the escalation steps (sources 11, 12, and 13 — the Abogado Lozano expedite guide, Shoreline Immigration's expedite request walkthrough, and the Boundless congressional inquiry guide) use terms like "expedite request," "congressional casework inquiry," and "writ of mandamus." The `all-MiniLM-L6-v2` embedding model maps the user's "pending for over 6 months" into a vector space region closer to renewal-timeline content (sources 9, 10, 16) than to expedite-specific procedural content. As a result, the top-5 retrieved chunks came from general renewal guides that describe the standard timeline but do not explain what to do when that timeline is far exceeded. The LLM received no chunks containing the expedite or mandamus options, and correctly — but unhelpfully — responded that it had no information.

A secondary contributing factor is that the 2,048-character chunks from the NILC source (source 15 — "Why Some DACA Renewals Are Taking Longer And What You Can Do") were retrieved, but the specific chunk that reached the model covered background on the delay causes rather than the action steps, which appeared in a later section of the same document that was cut into a separate chunk ranked below the top-5 cutoff.

**What you would change to fix it:** Two targeted fixes: (1) increase `k` from 5 to 7–8 to widen the retrieval window and give more document sections a chance to surface. Changing the ingestion to use recursive chunking could also help tighten the ideas across chunks, which would improve the vector space, and the LLM has better chunks to pcik from

---

## Spec Reflection

**One way the spec helped you during implementation:** Planning took the longest amount of time by a lot, but it provided a guided method to defining the system. It also helped me understand the system that was being created, and I could interrupt and verify the ai code assistant.

**One way your implementation diverged from the spec, and why:** The spec called for top-k = 3 chunks per query, but implementation considered 5-7 to provide more context. The context size for 5-7 chunks is still small.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* The Chunking Strategy section from planning.md (chunk_size=2048, overlap=512) and the list of 19 source URLs/file paths from the Documents table, along with the requirement to attach source URL metadata to every chunk.
- *What it produced:* A complete `ingest.py` with `load_documents()` (reads `.txt` files from `documents/sources/` and `documents/`), `chunk_text(text, chunk_size=2048, overlap=512)` using character-level splitting, and `chunk_documents()` that flattens document chunks into a list of dicts with `text`, `source_url`, `filename`, and `chunk_id` fields. It also included a `main()` with verification output (overlap check, URL metadata count) and wrote chunks to `chunks_review.json`.
- *What I changed or overrode:* The initial version only searched `documents/sources/`. I directed Claude to also search the `documents/` root directory (where `daca-resources-2026-extracted.txt` lives) and deduplicate by filename, because the ILRC consolidated file is at the root level and would have been silently skipped. I also added the `SOURCE_METADATA` dict manually to map stem names to canonical URLs, because the generated code initially used the filename as the fallback source identifier, which would have made source attribution meaningless in the UI.

**Instance 2**

- *What I gave the AI:* The Retrieval Approach section from planning.md (embedding model `all-MiniLM-L6-v2`, top-k=3), the `retrieve()` function signature from `embed_and_store.py`, and the legal-disclaimer requirement surfaced by evaluation question 5 (no legal advice on specific cases).
- *What it produced:* A `rag.py` with an `ask(question, k=5)` function that calls `retrieve()`, builds a numbered context block (`[1] (source: filename)...`), calls the Groq API with `llama-3.3-70b-versatile`, and returns both the answer text and a deduplicated source URL list. It also included a hard refusal string in the system prompt and a `main()` with three test queries.
- *What I changed or overrode:* Two overrides. First, I changed `k` from 3 (per the spec) to 5 after observing during testing that 3 chunks frequently missed multi-part answers. Second, the initial system prompt said "use only the provided context" but did not specify the exact fallback string to return when context was insufficient — I directed Claude to add the exact phrase `"I don't have enough information on that based on my sources."` as a literal instruction, so the LLM's refusal would be predictable and identifiable in automated evaluation rather than varying in phrasing each run.
