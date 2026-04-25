# Legal RAG System - Indian Law Q&A

A Retrieval-Augmented Generation (RAG) system for answering questions about Indian law with severity classification and citation support.

## 🎯 Features

- **Semantic Search**: Vector-based search over Indian legal documents (IPC, CrPC, Constitution, etc.)
- **RAG Pipeline**: Context-grounded answers using LangChain + GPT-4
- **Severity Classification**: Rule-based Red/Yellow/Green severity mapper
- **Citation System**: Verbatim quotes with Act and Section references
- **REST API**: FastAPI backend with comprehensive endpoints
- **Legal Disclaimers**: Mandatory safety warnings on all outputs

## 📋 System Architecture

```
┌─────────────────┐
│  PDF Documents  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ PDF Processor   │ ← Extract & clean text
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Text Chunker    │ ← Split into 500-token chunks
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Embedder        │ ← Generate embeddings (MiniLM-L6-v2)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ ChromaDB        │ ← Vector database
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ RAG Pipeline    │ ← LangChain + GPT-4
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ FastAPI Backend │ ← REST API
└─────────────────┘
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Create virtual environment
python3 -m venv legalrag
source legalrag/bin/activate  # On Windows: legalrag\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set OpenAI API key
export OPENAI_API_KEY='your-api-key-here'
```

### 2. Process Legal Documents

```bash
# Step 1: Extract text from PDFs
python src/ingestion/pdf_processor.py

# Step 2: Chunk text into manageable pieces
python src/rag/chunker.py

# Step 3: Generate embeddings
python src/rag/embedder.py

# Step 4: Create vector database
python src/rag/vector_store.py
```

### 3. Start API Server

```bash
cd src/api
python main.py
```

The API will be available at `http://localhost:8000`

### 4. Test the System

```bash
# Interactive docs
open http://localhost:8000/docs

# Health check
curl http://localhost:8000/health

# Ask a question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the punishment for murder in India?"}'
```

## 📁 Project Structure

```
legal-rag/
├── src/
│   ├── ingestion/
│   │   ├── pdf_processor.py      # PDF text extraction
│   │   └── batch_processor.py    # Batch processing
│   ├── rag/
│   │   ├── chunker.py            # Text chunking
│   │   ├── embedder.py           # Embedding generation
│   │   ├── vector_store.py       # ChromaDB integration
│   │   ├── severity_classifier.py # Severity classification
│   │   └── rag_pipeline.py       # RAG pipeline
│   └── api/
│       └── main.py               # FastAPI backend
├── data/
│   ├── raw/                      # Raw PDF files
│   ├── processed/                # Processed sections
│   ├── chunks/                   # Text chunks
│   ├── embeddings/               # Embedded chunks
│   └── chroma_db/                # Vector database
├── requirements.txt
└── README.md
```

## 🔧 Configuration

### Severity Classification Rules

Edit `severity_classifier.py` to customize severity rules:

- **RED**: Non-bailable, death penalty, life imprisonment, 10+ years
- **YELLOW**: Bailable, 3-10 years imprisonment
- **GREEN**: <3 years, fine only, minor offenses

### RAG Pipeline Settings

In `rag_pipeline.py`:
- `model_name`: LLM model (default: `gpt-4-turbo`)
- `embedding_model`: Embedding model (default: `all-MiniLM-L6-v2`)
- `k`: Number of chunks to retrieve (default: 5)
- `temperature`: LLM temperature (default: 0.1 for factual responses)

## 📊 Data Pipeline

### 1. PDF Processing
- Extracts text from legal PDFs
- Cleans and normalizes text
- Identifies sections and subsections
- Extracts legal metadata (bailable, cognizable, penalties)

### 2. Text Chunking
- Splits sections into 500-token chunks
- 50-token overlap between chunks
- Preserves section boundaries
- Maintains metadata

