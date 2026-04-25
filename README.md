# LegalRAG: AI-Powered Indian Legal Assistant

A full-stack RAG (Retrieval-Augmented Generation) system for searching and analyzing Indian legal documents.

## 📂 Project Structure

- **`backend/`**: FastAPI server, ChromaDB vector store, and RAG pipeline.
- **`frontend/`**: Next.js application with a modern, glassmorphic UI.
- **`data/`**: 
    - `raw/`: Original legal PDFs.
    - `manual_sections/`: High-quality, curated legal sections.
- **`docs/`**: Project documentation, analysis reports, and implementation details.
- **`scripts/`**: Automation scripts for setup and deployment.

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.9+
- Node.js 18+

### 2. Setup & Run
Use the consolidated start script to launch both servers:

```bash
./scripts/start_all.sh
```

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8001

## 🏛️ Key Features

- **Semantic Search**: Find relevant laws using natural language, not just keywords.
- **Severity Classification**: Automatically identifies the severity of legal offenses (Red/Yellow/Green).
- **Curated Data**: High-quality manual curation of critical Indian Penal Code (IPC) sections.
- **Modern UI**: Interactive, responsive interface built with TailwindCSS and Motion.

## 🛠️ Tech Stack

- **Backend**: FastAPI, ChromaDB, Sentence-Transformers (all-MiniLM-L6-v2).
- **Frontend**: Next.js 15, React 19, TailwindCSS, Motion, Styled-components.
- **Data**: Python-based ingestion pipeline with PDF parsing and metadata extraction.
```
