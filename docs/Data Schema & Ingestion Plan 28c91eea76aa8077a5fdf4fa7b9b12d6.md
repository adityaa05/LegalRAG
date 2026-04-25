# Data Schema & Ingestion Plan

# 1) Goals for this phas

- Produce a normalized, timestamped corpus of Indian law sections with clean text and structured metadata.
- Chunk and embed the corpus for semantic retrieval while preserving provenance.
- Attach structured legal attributes required for the Red/Yellow/Green severity engine.
- Provide QA and validation steps so Mira can detect ingestion errors early.

---

# 2) Metadata schema (single canonical record)

Use this JSON schema for every stored chunk/document.

```json
{
  "id": "ipc_302_section_1_chunk_0001",
  "act": "Indian Penal Code",
  "act_slug": "ipc",
  "section": "302",
  "section_title": "Punishment for murder",
  "jurisdiction": "India - Central",
  "text": "Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine.",
  "text_cleaned": "Whoever commits murder shall be punished with death or imprisonment for life and liable to fine.",
  "chunk_index": 0,
  "chunk_tokens": 120,
  "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
  "source_url": "https://www.indiacode.nic.in/handle/123456789/302",
  "source_date": "2024-07-01",
  "ingested_at": "2025-10-15T08:12:34+05:30",
  "version": "v1.0",
  "offense_type": "murder",
  "bailable": "No",
  "cognizable": "Yes",
  "max_penalty_years": 0,
  "min_penalty_years": 0,
  "penalty_type": "death|life_imprisonment|fine",
  "severity_label_candidate": "RED",
  "notes": "statute text; needs review for amendments"
}

```

Notes:

- `max_penalty_years` = 0 indicates capital punishment or life; keep special flags for life/death.
- `penalty_type` is a pipe-separated summary for quick rule parsing.
- `severity_label_candidate` is the output of the rule-based mapping; the final system should show the label and the rule that produced it.

---

# 3) Chunking & text processing rules

- Target chunk size: **400–700 tokens** (approx 2500–4500 characters) per chunk. This keeps retrieval context focused while leaving room in LLM prompt.
- Overlap: **50–100 tokens** overlap between adjacent chunks to preserve context across long sections.
- Keep natural boundaries: prefer splitting at paragraph, subsection, or clause boundaries rather than mid-sentence. If a single section is short, keep it unchunked.
- Preserve numbering/labels: keep "Section 302", sub-clauses (1), (a), (b). This improves traceability.
- Clean steps:
    - Strip HTML tags, navigation boilerplate, and duplicated headings.
    - Normalize whitespace and punctuation.
    - Resolve unicode issues, convert smart quotes to plain quotes.
    - Preserve original text in `text` and cleaned in `text_cleaned`.
- Language: if source contains bilingual text, store both versions in separate fields `text_en` and `text_local` and embed `text_en` for semantic search. For MVP use English only if available.

---

# 4) Required metadata fields (short list)

- id, act, section, section_title, jurisdiction, source_url, source_date, ingested_at, version.
- text, text_cleaned, chunk_index, chunk_tokens, embedding_model.
- legal attributes: offense_type, bailable (Yes/No/Unknown), cognizable (Yes/No/Unknown), max_penalty_years, penalty_type.
- provenance & audit: source_date, ingested_at, version, notes.

---

# 5) Severity mapping rules (Red / Yellow / Green)

Design the severity engine as a deterministic rule-based mapper using `bailable`, `cognizable`, and `max_penalty_years` and explicit penalty types. LLM may only validate or surface exceptions.

Suggested rules (tuneable):

- **RED** (High severity)
    - Any statute where `bailable == "No"`.
    - OR `penalty_type` includes `death` or `life_imprisonment`.
    - OR `max_penalty_years >= 10`.
    - Examples: IPC 302 (murder), NDPS heavy penalties.
- **YELLOW** (Moderate severity)
    - `bailable == "Yes"` but `max_penalty_years >= 3 and < 10`.
    - Or cognizable serious offenses with imprisonment 1–10 years.
    - Examples: grievous hurt with several years imprisonment.
- **GREEN** (Low severity)
    - `max_penalty_years < 3` or `penalty_type` = `fine` only or traffic violations.
    - Petty offenses, regulatory non-criminal violations.
- **Fallback / Unknown**
    - If fields are missing, label `UNKNOWN` and require human review. The UI should show `UNKNOWN` and a prompt to "View source" rather than an R/Y/G badge.

Store the mapping as a small JSON table so it can be updated without code changes.

---

# 6) Ingestion pipeline (high-level steps)

