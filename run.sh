#!/bin/bash

# IBM MDM Match Decision Explorer - Launch Script

echo "🔍 Starting IBM MDM Match Decision Explorer..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "⚠️  Virtual environment not found. Creating one..."
    python -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
    echo "✓ Dependencies installed"
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Please create one based on .env.example"
    echo "   Copy .env.example to .env and configure your MDM credentials"
    exit 1
fi

# Launch Streamlit app
echo ""
echo "🚀 Launching application..."
echo "   The app will open in your browser at http://localhost:8501"
echo ""
streamlit run src/app.py

# Made with Bob
