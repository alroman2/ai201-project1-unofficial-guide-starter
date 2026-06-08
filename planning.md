# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | USCIS — Form I-821D (Official) | Official USCIS page for DACA renewals: current form, instructions, eligibility, and $495 fee breakdown | https://www.uscis.gov/i-821d |
| 2 | USCIS — Expedite Requests (Official) | Official USCIS guidance on qualifying criteria and how to submit an expedite request | https://www.uscis.gov/forms/filing-guidance/expedite-requests |
| 3 | USCIS — Congressional Inquiries Refresher (PDF) | USCIS internal guide for congressional staff explaining how inquiries are processed and prioritized | https://www.uscis.gov/sites/default/files/document/guides/Congressional-Inquiries-Refresher.pdf |
| 4 | NPR — DOJ Makes It Easier to Deport DACA Recipients (Apr 2026) | Covers the April 2026 DOJ/BIA ruling that DACA status alone no longer protects against deportation | https://www.npr.org/2026/04/25/nx-s1-5798943/justice-department-makes-it-easier-to-deport-those-with-daca-status |
| 5 | CNN Business — DACA Processing Delays (May 2026) | Reports on renewal wait times surging 400–1000%, causing work authorization gaps for recipients | https://www.cnn.com/2026/05/16/business/daca-processing-delays |
| 6 | NPR — DACA Recipients Stuck in Limbo (May 2026) | In-depth feature on the human impact of DACA policy uncertainty for long-term recipients | https://www.npr.org/2026/05/19/g-s1-121405/immigration-trump-daca-generation-limbo |
| 7 | Presidents' Alliance — USCIS Policy Alert Explainer | Breaks down the May 8, 2026 USCIS memo tightening deferred action grants and its effect on renewals | https://www.presidentsalliance.org/explainer-uscis-policy-alert-on-deferred-action-and-possible-implications-for-daca/ |
| 8 | National Immigration Forum — Policy Bulletin May 15, 2026 | Weekly digest covering the latest DACA and immigration policy developments | https://forumtogether.org/article/policy-bulletin-friday-may-15-2026/ |
| 9 | Ilabacalaw — DACA Renewal 2026: Fees, Process & Tips | Attorney guide covering required forms, fees, stricter 2026 background check requirements, and timeline advice | https://ilabacalaw.com/blog/immigration-help/daca-renewal-in-2026-fees-process-and-what-every-dreamer-should-know/ |
| 10 | Novo Legal — DACA Renewal Timeline 2026 | Covers when to file (120–150 days before expiration), document checklist, and case tracking tips | https://www.novo-legal.com/en/news/daca-renewal-timeline-2026 |
| 11 | Abogado Lozano — How to Expedite Your USCIS Case 2026 | Covers all expedite strategies: discretionary request, premium processing, congressional inquiry, Ombudsman, and mandamus | https://abogadolozano.com/expedite-uscis-case-premium-processing/ |
| 12 | Shoreline Immigration — 2026 USCIS Expedite Request Guide | Step-by-step guide on drafting an expedite request, what evidence to include, and common denial mistakes | https://shorelineimmigration.com/uscis-expedite-request/ |
| 13 | Boundless — How to Contact Your Representative to Speed Up USCIS Processing | Plain-language guide on submitting a congressional casework inquiry and what to expect | https://www.boundless.com/blog/how-to-contact-your-representative-to-speed-up-your-visa-processing-time |
| 14 | ILRC — DACA Resource Hub (Nonprofit) | Central DACA hub with May 2026 practice alert, free eligibility toolkits, and guides for applicants and advocates | https://www.ilrc.org/daca |
| 15 | NILC — Why DACA Renewals Are Taking Longer & What to Do | Practical guide on documenting delays, submitting congressional inquiries, and escalating stalled cases | https://www.nilc.org/articles/why-some-daca-renewals-are-taking-longer-and-what-you-can-do/ |
| 16 | Immigrants Rising — Steps to Renew DACA (Nonprofit) | Plain-language nonprofit renewal checklist designed for students and young adults | https://immigrantsrising.org/resource/steps-to-renew-daca/ |
| 17 | TheDream.US — DACA Renewal Delays 2026 (PDF) | March 2026 downloadable report documenting delay causes and recommended action steps including congressional outreach | https://www.thedream.us/wp-content/uploads/2026/03/DACA-RENEWAL-DELAYS-2026.pdf |
| 18 | r/USCIS — Step-by-Step Guide: How I Filed a Writ of Mandamus | Detailed first-person Reddit post with templates and tips for filing a mandamus lawsuit to force USCIS action | https://www.reddit.com/r/USCIS/comments/1ho0adh/stepbystep_guide_on_how_i_filed_a_writ_of/ |
| 19 | r/DACA — "I Filed a Writ of Mandamus" (Reddit Thread) | DACA-specific first-person mandamus account with community Q&A on timelines, attorney costs, and outcomes | https://www.reddit.com/r/DACA/comments/1taqsru/hey_yall_i_did_it_i_filed_a_writ_of_mandamus/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:** 2048