1. **Source discovery**
    - Identify canonical source pages on indiacode.nic.in or official gazette. Keep a seeds list per act.
2. **Download / scrape**
    - Use a robust scraper that respects robots.txt and rate limits. Prefer bulk download when available. Prefer official APIs or data dumps.
3. **Parse & normalize**
    - Extract section id, title, subsections. Clean text. Extract dates (enactment & amendments).
4. **Annotate legal attributes**
    - Heuristic extraction: parse the penalty clause text to extract numeric years, words like "life", "death", "fine" and keywords "bailable", "non-bailable", "cognizable". For edge cases, mark `Unknown`.
5. **Chunk**
    - Split per rules in Section 3.
6. **Generate embeddings**
    - Use `sentence-transformers/all-MiniLM-L6-v2` for MVP. Batch embeddings to reduce API calls.
7. **Insert into vector DB**
    - Chroma local collection with metadata fields. Use `id` as unique key.
8. **Index verification & QA**
    - Run sample queries and seeded retrieval tests. Validate that the top-k contains the expected section.
9. **Version & store snapshots**
    - Keep a snapshot of the raw scraped files and the cleaned JSON dataset in `/data/corpus/v1/` with checksums. Keep a `manifest.json` listing counts and ingest_time.

---

# 7) Validation & QA checks (automation)

- **Checksum & row counts**: track expected counts per act. Alert if counts fall by >2%.
- **Seed query retrieval test**: a test set of 200 canonical Q→expected section pairs. Require top-5 recall >= 95% for deployment.
- **Severity audit**: human review of 200 random sections to check bailable/cognizable mapping. Target <= 3% mismatch.
- **Citation integrity test**: when LLM answers, ensure returned quote substring exists verbatim in the cited chunk. Create unit test for this.
- **Edge case tests**: sections mentioning multiple penalties, compound sentences, and amendments. Flag for manual resolution.

---

# 8) Storage & vector DB schema (Chroma recommended)

Chroma collection document fields:

- `id` (pk)
- `embedding` (vector)
- `document` (text_cleaned or text_en)
- `metadata` (the JSON metadata above)

Index by cosine similarity. Persist collection on disk and snapshot nightly.

---

# 9) Sample ingestion code (Python, runnable pseudocode)

This is a minimal end-to-end snippet for cleaning, chunking, embedding, and inserting into Chroma.

```python
# pip install beautifulsoup4 requests nltk sentence-transformers chromadb
from bs4 import BeautifulSoup
import requests
import re
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
import json
import time
from datetime import datetime

EMB_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
embedder = SentenceTransformer(EMB_MODEL)

client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma_db"))
collection = client.get_or_create_collection("india_laws")

def fetch_html(url):
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    return r.text

def extract_sections_from_html(html, source_url):
    soup = BeautifulSoup(html, "html.parser")
    # site-specific parsing here. Example:
    sections = []
    for sec in soup.select(".section"):  # placeholder selector
        sec_id = sec.select_one(".secnum").get_text(strip=True)
        title = sec.select_one(".title").get_text(strip=True)
        text = " ".join(p.get_text(" ", strip=True) for p in sec.select("p"))
        sections.append({"id": f"{source_url}#{sec_id}", "section": sec_id, "title": title, "text": text})
    return sections

def clean_text(text):
    text = re.sub(r'\s+', ' ', text).strip()
    # additional normalization
    return text

def chunk_text(text, max_tokens=600, overlap_sentences=2):
    sentences = sent_tokenize(text)
    chunks = []
    cur = []
    for s in sentences:
        cur.append(s)
        approx_tokens = sum(len(x.split()) for x in cur)
        if approx_tokens >= max_tokens:
            chunks.append(" ".join(cur))
            cur = cur[-overlap_sentences:]
    if cur:
        chunks.append(" ".join(cur))
    return chunks

def extract_penalty_attributes(text):
    # simple heuristics: look for years, life, death, bailable
    attr = {"bailable":"Unknown","cognizable":"Unknown","max_penalty_years": None, "penalty_type": ""}
    if re.search(r'\blife\b', text, re.I):
        attr["penalty_type"] += "life_imprisonment|"
    if re.search(r'\bdeath\b|\bcapital punishment\b', text, re.I):
        attr["penalty_type"] += "death|"
    yrs = re.findall(r'(\d+)\s+years?', text)
    yrs = [int(x) for x in yrs]
    if yrs:
        attr["max_penalty_years"] = max(yrs)
    if re.search(r'non-?bailable|not bailable', text, re.I):
        attr["bailable"] = "No"
    if re.search(r'\bbailable\b', text, re.I):
        attr["bailable"] = "Yes"
    if re.search(r'\bcognizable\b', text, re.I):
        attr["cognizable"] = "Yes"
    return attr

def ingest_section(section, source_url, act_slug):
    cleaned = clean_text(section['text'])
    chunks = chunk_text(cleaned)
    docs = []
    for i, c in enumerate(chunks):
        attrs = extract_penalty_attributes(c)
        meta = {
            "id": f"{act_slug}_{section['section']}_chunk_{i:04d}",
            "act": section.get("act", "Indian Law"),
            "act_slug": act_slug,
            "section": section["section"],
            "section_title": section.get("title",""),
            "jurisdiction": "India - Central",
            "text": section['text'],
            "text_cleaned": c,
            "chunk_index": i,
            "chunk_tokens": len(c.split()),
            "source_url": source_url,
            "source_date": "2024-07-01",
            "ingested_at": datetime.utcnow().isoformat()+"Z",
            "version":"v1.0",
            "offense_type": attrs.get("offense_type",""),
            "bailable": attrs["bailable"],
            "cognizable": attrs["cognizable"],
            "max_penalty_years": attrs["max_penalty_years"],
            "penalty_type": attrs["penalty_type"],
            "severity_label_candidate": "UNKNOWN",
            "notes": ""
        }
        emb = embedder.encode(c).tolist()
        docs.append((meta["id"], c, emb, meta))
    # insert into Chroma in batch
    ids, texts, embs, metas = zip(*docs)
    collection.add(documents=list(texts), metadatas=list(metas), ids=list(ids), embeddings=list(embs))

# Example usage:
# html = fetch_html("https://www.indiacode.nic.in/handle/123456/act-ipc")
# sections = extract_sections_from_html(html, "https://www.indiacode.nic.in/...")
# for sec in sections:
#     ingest_section(sec, "https://www.indiacode.nic.in/...", "ipc")
# client.persist()

```

