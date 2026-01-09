"""
Validate Trained Aadhaar Detection Model
---------------------------------------

This script validates the existing trained model on the validation set.
"""

import subprocess
import os

def validate_existing_model():
    """Validate the existing trained model"""
    print("Validating existing Aadhaar detection model...")
    
    # Check if the model exists
    model_path = "runs/detect/aadhar_detector/weights/best.pt"
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}")
        print("Please train the model first using:")
        print("  python simple_train_aadhar.py")
        return False
    
    # Validation command
    cmd = [
        "yolo", "detect", "val",
        f"model={model_path}",
        "data=aadhar/data.yaml",
        "device=cpu",
        "verbose=True"
    ]
    
    print("Executing validation command:")
    print(" ".join(cmd))
    print()
    
    try:
        # Run the validation command
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Validation completed successfully!")
            print(result.stdout)
            return True
        else:
            print("✗ Validation failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ Error during validation: {e}")
        return False

def run_sample_inference():
    """Run inference on a sample image to demonstrate usage"""
    print("\nRunning sample inference...")
    
    # Check if the model exists
    model_path = "runs/detect/aadhar_detector/weights/best.pt"
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}")
        return False
    
    # Find a sample image
    train_images_path = "aadhar/train/images"
    if not os.path.exists(train_images_path):
        print(f"Training images directory not found: {train_images_path}")
        return False
    
    # Get first image file
    image_files = [f for f in os.listdir(train_images_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    if not image_files:
        print("No image files found in training directory")
        return False
    
    sample_image = os.path.join(train_images_path, image_files[0])
    print(f"Running inference on sample image: {sample_image}")
    
    # Inference command
    cmd = [
        "yolo", "detect", "predict",
        f"model={model_path}",
        f"source={sample_image}",
        "save=True",
        "device=cpu"
    ]
    
    try:
        # Run the inference command
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Sample inference completed successfully!")
            print("Results saved in the 'runs/detect/predict' directory")
            return True
        else:
            print("✗ Sample inference failed:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ Error during sample inference: {e}")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("Aadhaar Card Entity Detection - Model Validation")
    print("=" * 60)
    
    # Validate the existing model
    if validate_existing_model():
        # Run sample inference
        run_sample_inference()
        
        print("\n" + "=" * 60)
        print("VALIDATION COMPLETE!")
        print("=" * 60)
        print("Next steps:")
        print("1. Use aadhar_inference.py for batch processing")
        print("2. Check 'runs/detect/predict' for inference results")
        print("3. Continue training with simple_train_aadhar.py if needed")
        print("=" * 60)
    else:
        print("\nValidation failed. Please check the error messages above.")

if __name__ == "__main__":
    main()