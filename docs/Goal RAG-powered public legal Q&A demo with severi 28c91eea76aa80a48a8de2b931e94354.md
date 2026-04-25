# Goal: RAG-powered public legal Q&A demo with severity indicator

1. Data Layer

| Task | Owner | Complexity | Dependencies | Tags |
| --- | --- | --- | --- | --- |
| Identify & scrape IPC, CrPC, MVA text from indiacode.nic.in | Mira | M | None | [CORE] |
| Clean and chunk text (500–800 tokens) | Ilya | M | Data scrape | [CORE] |
| Add metadata: `{section, act, offense_type, bailable, cognizable}` | Ilya | M | Cleaning | [CORE] |
| Generate embeddings (MiniLM-L6-v2) | Mira | S | Metadata | [CORE] |
| Store embeddings in Chroma vector DB | Ilya | S | Embeddings | [CORE] |
1. Backend/RAG Pipeline

| Task | Owner | Complexity | Dependencies | Tags |
| --- | --- | --- | --- | --- |
| Create LangChain pipeline (retriever + LLM chain) | Mira | M | Vector DB | [CORE] |
| Implement severity logic (Red/Yellow/Green rule-based map) | Ilya | M | Metadata | [CORE] |
| Add context + disclaimer to prompt template | Sam | S | RAG chain | [CORE] |
| Add citation injection (show section text + act name) | Mira | S | RAG chain | [CORE] |
1. Frontend (Steamlit)

| Task | Owner | Complexity | Dependencies | Tags |
| --- | --- | --- | --- | --- |
| Build query input + response display panel | Ilya | S | Backend API | [CORE] |
| Add color-coded severity UI badge (R/Y/G) | Ilya | S | Backend | [CORE] |
| Include citation + source text display | Mira | S | Backend | [CORE] |
| Add disclaimer banner + footer | Sam | S | UI setup | [CORE] |
| Add “Download Chat History” (txt/json) button | Ilya | M | UI | [CORE] |
1. Deployment

| Task | Owner | Complexity | Dependencies | Tags |
| --- | --- | --- | --- | --- |
| Containerize app with Docker | Ilya | M | Backend + Frontend | [CORE] |
| Deploy to Google Cloud Run | Mira | M | Docker | [CORE] |
| Configure simple logs + usage counter | Ilya | M | Cloud | [CORE] |
1. Quality & Safety

| Task | Owner | Complexity | Dependencies | Tags |
| --- | --- | --- | --- | --- |
| Add legal disclaimers to all outputs | Sam | S | Frontend | [RISK] |
| Test for hallucinations (cross-check vs source text) | Mira | M | Backend | [RISK] |
| Validate color-coding accuracy | Ilya | M | Metadata | [RISK] |