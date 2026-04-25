#!/bin/bash

# Legal RAG System - Run with Gemini API

echo "=========================================="
echo "Legal RAG System - Gemini Version"
echo "=========================================="

# Set Gemini API key
export GOOGLE_API_KEY="AIzaSyDd-lZhiaMojYL8_QMlt6s0PeAoClJipAA"

# Activate virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source legalrag/bin/activate
fi

# Install Gemini dependencies
echo ""
echo "Installing Gemini dependencies..."
pip install langchain-google-genai google-generativeai -q

# Step 1: Process PDFs
echo ""
echo "=========================================="
echo "Step 1: Processing PDF files..."
echo "=========================================="
python process_pdfs_simple.py
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

# Step 5: Test RAG pipeline with Gemini
echo ""
echo "=========================================="
echo "Step 5: Testing RAG pipeline (Gemini)..."
echo "=========================================="
python src/rag/rag_pipeline_gemini.py

echo ""
echo "=========================================="
echo "Pipeline Complete!"
echo "=========================================="
echo ""
echo "Your Legal RAG system is ready!"
echo "API key set: GOOGLE_API_KEY"
echo ""
