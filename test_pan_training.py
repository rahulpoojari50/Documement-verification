#!/usr/bin/env python3
"""
Test script for PAN card model training
"""

import os
import sys
from pathlib import Path

def test_training_setup():
    """
    Test that the training environment is properly set up
    """
    print("Testing PAN card training setup...")
    
    # Check if required directories exist
    required_dirs = [
        "data/processed/train/original",
        "data/processed/val/original", 
        "data/processed/test/original"
    ]
    
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            pan_count = len(list(path.glob("*pan*.jpg")))
            print(f"✓ Found {pan_count} PAN images in {dir_path}")
        else:
            print(f"✗ Directory not found: {dir_path}")
    
    # Check if ultralytics is available
    try:
        from ultralytics import YOLO
        print("✓ Ultralytics library is available")
    except ImportError:
        print("✗ Ultralytics library not found. Install with: pip install ultralytics")
        return False
    
    # Check if model file exists
    if Path("yolov8n.pt").exists():
        print("✓ Pretrained YOLOv8 model found")
    else:
        print("✗ Pretrained YOLOv8 model not found (yolov8n.pt)")
        print("  Download it from: https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt")
        return False
    
    return True

def run_sample_training():
    """
    Run a sample training with reduced parameters for testing
    """
    print("\nRunning sample PAN card training...")
    
    try:
        # Import the training module
        sys.path.append('.')
        from train_pan_model import train_pan_model
        
        # Run training with minimal parameters for testing
        print("Starting minimal training (1 epoch, small batch)...")
        model = train_pan_model(epochs=1, batch=4, imgsz=320)
        print("✓ Sample training completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Sample training failed: {e}")
        return False

def main():
    """
    Main test function
    """
    print("PAN Card Training Test")
    print("=" * 30)
    
    # Test environment setup
    if not test_training_setup():
        print("\nEnvironment setup test failed. Please fix the issues above.")
        return
    
    print("\nEnvironment setup test passed!")
    
    # Ask user if they want to run sample training
    response = input("\nDo you want to run a sample training test? (y/n): ")
    if response.lower() in ['y', 'yes']:
        if run_sample_training():
            print("\nSample training test completed successfully!")
            print("You can now run the full training with:")
            print("python train_pan_model.py")
        else:
            print("\nSample training test failed.")
    else:
        print("\nSkipping sample training. You can run the full training with:")
        print("python train_pan_model.py")

if __name__ == "__main__":
    main()