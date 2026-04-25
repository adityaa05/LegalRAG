#!/bin/bash

echo "=========================================="
echo "Starting Legal Retrieval API"
echo "=========================================="
echo ""
echo "This API works WITHOUT Gemini (no quota issues!)"
echo "Returns relevant legal sections with severity classification"
echo ""

cd src/api
python retrieval_api.py
