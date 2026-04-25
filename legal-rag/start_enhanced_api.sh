#!/bin/bash

echo "=========================================="
echo "Enhanced Legal Analysis API"
echo "=========================================="
echo ""
echo "This API analyzes legal situations and provides:"
echo "  • Relevant laws with severity"
echo "  • Key factors to consider"
echo "  • Specific recommendations"
echo "  • Overall risk assessment"
echo ""
echo "Starting server on http://localhost:8002"
echo "=========================================="
echo ""

# Activate virtual environment
if [ -d "legalrag/bin" ]; then
    source legalrag/bin/activate
fi

cd src/api
python enhanced_api.py
