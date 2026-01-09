#!/usr/bin/env python3

import os
import google.generativeai as genai

def list_available_models():
    """List all available Gemini models"""
    try:
        # Set the API key
        api_key = "AIzaSyAT42Z-6k21CLgXBySM4kxsoesJ11SCBOk"
        genai.configure(api_key=api_key)
        
        # List all available models
        print("Available models:")
        for model in genai.list_models():
            print(f"- {model.name}: {model.display_name}")
            if hasattr(model, 'supported_generation_methods'):
                print(f"  Supported methods: {model.supported_generation_methods}")
            print()
            
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_available_models()