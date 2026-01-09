"""
Test the updated verification pipeline that uploads all documents
"""

import requests
import os

def test_updated_pipeline():
    """Test the updated pipeline that uploads all documents"""
    print("=== Testing Updated Verification Pipeline ===")
    
    # Test with our generated documents
    test_images = [
        "/Users/rahulpoojari/Documents/mlmodel/test_docs/test_aadhaar_card.png",
        "/Users/rahulpoojari/Documents/mlmodel/test_docs/fake_aadhaar_card.png"
    ]
    
    for image_path in test_images:
        if not os.path.exists(image_path):
            print(f"❌ File not found: {image_path}")
            continue
            
        print(f"\n--- Testing: {os.path.basename(image_path)} ---")
        
        try:
            with open(image_path, "rb") as f:
                files = {"file": (os.path.basename(image_path), f, "image/png")}
                response = requests.post("http://localhost:8000/verify_and_upload", files=files)
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Result: {result}")
                
                status = result.get('status')
                if status == 'VERIFIED':
                    print("✅ Document verified and uploaded")
                elif status == 'UPLOADED_WITH_WARNING':
                    print("⚠️ Document uploaded with ML warning")
                else:
                    print(f"ℹ️ Status: {status}")
                    
                print(f"🔗 URL: {result.get('image_url')}")
            else:
                print(f"❌ Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_updated_pipeline()