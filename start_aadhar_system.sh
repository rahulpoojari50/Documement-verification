#!/bin/bash

# Aadhaar Card Entity Detection - Startup Script
# =============================================

echo "Aadhaar Card Entity Detection System"
echo "==================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if model exists
if [ ! -f "runs/detect/aadhar_detector/weights/best.pt" ]; then
    echo "Trained model not found. Starting training..."
    python train_aadhar_focused.py
else
    echo "Using existing trained model."
fi

# Start the API server
echo "Starting API server..."
echo "Access the API at: http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000