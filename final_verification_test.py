#!/usr/bin/env python3
"""
Final verification test for the complete document verification system
"""

import requests
import os
from pathlib import Path

def test_all_endpoints():
    """Test all API endpoints"""
    
    print("Testing Document Verification System")
    print("=" * 40)
    
    # Test health check
    print("1. Testing Health Check Endpoint...")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            result = response.json()
            print(f"   ✓ Status: {result['status']}")
            print(f"   ✓ YOLO Available: {result['yolo_available']}")
            print(f"   ✓ Model Loaded: {result['model_loaded']}")
        else:
            print(f"   ✗ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Health check error: {str(e)}")
        return False
    
    # Test Aadhaar detection endpoint (OPTIONS method to check CORS)
    print("\n2. Testing Aadhaar Detection Endpoint (CORS)...")
    try:
        response = requests.options("http://localhost:8000/detect")
        if response.status_code == 200:
            allow_header = response.headers.get('allow', '')
            print(f"   ✓ CORS configured: {allow_header}")
        else:
            print(f"   ✗ CORS check failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ CORS check error: {str(e)}")
    
    # Test Aadhaar authenticity endpoint (OPTIONS method to check CORS)
    print("\n3. Testing Aadhaar Authenticity Endpoint (CORS)...")
    try:
        response = requests.options("http://localhost:8000/verify_authenticity")
        if response.status_code == 200:
            allow_header = response.headers.get('allow', '')
            print(f"   ✓ CORS configured: {allow_header}")
        else:
            print(f"   ✗ CORS check failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ CORS check error: {str(e)}")
    
    # Test PAN authenticity endpoint (OPTIONS method to check CORS)
    print("\n4. Testing PAN Authenticity Endpoint (CORS)...")
    try:
        response = requests.options("http://localhost:8000/verify_pan_authenticity")
        if response.status_code == 200:
            allow_header = response.headers.get('allow', '')
            print(f"   ✓ CORS configured: {allow_header}")
        else:
            print(f"   ✗ CORS check failed: {response.status_code}")
    except Exception as e:
        print(f"   ✗ CORS check error: {str(e)}")
    
    # Test with actual Aadhaar sample
    print("\n5. Testing Aadhaar Detection with Sample Image...")
    data_dir = Path("data/processed/train/original")
    aadhar_samples = list(data_dir.glob("*aadhar*"))
    
    if aadhar_samples:
        aadhar_image_path = aadhar_samples[0]
        print(f"   Testing with: {aadhar_image_path.name}")
        try:
            with open(aadhar_image_path, "rb") as f:
                files = {"file": (aadhar_image_path.name, f, "image/jpeg")}
                response = requests.post("http://localhost:8000/detect", files=files)
                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✓ Detected {result['total_detections']} entities")
                    print(f"   ✓ Image size: {result['image_width']}x{result['image_height']}")
                else:
                    print(f"   ✗ Detection failed: {response.status_code}")
        except Exception as e:
            print(f"   ✗ Detection error: {str(e)}")
    else:
        print("   ⚠ No Aadhaar samples found for testing")
    
    # Test with actual PAN sample
    print("\n6. Testing PAN Verification with Sample Image...")
    pan_samples = list(data_dir.glob("*pan*"))
    
    if pan_samples:
        pan_image_path = pan_samples[0]
        print(f"   Testing with: {pan_image_path.name}")
        try:
            with open(pan_image_path, "rb") as f:
                files = {"file": (pan_image_path.name, f, "image/jpeg")}
                response = requests.post("http://localhost:8000/verify_pan_authenticity", files=files)
                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✓ PAN verification completed")
                    print(f"   ✓ Is authentic: {result['is_authentic']}")
                    print(f"   ✓ Confidence: {result['confidence']:.2f}")
                    print(f"   ✓ Detected {result['total_detections']} entities")
                else:
                    print(f"   ✗ PAN verification failed: {response.status_code}")
        except Exception as e:
            print(f"   ✗ PAN verification error: {str(e)}")
    else:
        print("   ⚠ No PAN samples found for testing")
    
    print("\n" + "=" * 40)
    print("Verification complete!")
    return True

if __name__ == "__main__":
    test_all_endpoints()