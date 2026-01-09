#!/usr/bin/env python3

import os
import sys
import requests

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_gemini_endpoint():
    """Test the Gemini endpoint with a sample image"""
    # Set the Gemini API key
    os.environ["GEMINI_API_KEY"] = "AIzaSyAT42Z-6k21CLgXBySM4kxsoesJ11SCBOk"
    
    # Import the main module to initialize the app
    try:
        import app.main
        print("Successfully imported app.main")
    except Exception as e:
        print(f"Error importing app.main: {e}")
        return
    
    # Test the health endpoint
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Health check response: {response.status_code}")
        print(f"Health check data: {response.json()}")
    except Exception as e:
        print(f"Error with health check: {e}")
        return
    
    print("Gemini endpoint test completed")

if __name__ == "__main__":
    test_gemini_endpoint()