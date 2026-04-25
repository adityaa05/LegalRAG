#!/bin/bash

echo "=========================================="
echo "Legal RAG - Fixed Pipeline"
echo "=========================================="

# Install Gemini dependencies
echo "Installing Gemini dependencies..."
pip install langchain-google-genai google-generativeai -q

# Set API key
export GOOGLE_API_KEY="AIzaSyDd-lZhiaMojYL8_QMlt6s0PeAoClJipAA"

echo ""
echo "Step 1: Chunking text..."
python src/rag/chunker.py

echo ""
echo "Step 2: Generating embeddings..."
python src/rag/embedder.py

echo ""
echo "Step 3: Creating vector database..."
python src/rag/vector_store.py

echo ""
echo "Step 4: Testing with Gemini..."
python src/rag/rag_pipeline_gemini.py

echo ""
echo "=========================================="
echo "Pipeline Complete!"
echo "=========================================="