Notes:

- The scraping selector logic must be adapted to the actual HTML structure or replaced with official API ingestion if available.
- The penalty extraction is heuristic and will need manual review and correction for edge cases.

---

# 10) Prompt templates

## A) Retrieval-first RAG prompt (for LLM)

Include retrieval snippets and force the model to indicate exact section citations and include the severity label candidate from metadata.

```
You are a legal information assistant. Use ONLY the retrieved law snippets below to answer. If the law snippets do not provide a clear answer, say "Insufficient information — consult a lawyer."

Context:
Query: {user_query}

Retrieved snippets:
1) [Act: {act}, Section: {section}] {snippet_1}
2) [Act: {act}, Section: {section}] {snippet_2}
...

Rules:
- Use only the snippets above. Quote verbatim any law text used as evidence.
- Do NOT add any new facts beyond the snippets.
- Provide a concise answer (3-6 sentences) that states whether the law likely applies, with explicit caveats.
- After the answer, include:
  - Sources: list the [Act, Section] you used.
  - Severity label candidate: {derived from metadata, e.g., RED/YELLOW/GREEN}
  - Confidence: High/Medium/Low (derive from snippet coverage; if snippets directly mention the issue, mark High).
- Always append the disclaimer: "This is legal information only and not legal advice."

```

## B) Severity validation prompt (LLM as validator)

Only used to summarize rationale and catch edge-cases. LLM is NOT authoritative—its output must be checked against rule-based mapping.

```
Given the following statute excerpt and parsed attributes:
- excerpt: {snippet}
- parsed attributes: bailable={bailable}, cognizable={cognizable}, max_penalty_years={max_penalty_years}, penalty_type={penalty_type}

Question: Based on these attributes, which severity label from [RED, YELLOW, GREEN] best fits and why. If attributes are ambiguous, reply "UNKNOWN" and list which fields are ambiguous.

```

---

# 11) Testing & seed queries

Create a `tests/seed_queries.jsonl` of 200 entries: `{query, expected_act, expected_section, expected_severity}`. Use for continuous integration.

Example entries:

```json
{"query":"Is murder bailable in India?","expected_act":"IPC","expected_section":"302","expected_severity":"RED"}
{"query":"Penalty for overspeeding on highway","expected_act":"Motor Vehicles Act","expected_section":"...","expected_severity":"GREEN"}

```

Run retrieval tests nightly or on every model/ingestion change.

---

# 12) Edge cases & manual review workflow

- Multi-offence queries: when user asks about several offenses, return each offense with source and severity. Prefer structured list responses.
- Amendments & retrospective clauses: include `source_date` and show "last amended" where available. If amendment changes penalty, mark `UPDATED` in UI and add an admin review ticket.
- Ambiguous statutory language: mark `UNKNOWN` and route to human review queue.