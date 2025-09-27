#!/bin/bash

echo "Starting Deepfake Detection System..."
echo

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the server with TruFor model
echo "Starting server with TruFor model..."
python start_trufor.py


