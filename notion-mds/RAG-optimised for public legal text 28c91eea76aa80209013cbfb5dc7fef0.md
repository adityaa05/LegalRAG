# RAG-optimised for public legal text

## Architecture Overview

1. **Document Ingestion Layer**
    - Sources: official open data portals (e.g., gov legislation APIs or bulk law text dumps).
    - Preprocessing: text chunking (500–1000 tokens), metadata tagging (jurisdiction, date, section).
    - Output → vector embeddings.
2. **Vector Database**
    - **Chroma** or **FAISS** for semantic retrieval.
    - Schema: `{id, title, section, jurisdiction, date, embedding}`
    - Indexed by cosine similarity.
3. **Retrieval-Augmented Generation (RAG) Pipeline**
    - Query → embedding → top-k retrieval → context-injected prompt to LLM.
    - **Model options**:
        - Local: `mistral-7b-instruct`, `llama-3-8b` (via Hugging Face).
        - API-based: `gpt-4-turbo` or `claude-3-sonnet` for higher reliability.
    - Prompt structure enforces grounding + disclaimer.
4. **API Layer**
    - **FastAPI** for query endpoints (`/ask`, `/upload`, `/status`).
    - Optional: rate limiting, API keys, and logging middleware.
5. **Frontend**
    - Streamlit (MVP demo) or React (scalable version).
    - Shows: retrieved law snippets, model’s summarized interpretation, and disclaimer.
6. **Deployment**
    - Dockerized container → deploy to **Google Cloud Run** or **AWS Fargate**.
    - CI/CD with GitHub Actions.

| Layer | Tool | Purpose |
| --- | --- | --- |
| **Data Source** | Open legal text (e.g., US Code / gov legislation APIs) | Raw corpus |
| **Embeddings** | `sentence-transformers/all-MiniLM-L6-v2` | Fast, lightweight |
| **Vector DB** | **Chroma** | Easiest for local prototyping |
| **LLM** | `gpt-4-turbo` (API) or `mistral-7b-instruct` (local) | Context-grounded response |
| **RAG Orchestration** | **LangChain** | Retrieval + generation flow |
| **Backend API** | **FastAPI** | `/ask` endpoint |
| **Frontend** | **Streamlit** | Simple UI for queries |
| **Deployment** | **Docker + Cloud Run** | Free/cheap and fast |
| **Disclaimer Layer** | Static text appended to every response | Legal safety |

---

## MVP Feature Scope

1. **Preloaded Corpus Q&A** (no uploads)
    - Uses open government law text (e.g., Indian Penal Code or U.S. Federal Code).
2. **Contextual Legal Answers**
    - Retrieval-augmented generation with source citations.
3. **Color-Coded Severity System**
    - **Red:** non-bailable / serious offense
    - **Yellow:** bailable / moderate severity
    - **Green:** minor or civil violation
    - Backed by rule-based mapping table + LLM validation.
4. **Chat History Download**
    - Export to `.txt` or `.json`.
5. **Mandatory Disclaimer Layer**
    - “This system provides legal information, not legal advice.”

---

The main public data sources include:

- **Indian Penal Code (IPC)**
- **Code of Criminal Procedure (CrPC)**
- **Motor Vehicles Act**
- **Narcotic Drugs and Psychotropic Substances Act (NDPS)**
- **Public portals:** indiacode.nic.in (official government law database)

---

[Goal: RAG-powered public legal Q&A demo with severity indicator](Goal%20RAG-powered%20public%20legal%20Q&A%20demo%20with%20severi%2028c91eea76aa80a48a8de2b931e94354.md)

---

## Risk summary (top risks)

