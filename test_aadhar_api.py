"""
Test Script for Aadhaar Detection API
-----------------------------------

This script tests the FastAPI endpoint for Aadhaar card entity detection.
"""

import requests
import os

def test_api_health():
    """Test the health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health")
        print("Health check response:")
        print(response.json())
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing health endpoint: {e}")
        return False

def test_detection_api():
    """Test the detection endpoint with a sample image"""
    # Find a sample Aadhaar image
    train_images_path = "aadhar/train/images"
    if not os.path.exists(train_images_path):
        print(f"Training images directory not found: {train_images_path}")
        return False
    
    # Get first image file
    image_files = [f for f in os.listdir(train_images_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not image_files:
        print("No image files found in training directory")
        return False
    
    sample_image = os.path.join(train_images_path, image_files[0])
    print(f"Testing detection on sample image: {sample_image}")
    
    try:
        with open(sample_image, "rb") as image_file:
            files = {"file": (os.path.basename(sample_image), image_file, "image/jpeg")}
            response = requests.post("http://localhost:8000/detect", files=files)
            
        print("Detection response:")
        print(response.json())
        return response.status_code == 200
    except Exception as e:
        print(f"Error testing detection endpoint: {e}")
        return False

def main():
    """Main function"""
    print("=" * 50)
    print("Aadhaar Detection API Test")
    print("=" * 50)
    
    print("1. Testing health endpoint...")
    if test_api_health():
        print("✓ Health check passed")
    else:
        print("✗ Health check failed")
        return
    
    print("\n2. Testing detection endpoint...")
    if test_detection_api():
        print("✓ Detection test passed")
    else:
        print("✗ Detection test failed")

if __name__ == "__main__":
    main()