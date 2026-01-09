"""
Test the ML verification and Cloudinary upload endpoint
"""

import requests
import base64
import os

# Create a simple test image
def create_test_image():
    """Create a simple test image for testing"""
    # Create a simple 1x1 pixel PNG image
    image_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    image_bytes = base64.b64decode(image_data)
    
    # Save to a test file
    with open("test_image.png", "wb") as f:
        f.write(image_bytes)
    
    print("Created test image: test_image.png")
    return "test_image.png"

def test_ml_verification():
    """Test the ML verification and Cloudinary upload endpoint"""
    print("Testing ML verification and Cloudinary upload endpoint...")
    
    # Create test image if it doesn't exist
    if not os.path.exists("test_image.png"):
        image_path = create_test_image()
    else:
        image_path = "test_image.png"
    
    try:
        # Test the endpoint
        with open(image_path, "rb") as f:
            files = {"file": ("test_image.png", f, "image/png")}
            response = requests.post("http://localhost:8000/verify_and_upload", files=files)
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("Success!")
            print(f"Status: {result.get('status', 'N/A')}")
            print(f"Prediction: {result.get('prediction', 'N/A')}")
            
            if result.get('status') == 'VERIFIED':
                print(f"✅ Document verified and uploaded to Cloudinary")
                print(f"Public ID: {result.get('public_id', 'N/A')}")
                print(f"URL: {result.get('image_url', 'N/A')}")
            elif result.get('status') == 'REJECTED':
                print(f"❌ Document rejected as FAKE")
                print(f"Message: {result.get('message', 'N/A')}")
            else:
                print(f"⚠️  Other status: {result.get('message', 'N/A')}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        # Clean up test image
        if os.path.exists("test_image.png"):
            os.remove("test_image.png")
            print("Cleaned up test image")

if __name__ == "__main__":
    test_ml_verification()