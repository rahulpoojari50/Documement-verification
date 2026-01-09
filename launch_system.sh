#!/bin/bash

# Aadhaar Detection System - Launch Script
echo "Starting Aadhaar Card Entity Detection System..."

# Check if backend is running
if curl -s http://localhost:8000/health | grep -q "healthy"; then
    echo "✓ Backend API is running"
else
    echo "✗ Backend API is not responding"
    echo "Please start the backend server with: source venv/bin/activate && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
    exit 1
fi

# Check if frontend is running
if curl -s http://localhost:3000 | grep -q "Aadhaar"; then
    echo "✓ Frontend is running"
else
    echo "✗ Frontend is not responding"
    echo "Please start the frontend with: cd frontend && npm start"
    exit 1
fi

# Open in browser
echo "Opening Aadhaar Detection System in your browser..."
open http://localhost:3000

echo "System is ready! You can now use the Aadhaar Card Entity Detection interface."
echo "Backend API documentation: http://localhost:8000/docs"