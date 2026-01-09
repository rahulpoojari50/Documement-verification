"""
Aadhaar Card Entity Detection Model
-----------------------------------

This script trains a YOLOv8 model on the Aadhaar card dataset for detecting
various entities on Aadhaar cards.

Dataset Information:
- 5 classes (labeled as '0', '1', '2', '3', '4')
- YOLO format with train/valid/test splits
- Bounding box annotations in normalized coordinates

Classes represent different entities on Aadhaar cards that need to be detected.
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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

def get_class_names():
    """Get class names from the data.yaml file"""
    import yaml
    
    try:
        with open("aadhar/data.yaml", 'r') as f:
            data = yaml.safe_load(f)
        
        class_names = data.get('names', [])
        print(f"Found {len(class_names)} classes: {class_names}")
        return class_names
    except Exception as e:
        print(f"Warning: Could not read class names from data.yaml: {e}")
        return ['0', '1', '2', '3', '4']  # Default class names

def train_model(epochs=50, imgsz=640, batch_size=16):
    """
    Train the YOLOv8 model on the Aadhaar dataset
    
    Args:
        epochs (int): Number of training epochs
        imgsz (int): Image size for training
        batch_size (int): Batch size for training
    """
    try:
        from ultralytics import YOLO
        print("✓ Ultralytics library imported successfully")
    except ImportError as e:
        print(f"ERROR: Cannot import ultralytics: {e}")
        print("Please install with: pip install ultralytics")
        return None
    
    # Check dataset first
    if not check_dataset():
        return None
    
    # Get class information
    class_names = get_class_names()
    num_classes = len(class_names)
    
    print(f"\nStarting model training with {num_classes} classes...")
    print(f"Classes: {class_names}")
    
    # Load a pretrained YOLOv8 model
    print("Loading pretrained YOLOv8 model...")
    model = YOLO('yolov8n.pt')  # Using nano version for faster training
    
    # Train the model
    print(f"Training model for {epochs} epochs...")
    print("This may take a while depending on your hardware...")
    
    try:
        # Updated syntax for newer versions of ultralytics
        results = model.train(
            data='aadhar/data.yaml',  # Path to dataset config
            epochs=epochs,            # Number of training epochs
            imgsz=imgsz,              # Image size
            batch=batch_size,         # Batch size (changed from batch_size to batch)
            name='aadhar_detector',   # Experiment name
            device='cpu',             # Use CPU (change to 0 for GPU)
            verbose=True              # Print detailed logs
        )
        print("✓ Training completed successfully!")
        return model
    except Exception as e:
        print(f"ERROR during training: {e}")
        return None

def validate_model(model):
    """Validate the trained model"""
    if model is None:
        print("ERROR: No model to validate")
        return None
        
    try:
        print("Validating model on validation set...")
        metrics = model.val()  # Validate on validation set
        print("✓ Validation completed")
        return metrics
    except Exception as e:
        print(f"ERROR during validation: {e}")
        return None

def main():
    """Main function to train and validate the Aadhaar detection model"""
    print("=" * 50)
    print("Aadhaar Card Entity Detection Model Trainer")
    print("=" * 50)
    
    # Train the model
    model = train_model(epochs=50, imgsz=640, batch_size=16)
    
    if model is None:
        print("Failed to train model")
        return
    
    # Validate the model
    metrics = validate_model(model)
    
    if metrics:
        print("\n" + "=" * 30)
        print("MODEL PERFORMANCE METRICS")
        print("=" * 30)
        print(f"mAP@0.5: {metrics.box.map50:.4f}")
        print(f"mAP@0.5:0.95: {metrics.box.map:.4f}")
        print(f"Precision: {metrics.box.p:.4f}")
        print(f"Recall: {metrics.box.r:.4f}")
        print("=" * 30)
    
    print("\nModel training pipeline completed!")
    print("Trained model saved in 'runs/detect/aadhar_detector/' directory")

if __name__ == "__main__":
    main()