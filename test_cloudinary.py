"""
Test script for Cloudinary integration
"""

import os
import sys
from cloudinary_integration import upload_verified_document, delete_document, list_documents, get_document_url

def test_cloudinary_functions():
    """Test all Cloudinary functions"""
    
    print("Testing Cloudinary Integration...")
    
    # Test 1: List existing documents
    print("\n1. Listing existing documents:")
    try:
        docs = list_documents()
        print(f"Found {len(docs['resources'])} documents")
        for doc in docs["resources"][:5]:  # Show first 5 documents
            print(f"  - {doc['secure_url']}")
    except Exception as e:
        print(f"Error listing documents: {e}")
    
    # Test 2: Upload a sample document (if exists)
    print("\n2. Testing document upload:")
    # Look for a sample image file in the project
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
                doc = upload_verified_document(filename)
                print(f"Successfully uploaded: {filename}")
                print(f"  Public ID: {doc['public_id']}")
                print(f"  URL: {doc['url']}")
                uploaded_doc = doc
                break
            except Exception as e:
                print(f"Error uploading {filename}: {e}")
        else:
            print(f"Sample file not found: {filename}")
    
    # Test 3: Get document URL
    if uploaded_doc:
        print("\n3. Testing URL retrieval:")
        url = get_document_url(uploaded_doc["public_id"])
        print(f"Retrieved URL: {url}")
    
    # Test 4: Delete document (optional - uncomment to test)
    # if uploaded_doc:
    #     print("\n4. Testing document deletion:")
    #     try:
    #         delete_document(uploaded_doc["public_id"])
    #         print("Document deleted successfully")
    #     except Exception as e:
    #         print(f"Error deleting document: {e}")
    
    print("\nCloudinary integration test completed.")

if __name__ == "__main__":
    test_cloudinary_functions()