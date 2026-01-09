"""
Debug the advanced verification endpoint
"""

import requests
import os

def debug_advanced_verification():
    """Debug the advanced verification endpoint"""
    print("=== Debugging Advanced Verification Endpoint ===")
    
    # Test with our generated documents
    image_path = "/Users/rahulpoojari/Documents/mlmodel/test_docs/test_aadhaar_card.png"
    
    if not os.path.exists(image_path):
        print(f"❌ File not found: {image_path}")
        return
        
    print(f"--- Testing: {os.path.basename(image_path)} ---")
    
    try:
        with open(image_path, "rb") as f:
            files = {"file": (os.path.basename(image_path), f, "image/png")}
            response = requests.post("http://localhost:8000/advanced_verify_document", files=files)
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    debug_advanced_verification()