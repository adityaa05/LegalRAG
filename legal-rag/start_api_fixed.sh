#!/bin/bash

# Get the absolute path of the legal-rag directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "=========================================="
echo "Starting Legal Retrieval API"
echo "=========================================="

# Activate virtual environment
if [ -d "legalrag" ]; then
    echo "Activating virtual environment..."
    source legalrag/bin/activate
else
    echo "ERROR: Virtual environment 'legalrag' not found!"
    exit 1
fi

# Set python path to include src
export PYTHONPATH=$PYTHONPATH:$SCRIPT_DIR/src

echo "Starting API on port 8001..."
cd src/api
python retrieval_api.py
