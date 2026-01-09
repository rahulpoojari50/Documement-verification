#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | xargs)
    echo "Environment variables loaded from .env file"
else
    echo "Warning: .env file not found"
fi

# Kill any existing backend processes
pkill -f "uvicorn app.main" >/dev/null 2>&1

# Kill any existing frontend processes
pkill -f "npm start" >/dev/null 2>&1

# Wait a moment for the processes to terminate
sleep 2

echo "Starting backend service..."
# Start the backend service with environment variables
cd /Users/rahulpoojari/Documents/mlmodel
source venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
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
echo "API keys are loaded from the .env file"

# Wait for background processes
wait $BACKEND_PID $FRONTEND_PID