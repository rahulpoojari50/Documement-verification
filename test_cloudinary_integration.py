"""
Test the Cloudinary integration with the FastAPI backend
"""

import requests
import os
import json

# Base URL for the FastAPI backend
BASE_URL = "http://localhost:8000"

def test_list_documents():
    """Test listing documents"""
    print("Testing list documents endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/list_documents")
        if response.status_code == 200:
            docs = response.json()
            print(f"Successfully listed {len(docs.get('resources', []))} documents")
            for doc in docs.get('resources', [])[:3]:  # Show first 3 documents
                print(f"  - {doc.get('secure_url', 'No URL')}")
        else:
            print(f"Failed to list documents. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error listing documents: {e}")

def test_upload_document():
    """Test uploading a document"""
    print("\nTesting upload document endpoint...")
    
    # Look for a sample image file
    sample_files = [
        "sample_aadhaar.jpg",
        "sample_pan.jpg",
        "sample_voter_id.jpg",
        "test_image.jpg"
    ]
    
    uploaded_doc = None
    for filename in sample_files:
        if os.path.exists(filename):
            try:
                with open(filename, "rb") as f:
                    files = {"file": (filename, f, "image/jpeg")}
                    response = requests.post(f"{BASE_URL}/upload_verified_document", files=files)
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"Successfully uploaded: {filename}")
                    print(f"  Public ID: {result.get('public_id', 'N/A')}")
                    print(f"  URL: {result.get('url', 'N/A')}")
                    uploaded_doc = result
                    break
                else:
                    print(f"Failed to upload {filename}. Status code: {response.status_code}")
                    print(f"Response: {response.text}")
            except Exception as e:
                print(f"Error uploading {filename}: {e}")
        else:
            print(f"Sample file not found: {filename}")
    
    return uploaded_doc

def test_delete_document(public_id):
    """Test deleting a document"""
    print("\nTesting delete document endpoint...")
    if not public_id:
        print("No public ID provided, skipping delete test")
        return
    
    try:
        response = requests.delete(f"{BASE_URL}/delete_document/{public_id}")
        if response.status_code == 200:
            result = response.json()
            print(f"Successfully deleted document: {result.get('message', 'No message')}")
        else:
            print(f"Failed to delete document. Status code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error deleting document: {e}")

def main():
    """Run all tests"""
    print("Testing Cloudinary Integration with FastAPI Backend")
    print("=" * 50)
    
    # Test 1: List documents
    test_list_documents()
    
    # Test 2: Upload document
    uploaded_doc = test_upload_document()
    
    # Test 3: Delete document (optional - uncomment to test)
    # if uploaded_doc:
    #     test_delete_document(uploaded_doc.get("public_id"))
    
    print("\n" + "=" * 50)
    print("Cloudinary integration tests completed")

if __name__ == "__main__":
    main()