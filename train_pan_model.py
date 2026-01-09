#!/usr/bin/env python3
"""
Training script for PAN card entity detection model
"""

import os
import sys
import shutil
from pathlib import Path

# Attempt to import ultralytics
try:
    from ultralytics import YOLO
    ULTRALYTICS_AVAILABLE = True
except ImportError:
    ULTRALYTICS_AVAILABLE = False
    print("Warning: ultralytics not installed. Install with: pip install ultralytics")

def create_pan_annotations(image_path, output_label_path):
    """
    Create synthetic YOLO-format annotations for a PAN card image
    
    Args:
        image_path (str): Path to the PAN card image
        output_label_path (str): Path to save the YOLO annotation file
    """
    import cv2
    
    # Load image to get dimensions
    image = cv2.imread(str(image_path))
    if image is None:
        print(f"Could not load image: {image_path}")
        return False
    
    # Typical PAN card layout regions (approximate normalized coordinates)
    # These are based on standard PAN card layouts
    annotations = [
        # PAN Number (usually in top center)
        [0, 0.5, 0.15, 0.4, 0.08],  # class_id=0 (pan_number)
        
        # Name (usually below PAN number)
        [1, 0.5, 0.3, 0.6, 0.1],    # class_id=1 (name)
        
        # Father's Name (below name)
        [2, 0.5, 0.45, 0.6, 0.1],   # class_id=2 (fathers_name)
        
        # Date of Birth (below father's name)
        [3, 0.5, 0.6, 0.3, 0.08],   # class_id=3 (dob)
        
        # Photo (top right corner)
        [4, 0.85, 0.2, 0.2, 0.3],   # class_id=4 (photo)
        
        # Signature (bottom right)
        [5, 0.8, 0.8, 0.3, 0.1]     # class_id=5 (signature)
    ]
    
    # Write annotations to file
    with open(output_label_path, 'w') as f:
        for ann in annotations:
            f.write(f"{ann[0]} {ann[1]} {ann[2]} {ann[3]} {ann[4]}\n")
    
    return True

def prepare_pan_dataset():
    """
    Prepare the PAN dataset by organizing the data directories
    """
    print("Preparing PAN dataset structure...")
    
    # Define base paths
    data_root = Path("data")
    processed_root = data_root / "processed"
    
    # Create directory structure for YOLO training
    yolo_dirs = {
        'train': Path("train"),
        'valid': Path("valid"), 
        'test': Path("test")
    }
    
    # Create image and label subdirectories
    for split in yolo_dirs:
        (yolo_dirs[split] / "images").mkdir(parents=True, exist_ok=True)
        (yolo_dirs[split] / "labels").mkdir(parents=True, exist_ok=True)
    
    # Copy original PAN images to train set
    original_pan_dir = processed_root / "train" / "original"
    if original_pan_dir.exists():
        pan_images = list(original_pan_dir.glob("*pan*.jpg"))
        print(f"Found {len(pan_images)} original PAN images for training")
        
        # Copy images and create synthetic labels
        for i, img_path in enumerate(pan_images):
            # Copy image
            dest_img = yolo_dirs['train'] / "images" / img_path.name
            shutil.copy(img_path, dest_img)
            
            # Create synthetic label file
            label_path = yolo_dirs['train'] / "labels" / f"{img_path.stem}.txt"
            create_pan_annotations(img_path, label_path)
    
    # Copy validation PAN images
    valid_pan_dir = processed_root / "val" / "original"
    if valid_pan_dir.exists():
        pan_images = list(valid_pan_dir.glob("*pan*.jpg"))
        print(f"Found {len(pan_images)} validation PAN images")
        
        for img_path in pan_images:
            # Copy image
            dest_img = yolo_dirs['valid'] / "images" / img_path.name
            shutil.copy(img_path, dest_img)
            
            # Create synthetic label file
            label_path = yolo_dirs['valid'] / "labels" / f"{img_path.stem}.txt"
            create_pan_annotations(img_path, label_path)
    
    # Copy test PAN images
    test_pan_dir = processed_root / "test" / "original"
    if test_pan_dir.exists():
        pan_images = list(test_pan_dir.glob("*pan*.jpg"))
        print(f"Found {len(pan_images)} test PAN images")
        
        for img_path in pan_images:
            # Copy image
            dest_img = yolo_dirs['test'] / "images" / img_path.name
            shutil.copy(img_path, dest_img)
            
            # Create synthetic label file
            label_path = yolo_dirs['test'] / "labels" / f"{img_path.stem}.txt"
            create_pan_annotations(img_path, label_path)
    
    print("Dataset preparation completed!")

def create_pan_dataset_yaml():
    """
    Create a dataset configuration file specifically for PAN card training
    """
    # Create the dataset configuration
    pan_data = {
        'train': '../train/images',
        'val': '../valid/images',
        'test': '../test/images',
        'nc': 6,
        'names': ['pan_number', 'name', 'fathers_name', 'dob', 'photo', 'signature']
    }
    
    # Write to file
    pan_yaml_path = os.path.join('aadhar', 'pan_data.yaml')
    
    import yaml
    with open(pan_yaml_path, 'w') as f:
        yaml.dump(pan_data, f, default_flow_style=False)
    
    print(f"Created PAN dataset configuration at: {pan_yaml_path}")
    return pan_yaml_path

def train_pan_model(epochs=50, imgsz=640, batch=16):
    """
    Train a YOLOv8 model on the PAN card dataset
    
    Args:
        epochs (int): Number of training epochs
        imgsz (int): Image size for training
        batch (int): Batch size
    """
    if not ULTRALYTICS_AVAILABLE:
        print("Cannot train model: ultralytics library not available")
        print("Please install ultralytics with: pip install ultralytics")
        sys.exit(1)
    
    # Prepare dataset
    prepare_pan_dataset()
    
    # Create PAN-specific dataset configuration
    pan_yaml_path = create_pan_dataset_yaml()
    
    # Load a pretrained YOLOv8 model (using nano version for faster training)
    model = YOLO('yolov8n.pt')
    
    print(f"Training PAN card model with dataset: {pan_yaml_path}")
    print("This may take some time depending on your hardware...")
    
    # Train the model
    results = model.train(
        data=pan_yaml_path,     # Path to our dataset YAML file
        epochs=epochs,          # Number of epochs
        imgsz=imgsz,            # Image size for training
        batch=batch,            # Batch size
        name='pan_detector',    # Name of the training run
        device='cpu'            # Use CPU for training (change to 0 if you have a compatible GPU)
    )
    
    return model

def validate_model(model):
    """
    Validate the trained model on the validation set
    """
    if not ULTRALYTICS_AVAILABLE:
        print("Cannot validate model: ultralytics library not available")
        return None
        
    print("Validating model...")
    # Validate the model
    metrics = model.val()  # No arguments needed, uses validation set from data.yaml
    return metrics

def main():
    if not ULTRALYTICS_AVAILABLE:
        print("Required dependency 'ultralytics' not found.")
        print("Please install it with: pip install ultralytics")
        return
    
    print("Starting PAN card entity detection model training...")
    print("Using synthetic annotations based on typical PAN card layouts.")
    
    # Train the model with default parameters
    trained_model = train_pan_model(epochs=50, imgsz=640, batch=16)
    
    # Validate the model
    metrics = validate_model(trained_model)
    if metrics:
        print(f"Validation mAP50: {metrics.box.map50}")
        print(f"Validation mAP50-95: {metrics.box.map}")
    
    print("PAN card model training completed successfully!")
    print("Model saved in the 'runs/detect/pan_detector' directory")

if __name__ == "__main__":
    main()