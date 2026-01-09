"""
Test Script for Aadhaar Detection System
---------------------------------------

This script verifies that all components of the Aadhaar detection system are properly set up.
"""

import os
import sys
from pathlib import Path

def test_ultralytics_installation():
    """Test if ultralytics is properly installed"""
    print("Testing ultralytics installation...")
    try:
        import ultralytics
        print(f"✓ Ultralytics version: {ultralytics.__version__}")
        
        from ultralytics import YOLO
        print("✓ YOLO class imported successfully")
        
        # Test model loading (this will download yolov8n.pt if not present)
        model = YOLO('yolov8n.pt')
        print("✓ YOLO model loaded successfully")
        
        return True
    except ImportError as e:
        print(f"✗ Failed to import ultralytics: {e}")
        return False
    except Exception as e:
        print(f"✗ Error loading YOLO model: {e}")
        return False

def test_dataset_structure():
    """Test if the Aadhaar dataset is properly structured"""
    print("\nTesting dataset structure...")
    
    dataset_path = Path("aadhar")
    if not dataset_path.exists():
        print("✗ Dataset directory 'aadhar' not found")
        return False
    
    # Check required files
    required_files = ["data.yaml"]
    for file in required_files:
        if not (dataset_path / file).exists():
            print(f"✗ Required file '{file}' not found")
            return False
    
    # Check required directories
    required_dirs = ["train", "valid", "test"]
    for dir_name in required_dirs:
        dir_path = dataset_path / dir_name
        if not dir_path.exists():
            print(f"✗ Required directory '{dir_name}' not found")
            return False
        
        # Check subdirectories
        if not (dir_path / "images").exists():
            print(f"✗ 'images' directory missing in '{dir_name}'")
            return False
        if not (dir_path / "labels").exists():
            print(f"✗ 'labels' directory missing in '{dir_name}'")
            return False
    
    print("✓ Dataset structure verified")
    return True

def test_yaml_config():
    """Test if the YAML configuration file is readable"""
    print("\nTesting YAML configuration...")
    
    try:
        import yaml
        config_path = Path("aadhar/data.yaml")
        if not config_path.exists():
            print("✗ data.yaml file not found")
            return False
            
        with open(config_path, 'r') as f:
            data = yaml.safe_load(f)
        
        print(f"✓ YAML file loaded successfully")
        print(f"  Number of classes: {data.get('nc', 'Not specified')}")
        print(f"  Class names: {data.get('names', 'Not specified')}")
        
        return True
    except Exception as e:
        print(f"✗ Error reading YAML configuration: {e}")
        return False

def test_sample_labels():
    """Test if sample label files can be read"""
    print("\nTesting sample label files...")
    
    try:
        # Try to read a sample label file
        label_dir = Path("aadhar/train/labels")
        if not label_dir.exists():
            print("✗ Label directory not found")
            return False
        
        # Get first .txt file
        label_files = list(label_dir.glob("*.txt"))
        if not label_files:
            print("✗ No label files found")
            return False
        
        # Read first label file
        with open(label_files[0], 'r') as f:
            lines = f.readlines()
        
        print(f"✓ Sample label file read successfully")
        print(f"  File: {label_files[0].name}")
        print(f"  Number of annotations: {len(lines)}")
        
        if lines:
            first_line = lines[0].strip().split()
            print(f"  First annotation format: {len(first_line)} values")
            print(f"  Values: {first_line}")
        
        return True
    except Exception as e:
        print(f"✗ Error reading label files: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Aadhaar Detection System - Component Tests")
    print("=" * 50)
    
    tests = [
        test_ultralytics_installation,
        test_dataset_structure,
        test_yaml_config,
        test_sample_labels
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()  # Add spacing between tests
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your system is ready for training.")
        print("\nNext steps:")
        print("1. Train the model:")
        print("   yolo detect train model=yolov8n.pt data=aadhar/data.yaml epochs=50 imgsz=640 batch=16")
        print("2. Or run the Python training script:")
        print("   python aadhar_detection_model.py")
    else:
        print("⚠ Some tests failed. Please check the errors above.")
    
    print("=" * 50)

if __name__ == "__main__":
    main()