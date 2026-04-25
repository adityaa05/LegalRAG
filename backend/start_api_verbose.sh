#!/bin/bash

echo "=========================================="
echo "Starting Legal Retrieval API"
echo "=========================================="
echo ""

# Check if ChromaDB exists
if [ ! -d "data/chroma_db" ]; then
    echo "❌ ChromaDB not found at data/chroma_db"
    echo "Run: python src/rag/vector_store.py first"
    exit 1
fi

echo "✓ ChromaDB found"
echo ""
echo "Starting server on http://localhost:8001"
echo "Press Ctrl+C to stop"
echo ""
echo "Once started, test with:"
echo "  curl http://localhost:8001/health"
echo ""
echo "=========================================="
echo ""

# Activate virtual environment
if [ -d "legalrag/bin" ]; then
    echo "Activating virtual environment..."
    source legalrag/bin/activate
fi

cd src/api
python retrieval_api.py
