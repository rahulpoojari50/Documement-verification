#!/usr/bin/env python3
"""
Test script to verify environment variables are loaded correctly
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def test_env_vars():
    """Test that environment variables are loaded correctly"""
    print("Testing environment variables...")
    
    # Check if .env file exists
    if os.path.exists('.env'):
        print("✓ .env file found")
    else:
        print("✗ .env file not found")
    
    # Check OpenAI API key
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        if openai_key.startswith('sk-'):
            print("✓ OpenAI API key loaded correctly")
        else:
            print("⚠ OpenAI API key loaded but may not be valid (doesn't start with 'sk-')")
        print(f"  Key preview: {openai_key[:10]}...{openai_key[-4:]}")
    else:
        print("✗ OpenAI API key not found")
    
    # Check Gemini API key
    gemini_key = os.getenv('GEMINI_API_KEY')
    if gemini_key:
        if gemini_key.startswith('AI'):
            print("✓ Gemini API key loaded correctly")
        else:
            print("⚠ Gemini API key loaded but may not be valid (doesn't start with 'AI')")
        print(f"  Key preview: {gemini_key[:10]}...{gemini_key[-4:]}")
    else:
        print("✗ Gemini API key not found")

if __name__ == "__main__":
    test_env_vars()