### 3. Embedding Generation
- Uses `sentence-transformers/all-MiniLM-L6-v2`
- 384-dimensional embeddings
- Normalized for cosine similarity
- Batch processing for efficiency

### 4. Vector Storage
- ChromaDB with persistent storage
- Cosine similarity search
- Metadata filtering support
- ~100MB for 10K chunks

## 🔍 API Endpoints

### `POST /ask`
Ask a legal question

**Request:**
```json
{
  "question": "What is the punishment for theft?",
  "num_sources": 5,
  "include_metadata": true
}
```

**Response:**
```json
{
  "question": "What is the punishment for theft?",
  "answer": "According to IPC Section 379...",
  "citations": [
    {
      "act": "IPC",
      "section": "379",
      "title": "Punishment for theft",
      "text_snippet": "Whoever commits theft..."
    }
  ],
  "severity": {
    "level": "YELLOW",
    "reasoning": "Moderate penalty: 3 years",
    "confidence": 0.85,
    "summary": {
      "color": "#F59E0B",
      "label": "Moderate Severity",
      "icon": "🟡",
      "action": "Legal consultation recommended"
    }
  },
  "num_sources": 5,
  "disclaimer": "⚠️ This is legal information only...",
  "timestamp": "2025-10-27T15:30:00"
}
```

### `GET /search?query=theft&k=5`
Search for relevant documents

### `GET /health`
Health check

### `GET /stats`
System statistics

### `GET /acts`
List available legal acts

## 🧪 Testing

### Unit Tests
```bash
pytest tests/
```

### Test Severity Classifier
```bash
python src/rag/severity_classifier.py
```

### Test RAG Pipeline
```bash
python src/rag/rag_pipeline.py
```

## 📝 Supported Legal Acts

- Indian Penal Code (IPC)
- Code of Criminal Procedure (CrPC)
- Code of Civil Procedure (CPC)
- Indian Constitution
- Indian Evidence Act
- Companies Act 2013
- Income Tax Act 1961
- Motor Vehicles Act

## ⚠️ Legal Disclaimer

**IMPORTANT**: This system provides legal information, NOT legal advice.

- Outputs are for informational purposes only
- Do not rely on this system for legal decisions
- Always consult a qualified lawyer for your specific situation
- The system may contain errors or outdated information
- No attorney-client relationship is created

## 🔐 Security & Privacy

- No user queries stored by default
- Anonymized logging
- API rate limiting (recommended for production)
- No PII collection
- Secure vector DB access

## 🚧 Known Limitations

1. **Hallucination Risk**: LLM may generate unsupported claims
2. **Corpus Staleness**: Laws may be amended after ingestion
3. **Jurisdiction Scope**: Limited to Indian central laws
4. **Context Window**: Limited to top-5 retrieved chunks
5. **Ambiguous Queries**: May not handle multi-offense questions well

## 📈 Performance

- **Retrieval Speed**: ~100ms for top-5 chunks
- **LLM Response**: ~2-5 seconds (GPT-4)
- **Embedding Generation**: ~1000 chunks/minute
- **Database Size**: ~100MB for 10K chunks

## 🛠️ Development

### Add New Legal Documents

1. Place PDF in `data/raw/`
2. Run `pdf_processor.py`
3. Run `chunker.py`
4. Run `embedder.py`
5. Run `vector_store.py` with `reset=True`

### Customize Prompt Template

Edit `_create_prompt_template()` in `rag_pipeline.py`

### Add Metadata Filters

Use `filter_metadata` parameter in queries:
```python
pipeline.retrieve_relevant_chunks(
    query="theft",
    filter_metadata={"document_type": "ipc"}
)
```

## 📚 References

- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [India Code](https://www.indiacode.nic.in/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 👥 Authors

Legal RAG System Development Team

## 🐛 Issues & Support

For issues, questions, or feature requests, please open an issue on GitHub.

---

**Built with ❤️ for legal accessibility**
