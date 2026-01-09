#!/bin/bash

# Set the Gemini API key as an environment variable
export GEMINI_API_KEY="AIzaSyAT42Z-6k21CLgXBySM4kxsoesJ11SCBOk"

echo "Gemini API key has been set as an environment variable."

# Kill any existing backend processes
pkill -f "uvicorn app.main" >/dev/null 2>&1

# Kill any existing frontend processes
pkill -f "npm start" >/dev/null 2>&1

# Wait a moment for the processes to terminate
sleep 2

echo "Starting backend service..."
# Start the backend service with the Gemini API key
cd /Users/rahulpoojari/Documents/mlmodel
source venv/bin/activate
GEMINI_API_KEY="AIzaSyAT42Z-6k21CLgXBySM4kxsoesJ11SCBOk" python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

sleep 5

echo "Starting frontend service..."
# Start the frontend service
cd /Users/rahulpoojari/Documents/mlmodel/frontend
npm start &
FRONTEND_PID=$!

echo "Services started successfully!"
echo "Backend is running on http://localhost:8000 (PID: $BACKEND_PID)"
echo "Frontend is running on http://localhost:3000 (PID: $FRONTEND_PID)"
echo "Gemini API key is configured for document verification."

# Wait for background processes
wait $BACKEND_PID $FRONTEND_PID