"""
Direct Python Validation of Aadhaar Detection Model
--------------------------------------------------

This script directly validates the trained model using Python API.
"""

import sys
import os

def validate_model():
    """Validate the model using Python API"""
    try:
        # Add current directory to path
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        # Import ultralytics
        from ultralytics import YOLO
        print("✓ Ultralytics imported successfully")
        
        # Check if model exists
        model_path = "runs/detect/aadhar_detector/weights/best.pt"
        if not os.path.exists(model_path):
            print(f"✗ Model not found at {model_path}")
            return False
        
        print(f"Loading model from {model_path}...")
        model = YOLO(model_path)
        print("✓ Model loaded successfully")
        
        # Validate on validation set
        print("Validating model on validation set...")
        print("This may take a few minutes...")
        
        metrics = model.val(
            data="aadhar/data.yaml",
            device="cpu"
        )
        
        print("\n" + "=" * 50)
        print("VALIDATION RESULTS")
        print("=" * 50)
        
        # Display the metrics as they are (no formatting)
        print(f"mAP@0.5: {metrics.box.map50}")
        print(f"mAP@0.5:0.95: {metrics.box.map}")
        print(f"Precision: {metrics.box.p}")
        print(f"Recall: {metrics.box.r}")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"✗ Error during validation: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("Aadhaar Card Entity Detection - Direct Python Validation")
    print("=" * 60)
    
    if validate_model():
        print("\n✓ Model validation completed successfully!")
        print("\nNext steps:")
        print("1. Use aadhar_inference.py for detecting entities on new Aadhaar cards")
        print("2. Check the metrics above to understand model performance")
        print("3. Continue training with simple_train_aadhar.py if needed")
    else:
        print("\n✗ Model validation failed!")

if __name__ == "__main__":
    main()