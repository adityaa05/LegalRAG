#!/bin/bash

echo "=========================================="
echo "CLEAN RAG PIPELINE - FINAL FIX"
echo "=========================================="
echo ""
echo "This will:"
echo "  1. Re-process PDFs with CLEAN extraction"
echo "  2. Filter out junk (70% reduction)"
echo "  3. Extract proper metadata"
echo "  4. Re-chunk intelligently"
echo "  5. Re-generate embeddings"
echo "  6. Rebuild vector database"
echo "  7. Test quality"
echo ""
echo "Expected results:"
echo "  • Section Accuracy: 60-70%+"
echo "  • Severity Accuracy: 75%+"
echo "  • Pass Rate: 70%+"
echo "  • Readiness Score: 70-80/100"
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
echo "Step 1/7: Clean PDF extraction..."
echo "=========================================="
python src/ingestion/clean_processor.py
if [ $? -ne 0 ]; then
    echo "✗ PDF processing failed"
    exit 1
fi
echo "✓ Clean extraction complete"

echo ""
echo "Step 2/7: Smart chunking..."
echo "=========================================="
python src/rag/smart_chunker.py
if [ $? -ne 0 ]; then
    echo "✗ Chunking failed"
    exit 1
fi
echo "✓ Chunking complete"

echo ""
echo "Step 3/7: Generating embeddings..."
echo "=========================================="
python src/rag/embed_clean.py
if [ $? -ne 0 ]; then
    echo "✗ Embedding generation failed"
    exit 1
fi
echo "✓ Embeddings generated"

echo ""
echo "Step 4/7: Building clean vector database..."
echo "=========================================="
python src/rag/build_clean_db.py
if [ $? -ne 0 ]; then
    echo "✗ Vector DB build failed"
    exit 1
fi
echo "✓ Vector database built"

echo ""
echo "Step 5/7: Starting API..."
echo "=========================================="
# Start API in background
python src/api/enhanced_api.py &
API_PID=$!
echo "API started (PID: $API_PID)"
sleep 8

echo ""
echo "Step 6/7: Running quality tests..."
echo "=========================================="
python test_rag_quality.py

# Stop API
echo ""
echo "Stopping API..."
kill $API_PID 2>/dev/null

echo ""
echo "Step 7/7: Generating report..."
echo "=========================================="
echo ""
echo "✓ Pipeline complete!"
echo ""
echo "Check rag_quality_report.json for detailed results"
echo ""
