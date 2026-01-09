"""
Test uploading a real document to Cloudinary
"""

import requests
import os

def test_real_document_upload():
    """Test uploading a real document to Cloudinary via the verification pipeline"""
    # Path to our newly created test document
    test_doc_path = "/Users/rahulpoojari/Documents/mlmodel/test_docs/test_aadhaar_card.png"
    
    if not os.path.exists(test_doc_path):
        print(f"Test document not found: {test_doc_path}")
        return
    
    try:
        print("Testing real document upload...")
        print(f"Using document: {test_doc_path}")
        
        # Test the ML verification and upload endpoint
        with open(test_doc_path, "rb") as f:
            files = {"file": ("test_aadhaar_card.png", f, "image/png")}
            response = requests.post("http://localhost:8000/verify_and_upload", files=files)
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("Success!")
            print(f"Status: {result.get('status', 'N/A')}")
            print(f"Prediction: {result.get('prediction', 'N/A')}")
            
            if result.get('status') == 'VERIFIED':
                print(f"✅ Document verified as REAL and uploaded to Cloudinary")
                print(f"Image URL: {result.get('image_url', 'N/A')}")
                print(f"Public ID: {result.get('public_id', 'N/A')}")
            elif result.get('status') == 'REJECTED':
                print(f"❌ Document rejected as FAKE")
                print(f"Message: {result.get('message', 'N/A')}")
            else:
                print(f"ℹ️ Other status: {result}")
                
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

def test_fake_document_upload():
    """Test uploading a fake document to Cloudinary via the verification pipeline"""
    # Path to our newly created fake document
    fake_doc_path = "/Users/rahulpoojari/Documents/mlmodel/test_docs/fake_aadhaar_card.png"
    
    if not os.path.exists(fake_doc_path):
        print(f"Fake document not found: {fake_doc_path}")
        return
    
    try:
        print("\nTesting fake document upload...")
        print(f"Using document: {fake_doc_path}")
        
        # Test the ML verification and upload endpoint
        with open(fake_doc_path, "rb") as f:
            files = {"file": ("fake_aadhaar_card.png", f, "image/png")}
            response = requests.post("http://localhost:8000/verify_and_upload", files=files)
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("Success!")
            print(f"Status: {result.get('status', 'N/A')}")
            print(f"Prediction: {result.get('prediction', 'N/A')}")
            
            if result.get('status') == 'VERIFIED':
                print(f"✅ Document verified as REAL and uploaded to Cloudinary")
                print(f"Image URL: {result.get('image_url', 'N/A')}")
                print(f"Public ID: {result.get('public_id', 'N/A')}")
            elif result.get('status') == 'REJECTED':
                print(f"✅ Document correctly rejected as FAKE (expected behavior)")
                print(f"Message: {result.get('message', 'N/A')}")
            else:
                print(f"ℹ️ Other status: {result}")
                
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_real_document_upload()
    test_fake_document_upload()