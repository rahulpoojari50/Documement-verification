#!/bin/bash

# Set OpenAI API key
# NOTE: You need to obtain an actual OpenAI API key from https://platform.openai.com/
# The GitHub token you provided is NOT an OpenAI API key and will not work
export OPENAI_API_KEY="sk-your-actual-openai-api-key-here"

echo "OpenAI API key has been set in the environment."
echo "IMPORTANT: You must replace the placeholder with an actual OpenAI API key from https://platform.openai.com/"

# Kill any existing backend processes
pkill -f "uvicorn app.main" >/dev/null 2>&1

# Wait a moment for the process to terminate
sleep 2

# Start the backend service with the OpenAI API key
cd /Users/rahulpoojari/Documents/mlmodel
source venv/bin/activate
OPENAI_API_KEY="sk-your-actual-openai-api-key-here" python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &

echo "Backend service restarted with OpenAI API key."
echo "You can now use the OpenAI verification feature in the document verification system."