1. **Hallucinated or incorrect legal advice** — Model fabricates statements that contradict source text.
2. **Misclassification of severity (R/Y/G)** — Rule gaps or ambiguous statutes produce wrong color.
3. **Incomplete / stale legal corpus** — Missing recent amendments or sections.
4. **Source-matching failures** — Retrieved snippets not actually supporting the model’s claim.
5. **Regulatory / liability exposure** — Users interpret outputs as legal advice and take action.
6. **Security / privacy leak** — Sensitive user queries or logs expose PII.
7. **Scalability / cost overruns** — API costs or compute blowout during demos.
8. **UX trust gaps** — Users distrust outputs due to lack of clear citations or confusing language.
9. **Indexed bias or jurisdiction mismatch** — Wrong jurisdiction (state vs central law) leads to wrong answer.
10. **Data ingestion errors** — Parsing/scraping mistakes create corrupted sections.

---

- Risk table — likelihood, impact, detection, mitigation, owner, escalation trigger
    
    
    | Risk | Likelihood | Impact | Detection (how we know) | Mitigation (what to do) | Owner | Escalation trigger |
    | --- | --- | --- | --- | --- | --- | --- |
    | Hallucinated / incorrect legal statements | Medium-high | High | Randomized QA tests fail; mismatch between model claim and source text during tests. | Enforce retrieval-first prompt templates. Require exact quoted source snippet for any legal claim. Add automated validator that checks model outputs vs retrieved snippets. Use conservative LLM model settings (low temperature). | Mira | >5% failure rate in production QA or user reports of direct contradiction. [ESCALATED] |
    | Misclassification of R/Y/G severity | Medium | High (user actions affected) | Compare rule-based label vs human-labeled sample. User feedback flags conflicting labels. | Build rule-based primary mapping (bailable: yes/no, cognizable, max penalty bands). Use LLM only to validate, not decide. Maintain an exceptions table. | Ilya | >3 incorrect labels in 100 queries or repeated user complaints. [ESCALATED] |
    | Incomplete / stale corpus | Medium | High | Scheduled checks show missing acts or amendments; user reports. | Use authoritative government sources. Schedule weekly/monthly corpus refresh. Timestamp sources and display citation dates. | Mira | Any law amended since corpus date that affects answers in demo scope. [ESCALATED] |
    | Source-matching failures (claims unsupported) | Medium-high | High | Automated matcher finds <threshold (e.g., 80%) token overlap between model claims and retrieved snippet. | Force model to return a "support evidence" field containing verbatim quote(s). Reject answers that lack direct quote. | Mira | >5% unsupported claims in QA tests. [ESCALATED] |
    | Regulatory / liability exposure | Low-medium | Very high | Legal counsel flags marketing text; user threatens action. | Prominent disclaimers. Clear TOS: "information only". Add safety copy before each answer: "Not legal advice, consult a lawyer." Rate-limit features that infer applicability to personal situations. | Sam | Any legal demand or cease-and-desist letter, or counsel recommendation. [ESCALATED] |
    | Security / privacy leak | Low-medium | High | Audit logs show PII stored in logs or vector DB. | Avoid storing raw user queries by default. Anonymize logs. Secure vector DB access with credentials and network rules. Encrypt at rest and in transit. | Ilya | Any PII found in logs or DB or failed penetration test. [ESCALATED] |
    | Cost / scalability overruns | Medium | Medium | Monitoring shows API spend > planned budget. | Use small LLM footprints for demo. Batch embedding ops. Set hard budget caps and autoscaling limits. Use local models if costs spike. | Ilya | Spend >150% of forecasted monthly demo budget. |
    | UX trust gaps | Medium | Medium | Low user satisfaction; click-through to "more info" low; feedback indicates confusion. | Show clear citations, verbatim snippets, severity rationale, and "confidence" indicator. Offer "See original law" link. | Sam | Drop in demo conversion or trust metrics below threshold. |
    | Jurisdiction mismatch | Low-medium | High | Users report wrong state-specific law returned. | Include jurisdiction filter metadata and expose selection in UI. Validate retrieval by jurisdiction during ingestion. | Mira | Any user report showing answer applies to wrong jurisdiction. |
    | Data ingestion / parsing errors | Medium | Medium | Random QA shows broken sections. | Add validation during ingestion: checksum, minimal token length, human spot-check of high-priority acts. | Ilya | >2% of sections flagged as corrupt in validation. |

