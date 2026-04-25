# Legal RAG System - Environment Setup

## Required Python Libraries

```bash
# Core libraries
pip install python-dotenv requests beautifulsoup4 lxml

# Text processing and NLP
pip install nltk spacy pandas numpy

# PDF processing 
pip install PyMuPDF  # or pymupdf
pip install pdfplumber  # alternative: fitz, pypdf2

# Embeddings and Vector DB
pip install sentence-transformers
pip install chromadb

# RAG Framework
pip install langchain
pip install langchain-community
pip install langchain-openai  # if using OpenAI
pip install langchain-chroma

# Web framework for UI
pip install streamlit

# Additional utilities
pip install python-json-logger tqdm
```

## Alternative Options at Each Layer

### PDF Processing:
- **PyMuPDF (fitz)**: Fast, good for structured PDFs ✅ **Recommended**
- **pdfplumber**: Better for tables and complex layouts
- **pypdf2**: Basic, sometimes struggles with complex PDFs

### Embeddings:
- **sentence-transformers/all-MiniLM-L6-v2**: Fast, lightweight ✅ **For Learning**
- **sentence-transformers/all-mpnet-base-v2**: Better quality, slower
- **OpenAI text-embedding-ada-002**: Best quality, costs money

### Vector Database:
- **ChromaDB**: Easiest for local development ✅ **For Learning**
- **FAISS**: Facebook's library, good performance
- **Pinecone**: Cloud-hosted, production-ready

### LLM Options:
- **OpenAI GPT-4**: Best quality, requires API key
- **Local models**: Ollama + Llama/Mistral (free, private)
- **Hugging Face**: Many free options

## Project Structure
```
legal-rag/
├── data/
│   ├── raw/          # Original PDF files
│   ├── processed/    # Cleaned text files
│   └── chunks/       # Chunked data
├── embeddings/       # Vector database files
├── src/
│   ├── ingestion/    # PDF processing scripts
│   ├── rag/          # RAG pipeline
│   └── frontend/     # Streamlit app
├── notebooks/        # Jupyter notebooks for experimentation
├── requirements.txt
└── README.md
```