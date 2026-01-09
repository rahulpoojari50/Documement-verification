"""
Simple Training Script for Aadhaar Detection Model
-------------------------------------------------

This is a simplified script to train the Aadhaar detection model.
"""

import subprocess
import sys

def train_model():
    """Train the model using the CLI approach"""
    print("Starting Aadhaar card entity detection model training...")
    print("This may take some time depending on your hardware...")
    
    # Training command
    cmd = [
        "yolo", "detect", "train",
        "model=yolov8n.pt",
        "data=aadhar/data.yaml",
        "epochs=50",
        "imgsz=640",
        "batch=16",
        "name=aadhar_detector",
        "device=cpu"
    ]
    
    print("Executing command:")
    print(" ".join(cmd))
    print()
    
    try:
        # Run the training command
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        # Print output in real-time
        if process.stdout is not None:
            for line in process.stdout:
                print(line, end='')
        
        # Wait for completion
        process.wait()
        
        if process.returncode == 0:
            print("\n✓ Training completed successfully!")
            print("Model saved in 'runs/detect/aadhar_detector/' directory")
            return True
        else:
            print(f"\n✗ Training failed with return code {process.returncode}")
            return False
            
    except Exception as e:
        print(f"✗ Error during training: {e}")
        return False

def validate_model():
    """Validate the trained model"""
    print("\nValidating trained model...")
    
    # Validation command
    cmd = [
        "yolo", "detect", "val",
        "model=runs/detect/aadhar_detector/weights/best.pt",
        "data=aadhar/data.yaml",
        "device=cpu"
    ]
    
    print("Executing command:")
    print(" ".join(cmd))
    print()
    
    try:
        # Run the validation command
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        
        # Print output in real-time
        if process.stdout is not None:
            for line in process.stdout:
                print(line, end='')
        
        # Wait for completion
        process.wait()
        
        if process.returncode == 0:
            print("\n✓ Validation completed successfully!")
            return True
        else:
            print(f"\n✗ Validation failed with return code {process.returncode}")
            return False
            
    except Exception as e:
        print(f"✗ Error during validation: {e}")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("Aadhaar Card Entity Detection Model Training")
    print("=" * 60)
    
    # Train the model
    if train_model():
        # Validate the model
        validate_model()
        
        print("\n" + "=" * 60)
        print("TRAINING PIPELINE COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("Next steps:")
        print("1. Use aadhar_inference.py to run detection on new images")
        print("2. Check runs/detect/aadhar_detector/ for training results")
        print("3. Find the best model at runs/detect/aadhar_detector/weights/best.pt")
        print("=" * 60)
    else:
        print("\nTraining failed. Please check the error messages above.")

if __name__ == "__main__":
    main()