#!/bin/bash

# Legal RAG System Setup Script

echo "=========================================="
echo "Legal RAG System - Setup Script"
echo "=========================================="

# Check Python version
echo ""
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv legalrag

# Activate virtual environment
echo "Activating virtual environment..."
source legalrag/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Download NLTK data
echo ""
echo "Downloading NLTK data..."
python3 -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Create directory structure
echo ""
echo "Creating directory structure..."
mkdir -p data/raw
mkdir -p data/processed
mkdir -p data/chunks
mkdir -p data/embeddings
mkdir -p data/chroma_db
mkdir -p logs
mkdir -p tests

# Check for OpenAI API key
echo ""
echo "Checking for OpenAI API key..."
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  WARNING: OPENAI_API_KEY not set"
    echo "Set it with: export OPENAI_API_KEY='your-api-key'"
else
    echo "✓ OPENAI_API_KEY is set"
fi

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Place PDF files in data/raw/"
echo "2. Run: python src/ingestion/pdf_processor.py"
echo "3. Run: python src/rag/chunker.py"
echo "4. Run: python src/rag/embedder.py"
echo "5. Run: python src/rag/vector_store.py"
echo "6. Run: python src/api/main.py"
echo ""
echo "Or use the quick start script:"
echo "  ./run_pipeline.sh"
echo ""
