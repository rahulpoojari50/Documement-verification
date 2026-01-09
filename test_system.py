#!/usr/bin/env python3
"""
Complete System Test Script
Tests all components of the document authenticity detection system
"""

import os
import sys
import subprocess
import time

def test_environment():
    """Test if all required packages are available"""
    print("Testing environment setup...")
    try:
        import torch
        import torchvision
        import cv2
        import numpy as np
        import fastapi
        import albumentations
        print("✅ All packages imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_data_preparation():
    """Test if data preparation completed successfully"""
    print("Testing data preparation...")
    required_paths = [
        "data/processed/train/fake",
        "data/processed/train/original",
        "data/processed/val/fake",
        "data/processed/val/original",
        "data/processed/test/fake",
        "data/processed/test/original"
    ]
    
    for path in required_paths:
        if not os.path.exists(path):
            print(f"❌ Missing directory: {path}")
            return False
        print(f"✅ Found directory: {path}")
    
    # Check if we have processed images
    fake_count = len([f for f in os.listdir("data/processed/train/fake") if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    original_count = len([f for f in os.listdir("data/processed/train/original") if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    
    print(f"✅ Training data - Fake: {fake_count}, Original: {original_count}")
    return True

def test_model_components():
    """Test if model components can be imported"""
    print("Testing model components...")
    try:
        # Test if we can import our scripts
        sys.path.append('scripts')
        from scripts.train import DocumentClassifier
        from scripts.data_prep import create_directories
        print("✅ Model components imported successfully")
        return True
    except Exception as e:
        print(f"❌ Model component error: {e}")
        return False

def test_api_components():
    """Test if API components can be imported"""
    print("Testing API components...")
    try:
        sys.path.append('app')
        from app.main import app
        print("✅ API components imported successfully")
        return True
    except Exception as e:
        print(f"❌ API component error: {e}")
        return False

def test_docker_files():
    """Test if Docker files exist"""
    print("Testing Docker setup...")
    required_files = ["Dockerfile", "docker-compose.yml"]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ Found {file}")
        else:
            print(f"❌ Missing {file}")
            return False
    return True

def main():
    """Run all tests"""
    print("=== Document Authenticity Detection System Test ===\n")
    
    tests = [
        test_environment,
        test_data_preparation,
        test_model_components,
        test_api_components,
        test_docker_files
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"=== Test Results: {passed}/{total} tests passed ===")
    
    if passed == total:
        print("🎉 All tests passed! Your system is ready for training and deployment.")
        print("\nNext steps:")
        print("1. Train the model: python3 scripts/train.py --epochs 5")
        print("2. Run the API: uvicorn app.main:app --reload")
        print("3. Start frontend: cd frontend && npm start")
    else:
        print("⚠️  Some tests failed. Please check the output above.")

if __name__ == "__main__":
    main()