"""
Aadhaar Card Inference Script
-----------------------------

This script demonstrates how to use a trained YOLOv8 model to detect entities on Aadhaar card images.
"""

import os
import sys
from pathlib import Path

def check_trained_model():
    """Check if a trained model exists"""
    model_path = Path("runs/detect/aadhar_detector/weights/best.pt")
    if model_path.exists():
        print(f"✓ Found trained model at: {model_path}")
        return str(model_path)
    else:
        print("⚠ Trained model not found. Have you trained the model yet?")
        print("Expected location: runs/detect/aadhar_detector/weights/best.pt")
        return None

def run_inference_on_image(image_path, model_path):
    """
    Run inference on a single Aadhaar card image
    
    Args:
        image_path (str): Path to the Aadhaar card image
        model_path (str): Path to the trained model
    """
    try:
        from ultralytics import YOLO
        print("✓ Ultralytics library imported successfully")
    except ImportError as e:
        print(f"ERROR: Cannot import ultralytics: {e}")
        print("Please install with: pip install ultralytics")
        return False
    
    # Check if image exists
    if not os.path.exists(image_path):
        print(f"ERROR: Image file not found: {image_path}")
        return False
    
    # Load the trained model
    print(f"Loading model from: {model_path}")
    model = YOLO(model_path)
    
    # Run inference
    print(f"Running inference on: {image_path}")
    results = model(image_path)
    
    # Display results
    print("\n" + "=" * 40)
    print("INFERENCE RESULTS")
    print("=" * 40)
    
    result = None
    for i, result in enumerate(results):
        print(f"Result {i+1}:")
        if result.boxes:
            boxes = result.boxes
            print(f"  Detected {len(boxes)} objects")
            for j, box in enumerate(boxes):
                class_id = int(box.cls.item())
                confidence = box.conf.item()
                xyxy = box.xyxy.tolist()[0]  # Bounding box coordinates
                print(f"    Object {j+1}: Class {class_id} with {confidence:.2f} confidence")
                print(f"      Bounding box: {xyxy}")
        else:
            print("  No objects detected")
    
    # Save results (if we have results)
    if result is not None:
        result.save(filename=f"aadhar_result_{os.path.basename(image_path)}")
        print(f"\nResults saved as: aadhar_result_{os.path.basename(image_path)}")
    
    return True

def run_batch_inference(image_directory, model_path):
    """
    Run inference on multiple Aadhaar card images
    
    Args:
        image_directory (str): Directory containing Aadhaar card images
        model_path (str): Path to the trained model
    """
    try:
        from ultralytics import YOLO
        print("✓ Ultralytics library imported successfully")
    except ImportError as e:
        print(f"ERROR: Cannot import ultralytics: {e}")
        print("Please install with: pip install ultralytics")
        return False
    
    # Check if directory exists
    if not os.path.exists(image_directory):
        print(f"ERROR: Directory not found: {image_directory}")
        return False
    
    # Get image files
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
    image_files = [f for f in os.listdir(image_directory) 
                   if os.path.splitext(f)[1].lower() in image_extensions]
    
    if not image_files:
        print(f"No image files found in: {image_directory}")
        return False
    
    print(f"Found {len(image_files)} image files")
    
    # Load the trained model
    print(f"Loading model from: {model_path}")
    model = YOLO(model_path)
    
    # Process each image
    successful_detections = 0
    for i, image_file in enumerate(image_files):
        image_path = os.path.join(image_directory, image_file)
        print(f"\nProcessing image {i+1}/{len(image_files)}: {image_file}")
        
        try:
            results = model(image_path)
            
            # Count detections
            detections = 0
            result = None
            for result in results:
                if result.boxes:
                    detections += len(result.boxes)
            
            print(f"  Detected {detections} objects")
            if detections > 0:
                successful_detections += 1
                
            # Save result (if we have results)
            if result is not None:
                result.save(filename=f"aadhar_result_{image_file}")
            
        except Exception as e:
            print(f"  ERROR processing {image_file}: {e}")
    
    print(f"\nBatch processing completed. Successfully processed {successful_detections}/{len(image_files)} images.")
    return True

def main():
    """Main function demonstrating inference usage"""
    print("=" * 50)
    print("Aadhaar Card Entity Detection - Inference")
    print("=" * 50)
    
    # Check for trained model
    model_path = check_trained_model()
    if not model_path:
        print("\nPlease train the model first using:")
        print("  python aadhar_detection_model.py")
        print("  or")
        print("  yolo detect train model=yolov8n.pt data=aadhar/data.yaml epochs=50 imgsz=640 batch=16")
        return
    
    print("\nInference Options:")
    print("1. Single image inference")
    print("2. Batch inference on directory")
    
    choice = input("\nEnter your choice (1 or 2): ").strip()
    
    if choice == "1":
        image_path = input("Enter path to Aadhaar card image: ").strip()
        if image_path:
            run_inference_on_image(image_path, model_path)
    elif choice == "2":
        directory_path = input("Enter path to directory containing Aadhaar card images: ").strip()
        if directory_path:
            run_batch_inference(directory_path, model_path)
    else:
        print("Invalid choice. Please run the script again and select 1 or 2.")

if __name__ == "__main__":
    main()