"""
Aadhaar-Only Training Script
---------------------------

This script trains a model specifically for Aadhaar card entity detection.
"""

import os
import sys
from pathlib import Path

def train_aadhar_model():
    """Train the Aadhaar detection model"""
    print("Training Aadhaar card entity detection model...")
    
    # Check if ultralytics is available
    try:
        from ultralytics import YOLO
        print("✓ Ultralytics library available")
    except ImportError:
        print("✗ Ultralytics library not found")
        print("Please install with: pip install ultralytics")
        return False
    
    # Check if dataset exists
    dataset_path = Path("aadhar")
    if not dataset_path.exists():
        print(f"✗ Dataset not found at {dataset_path}")
        return False
    
    # Check if data.yaml exists
    data_yaml = dataset_path / "data.yaml"
    if not data_yaml.exists():
        print(f"✗ Dataset configuration not found at {data_yaml}")
        return False
    
    print(f"✓ Using dataset: {data_yaml}")
    
    # Check if pretrained model exists
    pretrained_model = "yolov8n.pt"
    if not os.path.exists(pretrained_model):
        print(f"Downloading pretrained model {pretrained_model}...")
    
    # Train the model
    try:
        model = YOLO(pretrained_model)
        print("Starting training...")
        
        # Train with default parameters
        model.train(
            data=str(data_yaml),
            epochs=50,
            imgsz=640,
            batch=16,
            name="aadhar_detector",
            device="cpu"  # Change to "0" for GPU
        )
        
        print("✓ Training completed successfully")
        print("Model saved in runs/detect/aadhar_detector/")
        return True
        
    except Exception as e:
        print(f"✗ Training failed: {e}")
        return False

def validate_model():
    """Validate the trained model"""
    print("Validating trained model...")
    
    # Check if ultralytics is available
    try:
        from ultralytics import YOLO
        print("✓ Ultralytics library available")
    except ImportError:
        print("✗ Ultralytics library not found")
        return False
    
    # Check if trained model exists
    model_path = "runs/detect/aadhar_detector/weights/best.pt"
    if not os.path.exists(model_path):
        print(f"✗ Trained model not found at {model_path}")
        return False
    
    # Check if dataset config exists
    data_yaml = "aadhar/data.yaml"
    if not os.path.exists(data_yaml):
        print(f"✗ Dataset configuration not found at {data_yaml}")
        return False
    
    try:
        model = YOLO(model_path)
        print("Running validation...")
        
        metrics = model.val(
            data=data_yaml,
            device="cpu"  # Change to "0" for GPU
        )
        
        print("✓ Validation completed successfully")
        print(f"mAP@0.5: {metrics.box.map50}")
        print(f"mAP@0.5:0.95: {metrics.box.map}")
        return True
        
    except Exception as e:
        print(f"✗ Validation failed: {e}")
        return False

def main():
    """Main function"""
    print("=" * 50)
    print("Aadhaar Card Entity Detection - Training")
    print("=" * 50)
    
    print("1. Training model...")
    if train_aadhar_model():
        print("\n2. Validating model...")
        validate_model()
        
        print("\n" + "=" * 50)
        print("TRAINING PIPELINE COMPLETED")
        print("=" * 50)
        print("Next steps:")
        print("1. Start the API: python -m uvicorn app.main:app --reload")
        print("2. Test the API: python test_aadhar_api.py")
        print("3. Use the model directly: python demo_aadhar_inference.py")
        print("=" * 50)
    else:
        print("\nTraining failed!")

if __name__ == "__main__":
    main()