---

## Detection & monitoring plan

- **Automated test suite** (owner: Mira)
    - Unit tests: retrieval returns expected sections for seed queries.
    - Integration tests: full RAG end-to-end for a test-set of 200 seeded legal questions with gold-standard answers. Failure threshold: 95% pass for retrieval; 90% for supported claims.
- **Labeling audits** (owner: Ilya)
    - Monthly human review of 200 random queries to validate R/Y/G and citation accuracy.
- **Logging & metrics** (owner: Ilya)
    - Track: API latency; % of answers with verbatim citation; number of user complaints; cost per 1k queries.
- **Alerts**
    - Alert on: hallucination rate > 5%; cost > 150% forecast; PII leak detections. Alerts delivered via email/Slack.

---

## Mitigation specifics (implementation-level)

1. **Make retrieval the source of truth**
    - Prompt template: include top-k retrieved verbatim snippets and instruct model to only use them. If answer cannot be supported, respond "Insufficient information — consult a lawyer."
2. **Rule-based severity engine**
    - Construct mapping table extracted from corpus: for each offense section include `max_penalty_years`, `bailable` (Y/N), `cognizable` (Y/N), `summary_category`. Map to R/G/Y via threshold rules. Only use LLM to nominate an exception; exceptions require human review for now.
3. **Citation-first UI**
    - Frontend must show the exact section(s) quoted, act name, and link to original law on indiacode. Display citation date.
4. **Operational safety**
    - No user upload in MVP. No PII storage. Logs store hashed session ids only.
5. **Human-in-the-loop for edge cases**
    - Errors in classification or unsupported claims create ticket flagged [ESCALATED] for manual review and corpus update.
6. **Conservative generation settings**
    - Use temperature 0–0.2, max tokens limited, and few-shot examples that show refusal behavior for out-of-scope or uncertain cases.

---

## Residual risk & acceptance criteria

- Residual risk remains for complex, multi-fact scenarios where statutes interact. Acceptance criteria for MVP launch:
    - <5% unsupported claims in QA set.
    - <3% mis-labeled severity in human audit sample.
    - Disclaimers present on all responses.
    - No PII found in system logs or DB.

---

## Escalation policy & [ESCALATED] flags

- Any of these conditions should be immediately escalated and freeze public demo until triage:
    - Hallucination rate >5% on tests.
    - Any verified user report of advice leading to material harm.
    - PII found in vector DB or logs.
    - Legal counsel issues a takedown or formal cease request.

Mark tasks as [ESCALATED] in `build_plan.md` where applicable:

- "Enforce retrieval-first prompt templates" — add [ESCALATED] if validation tests fail.
- "Implement severity logic" — add [ESCALATED] if mislabel >3%.
- "Add legal disclaimers" — always [CORE] and prioritized.

---

## Recovery & contingency plans

- If corpus found stale: pull emergency update from indiacode, mark affected sections in UI as "updated on [date]" and show "possible change" badge.
- If hallucinations spike: switch LLM model or reduce generation to template-only replies that quote law only.
- If PII leak: shut down public endpoint, rotate DB credentials, purge logs, notify affected parties if required.

---

## Mapping risks back to `build_plan.md` tasks (short)

- Enforcement of citations → LangChain prompt task (Mira).
- Severity engine correctness → Implement severity logic + human audit (Ilya).
- Corpus freshness → Identify & scrape + scheduled refresh (Mira).
- Logging & privacy → Configure logs/anonymization (Ilya).
- Disclaimers → UI disclaimer task (Sam).

---

[Data Schema & Ingestion Plan](Data%20Schema%20&%20Ingestion%20Plan%2028c91eea76aa8077a5fdf4fa7b9b12d6.md)

---