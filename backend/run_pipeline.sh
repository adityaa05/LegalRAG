#!/bin/bash

# Legal RAG System - Complete Pipeline Runner

echo "=========================================="
echo "Legal RAG System - Pipeline Runner"
echo "=========================================="

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source legalrag/bin/activate
fi

# Check for PDFs
echo ""
echo "Checking for PDF files..."
pdf_count=$(ls -1 data/raw/*.pdf 2>/dev/null | wc -l)
if [ $pdf_count -eq 0 ]; then
    echo "⚠️  No PDF files found in data/raw/"
    echo "Please add PDF files before running the pipeline"
    exit 1
fi
echo "Found $pdf_count PDF files"

# Step 1: Process PDFs
echo ""
echo "=========================================="
echo "Step 1: Processing PDF files..."
echo "=========================================="
python src/ingestion/batch_processor.py
if [ $? -ne 0 ]; then
    echo "✗ PDF processing failed"
    exit 1
fi
echo "✓ PDF processing complete"

# Step 2: Chunk text
echo ""
echo "=========================================="
echo "Step 2: Chunking text..."
echo "=========================================="
python src/rag/chunker.py
if [ $? -ne 0 ]; then
    echo "✗ Text chunking failed"
    exit 1
fi
echo "✓ Text chunking complete"

# Step 3: Generate embeddings
echo ""
echo "=========================================="
echo "Step 3: Generating embeddings..."
echo "=========================================="
python src/rag/embedder.py
if [ $? -ne 0 ]; then
    echo "✗ Embedding generation failed"
    exit 1
fi
echo "✓ Embedding generation complete"

# Step 4: Create vector database
echo ""
echo "=========================================="
echo "Step 4: Creating vector database..."
echo "=========================================="
python src/rag/vector_store.py
if [ $? -ne 0 ]; then
    echo "✗ Vector database creation failed"
    exit 1
fi
echo "✓ Vector database created"

# Step 5: Test RAG pipeline
echo ""
echo "=========================================="
echo "Step 5: Testing RAG pipeline..."
echo "=========================================="
python src/rag/rag_pipeline.py
if [ $? -ne 0 ]; then
    echo "⚠️  RAG pipeline test had issues (check if OPENAI_API_KEY is set)"
else
    echo "✓ RAG pipeline test complete"
fi

# Summary
echo ""
echo "=========================================="
echo "Pipeline Complete!"
echo "=========================================="
echo ""
echo "You can now:"
echo "1. Start the API server: python src/api/main.py"
echo "2. Run tests: pytest tests/"
echo "3. Access API docs: http://localhost:8000/docs"
echo ""
