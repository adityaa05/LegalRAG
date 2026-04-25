#!/bin/bash

echo "=========================================="
echo "IMPROVED RAG PIPELINE"
echo "=========================================="
echo ""
echo "This will:"
echo "  1. Re-process PDFs with better extraction"
echo "  2. Re-chunk with improved strategy"
echo "  3. Re-generate embeddings"
echo "  4. Rebuild vector database"
echo "  5. Re-test quality"
echo ""
echo "This will take 10-15 minutes..."
echo ""
read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    exit 1
fi

# Activate virtual environment
if [ -d "legalrag/bin" ]; then
    source legalrag/bin/activate
fi

echo ""
echo "Step 1/5: Re-processing PDFs with improved extraction..."
echo "=========================================="
python src/ingestion/improved_processor.py
if [ $? -ne 0 ]; then
    echo "✗ PDF processing failed"
    exit 1
fi
echo "✓ PDF processing complete"

echo ""
echo "Step 2/5: Chunking with improved strategy..."
echo "=========================================="
python src/rag/improved_chunker.py
if [ $? -ne 0 ]; then
    echo "✗ Chunking failed"
    exit 1
fi
echo "✓ Chunking complete"

echo ""
echo "Step 3/5: Generating embeddings..."
echo "=========================================="
python src/rag/embedder.py
if [ $? -ne 0 ]; then
    echo "✗ Embedding generation failed"
    exit 1
fi
echo "✓ Embeddings generated"

echo ""
echo "Step 4/5: Rebuilding vector database..."
echo "=========================================="
python src/rag/rebuild_vectordb.py
if [ $? -ne 0 ]; then
    echo "✗ Vector DB rebuild failed"
    exit 1
fi
echo "✓ Vector database rebuilt"

echo ""
echo "Step 5/5: Testing quality..."
echo "=========================================="
# Start API in background
python src/api/enhanced_api.py &
API_PID=$!
sleep 5

# Run tests
python test_rag_quality.py

# Stop API
kill $API_PID

echo ""
echo "=========================================="
echo "PIPELINE COMPLETE!"
echo "=========================================="
echo ""
echo "Check rag_quality_report.json for results"
echo ""
