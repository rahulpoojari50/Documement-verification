"""
Demo Script for Aadhaar Detection Inference
------------------------------------------

This script demonstrates how to use the trained model for inference on Aadhaar cards.
"""

import sys
import os

def demo_inference():
    """Demonstrate inference using the trained model"""
    try:
        # Import ultralytics
        from ultralytics import YOLO
        print("✓ Ultralytics imported successfully")
        
        # Check if model exists
        model_path = "runs/detect/aadhar_detector/weights/best.pt"
        if not os.path.exists(model_path):
            print(f"✗ Model not found at {model_path}")
            print("Please train the model first.")
            return False
        
        # Load the trained model
        print(f"Loading trained model from {model_path}...")
        model = YOLO(model_path)
        print("✓ Model loaded successfully")
        
        # Find a sample image to test on
        train_images_path = "aadhar/train/images"
        if not os.path.exists(train_images_path):
            print(f"✗ Training images directory not found: {train_images_path}")
            return False
        
        # Get first image file
        image_files = [f for f in os.listdir(train_images_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if not image_files:
            print("✗ No image files found in training directory")
            return False
        
        sample_image = os.path.join(train_images_path, image_files[0])
        print(f"Running inference on sample image: {sample_image}")
        
        # Run inference
        print("Running inference...")
        results = model(sample_image)
        
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
                    print(f"    Object {j+1}: Class {class_id} with {confidence:.2f} confidence")
            else:
                print("  No objects detected")
        
        # Save results
        if result is not None:
            result.save(filename=f"aadhar_demo_result_{os.path.basename(sample_image)}")
            print(f"\nResults saved as: aadhar_demo_result_{os.path.basename(sample_image)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error during inference: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("Aadhaar Card Entity Detection - Inference Demo")
    print("=" * 60)
    
    print("This script demonstrates how to use the trained model for inference.")
    print("It will run detection on a sample Aadhaar card image from your dataset.")
    print()
    
    if demo_inference():
        print("\n✓ Inference demo completed successfully!")
        print("\nNext steps:")
        print("1. Check the generated result image with bounding boxes")
        print("2. Use aadhar_inference.py for processing multiple images")
        print("3. Integrate this approach into your application")
    else:
        print("\n✗ Inference demo failed!")

if __name__ == "__main__":
    main()