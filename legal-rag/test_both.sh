#!/bin/bash

export GOOGLE_API_KEY="AIzaSyDd-lZhiaMojYL8_QMlt6s0PeAoClJipAA"

echo "=========================================="
echo "Testing Simple RAG (Direct Gemini API)"
echo "=========================================="
python src/rag/simple_rag_gemini.py

echo ""
echo ""
echo "=========================================="
echo "Testing LangChain RAG (if simple works)"
echo "=========================================="
python src/rag/rag_pipeline_gemini.py
