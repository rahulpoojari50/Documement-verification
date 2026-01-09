"""
Aadhaar Card Entity Detection Model - CLI Version
-------------------------------------------------

This script uses the ultralytics CLI to train a model on the Aadhaar dataset.
"""

import os
import subprocess
import sys
from pathlib import Path

def check_dataset():
    """Check if the Aadhaar dataset is properly structured"""
    dataset_path = Path("aadhar")
    required_files = ["data.yaml"]
    required_dirs = ["train", "valid", "test"]
    
    print("Checking Aadhaar dataset structure...")
    
    if not dataset_path.exists():
        print(f"ERROR: Dataset directory '{dataset_path}' not found")
        return False
        
    # Check for required files
    for file in required_files:
        if not (dataset_path / file).exists():
            print(f"ERROR: Required file '{file}' not found in dataset directory")
            return False
            
    # Check for required directories
    for dir_name in required_dirs:
        dir_path = dataset_path / dir_name
        if not dir_path.exists():
            print(f"ERROR: Required directory '{dir_name}' not found in dataset directory")
            return False
            
        # Check if images and labels subdirectories exist
        if not (dir_path / "images").exists() or not (dir_path / "labels").exists():
            print(f"ERROR: 'images' or 'labels' directory missing in '{dir_name}'")
            return False
    
    print("✓ Dataset structure verified")
    return True

def train_model_cli(epochs=50, imgsz=640, batch_size=16):
    """
    Train the model using ultralytics CLI
    """
    if not check_dataset():
        return False
    
    # Create the training command
    cmd = [
        "yolo", "train",
        "model=yolov8n.pt",           # Pretrained model
        "data=aadhar/data.yaml",      # Dataset configuration
        f"epochs={epochs}",           # Number of epochs
        f"imgsz={imgsz}",             # Image size
        f"batch={batch_size}",        # Batch size
        "name=aadhar_detector_cli",   # Experiment name
        "device=cpu"                  # Use CPU (change to device=0 for GPU)
    ]
    
    print("Executing training command:")
    print(" ".join(cmd))
    print("\nThis may take a while depending on your hardware...")
    
    try:
        # Execute the command
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Training completed successfully!")
            print(result.stdout)
            return True
        else:
            print("ERROR during training:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"ERROR executing training command: {e}")
        return False

def validate_model_cli():
    """
    Validate the trained model using ultralytics CLI
    """
    # Create the validation command
    cmd = [
        "yolo", "val",
        "model=runs/detect/aadhar_detector_cli/weights/best.pt",  # Trained model
        "data=aadhar/data.yaml",  # Dataset configuration
        "device=cpu"              # Use CPU (change to device=0 for GPU)
    ]
    
    print("Executing validation command:")
    print(" ".join(cmd))
    
    try:
        # Execute the command
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Validation completed successfully!")
            print(result.stdout)
            return True
        else:
            print("ERROR during validation:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"ERROR executing validation command: {e}")
        return False

def main():
    """Main function to train and validate the Aadhaar detection model"""
    print("=" * 50)
    print("Aadhaar Card Entity Detection Model Trainer (CLI)")
    print("=" * 50)
    
    # Train the model
    print("\nStarting model training...")
    success = train_model_cli(epochs=50, imgsz=640, batch_size=16)
    
    if not success:
        print("Failed to train model")
        return
    
    # Validate the model
    print("\nStarting model validation...")
    validate_model_cli()
    
    print("\nModel training pipeline completed!")
    print("Trained model saved in 'runs/detect/aadhar_detector_cli/' directory")

if __name__ == "__main__":
    main()