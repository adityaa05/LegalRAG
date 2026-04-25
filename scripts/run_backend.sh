#!/bin/bash

# Get the absolute path of the project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( dirname "$SCRIPT_DIR" )"
cd "$PROJECT_ROOT/backend"

echo "=========================================="
echo "Starting Legal Retrieval API (Backend)"
echo "=========================================="

# Activate virtual environment
if [ -d "legalrag" ]; then
    echo "Activating virtual environment..."
    source legalrag/bin/activate
else
    echo "ERROR: Virtual environment 'legalrag' not found in $(pwd)!"
    exit 1
fi

# Set python path to include src
export PYTHONPATH=$PYTHONPATH:$(pwd)/src

echo "Starting API on port 8001..."
cd src/api
python retrieval_api.py
