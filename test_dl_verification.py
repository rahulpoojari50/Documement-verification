#!/usr/bin/env python3
"""
Test script for Driving License verification functionality
"""

import requests
import os
from pathlib import Path

def test_dl_verification():
    """Test the Driving License verification endpoint"""
    
    # Define the API endpoint
    url = "http://localhost:8000/verify_driving_license_authenticity"
    
    # Find a Driving License sample in the data directory
    data_dir = Path("data/processed/train/original")
    
    # Look for Driving License samples
    dl_samples = list(data_dir.glob("*dl*"))
    
    if not dl_samples:
        print("No Driving License samples found in the data directory")
        return
    
    # Use the first Driving License sample
    dl_image_path = dl_samples[0]
    print(f"Testing with Driving License image: {dl_image_path}")
    
    # Prepare the file for upload
    try:
        with open(dl_image_path, "rb") as f:
            files = {"file": (dl_image_path.name, f, "image/jpeg")}
            
            # Send the request
            response = requests.post(url, files=files)
            
            # Check the response
            if response.status_code == 200:
                result = response.json()
                print("Driving License Verification Result:")
                print(f"  Is Authentic: {result['is_authentic']}")
                print(f"  Confidence: {result['confidence']:.2f}")
                print(f"  DL Pattern Detected: {result['dl_pattern_detected']}")
                print(f"  DL Text Detected: {result['dl_text_detected']}")
                print(f"  Total Detections: {result['total_detections']}")
            else:
                print(f"Error: {response.status_code} - {response.text}")
                
    except Exception as e:
        print(f"Error testing Driving License verification: {str(e)}")

def test_health_check():
    """Test the health check endpoint"""
    url = "http://localhost:8000/health"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            result = response.json()
            print("Health Check Result:")
            print(f"  Status: {result['status']}")
            print(f"  YOLO Available: {result['yolo_available']}")
            print(f"  Model Loaded: {result['model_loaded']}")
        else:
            print(f"Health check failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error during health check: {str(e)}")

if __name__ == "__main__":
    print("Testing Driving License Verification System")
    print("=" * 40)
    
    # Test health check first
    test_health_check()
    print()
    
    # Test Driving License verification
    test_dl_verification()