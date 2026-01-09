#!/usr/bin/env python3
"""
Test script for PAN card verification functionality
"""

import requests
import os
from pathlib import Path

def test_pan_verification():
    """Test the PAN card verification endpoint"""
    
    # Define the API endpoint
    url = "http://localhost:8000/verify_pan_authenticity"
    
    # Find a PAN card sample in the data directory
    data_dir = Path("data/processed/train/original")
    
    # Look for PAN card samples
    pan_samples = list(data_dir.glob("*pan*"))
    
    if not pan_samples:
        print("No PAN card samples found in the data directory")
        return
    
    # Use the first PAN card sample
    pan_image_path = pan_samples[0]
    print(f"Testing with PAN card image: {pan_image_path}")
    
    # Prepare the file for upload
    try:
        with open(pan_image_path, "rb") as f:
            files = {"file": (pan_image_path.name, f, "image/jpeg")}
            
            # Send the request
            response = requests.post(url, files=files)
            
            # Check the response
            if response.status_code == 200:
                result = response.json()
                print("PAN Verification Result:")
                print(f"  Is Authentic: {result['is_authentic']}")
                print(f"  Confidence: {result['confidence']:.2f}")
                print(f"  PAN Pattern Detected: {result['pan_pattern_detected']}")
                print(f"  PAN Text Detected: {result['pan_text_detected']}")
                print(f"  Total Detections: {result['total_detections']}")
            else:
                print(f"Error: {response.status_code} - {response.text}")
                
    except Exception as e:
        print(f"Error testing PAN verification: {str(e)}")

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
    print("Testing PAN Card Verification System")
    print("=" * 40)
    
    # Test health check first
    test_health_check()
    print()
    
    # Test PAN verification
    test_pan_verification()