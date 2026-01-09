"""
Comprehensive debug test for document verification and Cloudinary upload
"""

import requests
import os
import sys
sys.path.append('/Users/rahulpoojari/Documents/mlmodel')

from model_loader import predict_document
import tensorflow as tf

def debug_document_processing(image_path):
    """Debug the complete document processing pipeline"""
    print(f"=== Debugging Document: {image_path} ===")
    
    # Check if file exists
    if not os.path.exists(image_path):
        print(f"❌ File not found: {image_path}")
        return
    
    print(f"✅ File exists: {image_path}")
    print(f"📁 File size: {os.path.getsize(image_path)} bytes")
    
    # Test model prediction
    try:
        print("\n--- ML Model Prediction ---")
        prediction_result = predict_document(image_path)
        print(f"🤖 Model prediction: {prediction_result}")
    except Exception as e:
        print(f"❌ Model prediction failed: {e}")
        return
    
    # Test direct API call
    try:
        print("\n--- API Verification and Upload ---")
        with open(image_path, "rb") as f:
            files = {"file": (os.path.basename(image_path), f, "image/png")}
            response = requests.post("http://localhost:8000/verify_and_upload", files=files)
        
        print(f"🌐 API Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"📄 API Response: {result}")
            
            if result.get('status') == 'VERIFIED':
                print(f"✅ Document VERIFIED and uploaded to Cloudinary")
                print(f"🔗 Image URL: {result.get('image_url')}")
                print(f"🆔 Public ID: {result.get('public_id')}")
            elif result.get('status') == 'REJECTED':
                print(f"❌ Document REJECTED as FAKE")
                print(f"💬 Reason: {result.get('message')}")
            else:
                print(f"ℹ️ Other status: {result}")
        else:
            print(f"❌ API Error: {response.text}")
            
    except Exception as e:
        print(f"❌ API call failed: {e}")

def list_existing_documents():
    """List existing documents in Cloudinary"""
    print("\n=== Existing Cloudinary Documents ===")
    try:
        response = requests.get("http://localhost:8000/list_documents")
        if response.status_code == 200:
            result = response.json()
            resources = result.get('resources', [])
            print(f"📚 Found {len(resources)} documents in Cloudinary:")
            for i, resource in enumerate(resources, 1):
                print(f"  {i}. {resource.get('public_id', 'N/A')}")
                print(f"     🕐 Created: {resource.get('created_at', 'N/A')}")
                print(f"     🔗 URL: {resource.get('secure_url', 'N/A')[:50]}...")
                print()
        else:
            print(f"❌ Failed to list documents: {response.text}")
    except Exception as e:
        print(f"❌ Error listing documents: {e}")

def test_direct_upload(image_path):
    """Test direct upload to Cloudinary"""
    print(f"\n=== Direct Cloudinary Upload Test: {image_path} ===")
    
    if not os.path.exists(image_path):
        print(f"❌ File not found: {image_path}")
        return
    
    try:
        with open(image_path, "rb") as f:
            files = {"file": (os.path.basename(image_path), f, "image/png")}
            response = requests.post("http://localhost:8000/upload_verified_document", files=files)
        
        print(f"🌐 Direct Upload Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Direct upload successful!")
            print(f"🔗 URL: {result.get('url')}")
            print(f"🆔 Public ID: {result.get('public_id')}")
        else:
            print(f"❌ Direct upload failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Direct upload error: {e}")

def main():
    """Main debug function"""
    print("🔍 COMPREHENSIVE DOCUMENT VERIFICATION AND UPLOAD DEBUG")
    print("=" * 60)
    
    # Check if backend is running
    try:
        response = requests.get("http://localhost:8000/docs", timeout=5)
        print("✅ Backend service is running")
    except:
        print("❌ Backend service is NOT running. Please start it first.")
        return
    
    # Test with our generated documents
    test_images = [
        "/Users/rahulpoojari/Documents/mlmodel/test_docs/test_aadhaar_card.png",
        "/Users/rahulpoojari/Documents/mlmodel/test_docs/fake_aadhaar_card.png"
    ]
    
    for image_path in test_images:
        debug_document_processing(image_path)
        test_direct_upload(image_path)
    
    # List existing documents
    list_existing_documents()
    
    print("\n" + "=" * 60)
    print("💡 TIPS:")
    print("1. If documents are REJECTED, the ML model doesn't recognize them as REAL")
    print("2. If documents show as VERIFIED but don't appear in Cloudinary, check credentials")
    print("3. If direct upload works but verification doesn't, the issue is in the ML model")
    print("4. Check that the image files are valid and not corrupted")

if __name__ == "__main__":
    main()