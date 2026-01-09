#!/bin/bash

# Set Gemini API key
# Note: The provided key appears to be a GitHub token, not a Gemini API key
# You'll need to obtain a proper Gemini API key from https://ai.google.dev/
export GEMINI_API_KEY="AIzaSyAT42Z-6k21CLgXBySM4kxsoesJ11SCBOk"

echo "Gemini API key has been set in the environment."
echo "Note: Using the default key as the provided token is not a valid Gemini API key."
echo "To use your own key, replace the value in this script."

# Kill any existing backend processes
pkill -f "uvicorn app.main" >/dev/null 2>&1

# Wait a moment for the process to terminate
sleep 2

# Start the backend service with the Gemini API key
cd /Users/rahulpoojari/Documents/mlmodel
source venv/bin/activate
GEMINI_API_KEY="AIzaSyAT42Z-6k21CLgXBySM4kxsoesJ11SCBOk" python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &

echo "Backend service restarted with Gemini API key."
echo "You can now use the Gemini verification feature in the document verification system."