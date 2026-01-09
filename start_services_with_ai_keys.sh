#!/bin/bash

# Set the API keys as environment variables
export GEMINI_API_KEY="AIzaSyAT42Z-6k21CLgXBySM4kxsoesJ11SCBOk"
export OPENAI_API_KEY="sk-your-openai-api-key-here"

echo "Gemini and OpenAI API keys have been set as environment variables."
echo "To use your own keys, replace the values in this script with your actual API keys."

# Kill any existing backend processes
pkill -f "uvicorn app.main" >/dev/null 2>&1

# Kill any existing frontend processes
pkill -f "npm start" >/dev/null 2>&1

# Wait a moment for the processes to terminate
sleep 2

echo "Starting backend service..."
# Start the backend service with both API keys
cd /Users/rahulpoojari/Documents/mlmodel
source venv/bin/activate
GEMINI_API_KEY="AIzaSyAT42Z-6k21CLgXBySM4kxsoesJ11SCBOk" OPENAI_API_KEY="sk-your-openai-api-key-here" python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
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
echo "Both Gemini and OpenAI API keys are configured for document verification."

# Wait for background processes
wait $BACKEND_PID $FRONTEND_PID