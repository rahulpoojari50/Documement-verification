#!/usr/bin/env python3
"""
Script to create synthetic annotations for PAN card images based on typical PAN card layouts
"""

import os
import cv2
from pathlib import Path
import numpy as np

def create_pan_annotations(image_path, output_label_path):
    """
    Create synthetic YOLO-format annotations for a PAN card image
    
    Args:
        image_path (str): Path to the PAN card image
        output_label_path (str): Path to save the YOLO annotation file
    """
    # Load image to get dimensions
    image = cv2.imread(str(image_path))
    if image is None:
        print(f"Could not load image: {image_path}")
        return False
    
    height, width = image.shape[:2]
    
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

def process_pan_dataset():
    """
    Process all PAN card images and create synthetic annotations
    """
    print("Creating synthetic annotations for PAN card dataset...")
    
    # Define paths
    data_root = Path("data/processed")
    
    splits = ['train', 'val', 'test']
    
    total_processed = 0
    
    for split in splits:
        original_dir = data_root / split / "original"
        if not original_dir.exists():
            continue
            
        # Find PAN card images
        pan_images = list(original_dir.glob("*pan*.jpg"))
        
        print(f"Processing {len(pan_images)} PAN images in {split} set...")
        
        for img_path in pan_images:
            # Create corresponding label file path
            labels_dir = Path(split) / "labels"
            labels_dir.mkdir(parents=True, exist_ok=True)
            
            label_path = labels_dir / f"{img_path.stem}.txt"
            
            # Create annotation
            if create_pan_annotations(img_path, label_path):
                total_processed += 1
    
    print(f"Processed {total_processed} PAN card images with synthetic annotations.")

if __name__ == "__main__":
    process_pan_dataset()