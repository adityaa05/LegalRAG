#!/bin/bash

# Install dependencies in virtual environment

echo "Installing dependencies..."

# Activate virtual environment
source legalrag/bin/activate

# Install dependencies
pip install -r requirements.txt

echo "✓ Dependencies installed"
