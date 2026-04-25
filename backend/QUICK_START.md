# Legal RAG System - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Prerequisites
- Python 3.9+
- OpenAI API Key
- PDF files of Indian legal documents

---

## Step 1: Setup (2 minutes)

```bash
# Navigate to project
cd legal-rag

# Run setup script
./setup.sh

# Activate virtual environment
source legalrag/bin/activate

# Set OpenAI API key
export OPENAI_API_KEY='your-api-key-here'
```

---

## Step 2: Add Your Data (1 minute)

```bash
# Place your PDF files in data/raw/
cp /path/to/your/legal/pdfs/*.pdf data/raw/
```

**Supported Documents:**
- Indian Penal Code (IPC)
- Code of Criminal Procedure (CrPC)
- Indian Constitution
- Evidence Act
- Companies Act
- Income Tax Act
- Motor Vehicles Act

---

## Step 3: Run Pipeline (5-10 minutes)

```bash
# Run complete pipeline
./run_pipeline.sh
```

This will:
1. ✅ Extract text from PDFs
2. ✅ Chunk text into 500-token pieces
3. ✅ Generate embeddings
4. ✅ Create vector database
5. ✅ Test the system

---

## Step 4: Start API Server (30 seconds)

```bash
# Start FastAPI server
cd src/api
python main.py
```

Server runs at: `http://localhost:8000`

---

## Step 5: Test It! (1 minute)

### Option A: Interactive API Docs
Open browser: `http://localhost:8000/docs`

### Option B: Command Line
```bash
# Health check
curl http://localhost:8000/health

# Ask a question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is the punishment for murder in India?"
  }'
```

### Option C: Python
```python
import requests

response = requests.post(
    "http://localhost:8000/ask",
    json={"question": "What is the punishment for theft?"}
)

print(response.json())
```

---

## 📊 Example Response

```json
{
  "question": "What is the punishment for murder?",
  "answer": "According to IPC Section 302, whoever commits murder shall be punished with death or imprisonment for life, and shall also be liable to fine.",
  "citations": [
    {
      "act": "IPC",
      "section": "302",
      "title": "Punishment for murder",
      "text_snippet": "Whoever commits murder shall be punished with death..."
    }
  ],
  "severity": {
    "level": "RED",
    "reasoning": "Non-bailable offense (high severity)",
    "confidence": 0.95,
    "summary": {
      "color": "#DC2626",
      "label": "High Severity",
      "icon": "🔴",
      "action": "Consult a criminal defense lawyer immediately"
    }
  },
  "disclaimer": "⚠️ This is legal information only and not legal advice..."
}
```

---

## 🎯 Common Use Cases

### 1. Ask Legal Questions
```bash
POST /ask
{
  "question": "Is theft a bailable offense?"
}
```

### 2. Search Documents
```bash
GET /search?query=theft&k=5
```

### 3. Get System Stats
```bash
GET /stats
```

### 4. List Available Acts
```bash
GET /acts
```

---

## 🔧 Troubleshooting

### "OPENAI_API_KEY not found"
```bash
export OPENAI_API_KEY='sk-...'
```

### "No PDF files found"
```bash
# Add PDFs to data/raw/
ls data/raw/  # Should show .pdf files
```

### "Collection not found"
```bash
# Run vector store creation
python src/rag/vector_store.py
```

### "Module not found"
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📈 Performance Tips

1. **First Run**: Takes 5-10 minutes to process documents
2. **Subsequent Runs**: Instant (uses cached embeddings)
3. **API Response Time**: 2-5 seconds per query
4. **Batch Processing**: Process multiple PDFs at once

---

## 🧪 Run Tests

```bash
# Run all tests
pytest tests/ -v

# Generate test report
python tests/test_seed_queries.py --report
```

---

## 📚 Next Steps

1. ✅ **System Running** - API is live
2. 🔄 **Connect Frontend** - Use API endpoints
3. 🔄 **Add More Documents** - Expand corpus
4. 🔄 **Customize Rules** - Adjust severity classification
5. 🔄 **Deploy** - Move to production

---

## 🆘 Need Help?

1. Check `README.md` for detailed docs
2. Review `BACKEND_STATUS.md` for implementation details
3. Check logs for error messages
4. Verify all dependencies installed

---

## 🎉 You're Ready!

Your Legal RAG system is now running. Start asking legal questions!

**API Docs**: http://localhost:8000/docs  
**Health Check**: http://localhost:8000/health  
**Query Endpoint**: POST http://localhost:8000/ask

---

**Built with ❤️ for legal accessibility**
