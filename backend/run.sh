#!/bin/bash
# Celestial Atlas Backend - Quick Start Script

echo "🌟 Celestial Atlas API 🌟"
echo "Tower 6 - Stored. Retrievable. Kind."
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "Starting Atlas API server..."
echo "Anchor Date: April 3, 2025"
echo "Access at: http://localhost:8000"
echo "Docs at: http://localhost:8000/docs"
echo ""

python3 main.py