**Overlap:** 512

**Reasoning:**
There are guides including blogs, official u.s government documentation, and reddit threads that go back and forth. A longer baseline chunking helps preserve context in each chunk which is important fo accuracy for legal questions.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     all-MiniLM-L6-v2
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:** all-MiniLM-L6-v2

**Top-k:**3

**Production tradeoff reflection:**

If cost were not a contrain, i would run a much larger embeddings model that can support 8192 context such as text-embedding-3-large. It should also contain spanish, korean, and multiple other languages as end user might want to as questions in native language.


---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | Can i submit a new daca application | Kind of, as of 2026 you may submit a new application but processing of allnew applications has been paused.|
| 2 | If I already have daca, when should i submit my renewal | You should submit at least 120-150 days before your expiration date. |
| 3 | What can I do if my DACA renewal has been pending for over 6 months? | You have several escalation options in order: (1) submit a discretionary expedite request to USCIS with documentation of financial harm, (2) contact your U.S. representative's casework office to submit a congressional inquiry, (3) file a complaint with the USCIS Ombudsman, and (4) consult an attorney about filing a Writ of Mandamus. |
| 4 | What happened with DACA and deportation protection in April 2026? | The DOJ and Board of Immigration Appeals issued a ruling in April 2026 establishing that holding DACA status alone is no longer sufficient to prevent deportation. Recipients can still be removed, and the ruling made it easier for immigration authorities to initiate deportation proceedings. |
| 5 | Can you tell me whether I specifically qualify for DACA or give me legal advice on my case? | No. This guide provides general educational information only and is not a substitute for legal advice. Immigration law is complex and individual circumstances vary — you should consult a licensed immigration attorney for advice specific to your situation. |
| 6 | What type of evidence do the Reddit sources provide compared to the official government pages and nonprofit legal guides? | Reddit sources provide first-person accounts and lived experiences from DACA recipients — such as filing a Writ of Mandamus — offering practical, anecdotal insight. Official USCIS pages and nonprofit guides from ILRC and NILC provide authoritative, policy-based information grounded in law and formal procedure. Both types are useful but should be weighted differently: official sources for accuracy on rules and deadlines, Reddit for real-world context and process tips. |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Mixed source quality implies that official uscis documentation is higher than reddit threads which might lead to varied asnwer quality.
2.Inconsistent formats such as threads, blogs, and guides can lead to weird chunks when using fixed size chunking

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->


**Milestone 3 — Ingestion and chunking:**

- **AI tool:** Claude
- **Input:** The Chunking Strategy section of this planning.md (chunk size 2048, overlap 512) plus the list of 19 source URLs/file paths from the Documents table
- **Expected output:** A `ingest.py` script with a `load_documents()` function that fetches/reads each source and a `chunk_text(text, chunk_size=2048, overlap=512)` function that returns a list of text chunks with source metadata attached
- **Verification:** Run the script against 2–3 sources and print chunk count + first/last 100 chars of each chunk to confirm size and overlap are correct; confirm no chunk drops the source URL from its metadata

**Milestone 4 — Embedding and retrieval:**

- **AI tool:** Claude
- **Input:** The Retrieval Approach section (model: all-MiniLM-L6-v2, top-k: 3) and the output chunks + metadata schema from Milestone 3
- **Expected output:** An `embed_and_store.py` script that embeds all chunks with `sentence-transformers` and persists them to a ChromaDB collection, plus a `retrieve(query, k=3)` function that returns the top-3 chunks with their source URLs
- **Verification:** Run the 6 evaluation questions from the Evaluation Plan and confirm that at least one returned chunk per question contains text clearly relevant to the expected answer; spot-check that source URLs are preserved in results

**Milestone 5 — Generation and interface:**

- **AI tool:** Claude
- **Input:** The Evaluation Plan section (6 test Q&A pairs), the `retrieve()` function signature from Milestone 4, and the disclaimer requirement from question 5 (no legal advice)
- **Expected output:** A `rag.py` script with an `answer(query)` function that calls `retrieve()`, builds a prompt with the retrieved chunks as context, calls the Claude API, and returns a response; plus a minimal CLI loop so the guide can be queried interactively
- **Verification:** Run all 6 evaluation questions through the CLI and manually score each response against the expected answers in the Evaluation Plan; confirm question 5 always triggers the legal-advice disclaimer regardless of phrasing
