#!/usr/bin/env python3
"""
Script to update the system to use the newly trained PAN model
"""

import os
import shutil
from pathlib import Path

def update_model_weights():
    """
    Update the system to use the newly trained PAN model weights
    """
    print("Updating system to use newly trained PAN model...")
    
    # Define paths
    trained_model_path = Path("runs/detect/pan_detector/weights/best.pt")
    target_model_path = Path("models/pan_model.pt")
    
    # Check if trained model exists
    if not trained_model_path.exists():
        print(f"Trained model not found at: {trained_model_path}")
        print("Please run the training first using:")
        print("python train_pan_model.py")
        return False
    
    # Create models directory if it doesn't exist
    target_model_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Copy the trained model to the models directory
    try:
        shutil.copy(trained_model_path, target_model_path)
        print(f"Successfully copied trained model to: {target_model_path}")
        return True
    except Exception as e:
        print(f"Failed to copy model: {e}")
        return False

def update_api_endpoint():
    """
    Update the API endpoint to use the PAN model
    """
    print("Updating API endpoint to use PAN model...")
    
    # This would typically involve modifying the app/main.py file
    # to load the PAN model instead of the general model
    # For now, we'll just print instructions
    print("To use the PAN model in the API:")
    print("1. Modify app/main.py to load models/pan_model.pt instead of yolov8n.pt")
    print("2. Or create a separate endpoint for PAN-specific detection")
    
    return True

def main():
    """
    Main update function
    """
    print("PAN Model Update Script")
    print("=" * 30)
    
    # Update model weights
    if update_model_weights():
        print("\n✓ Model weights updated successfully")
    else:
        print("\n✗ Failed to update model weights")
        return
    
    # Update API endpoint
    if update_api_endpoint():
        print("\n✓ API update instructions provided")
    else:
        print("\n✗ Failed to update API endpoint")
        return
    
    print("\nUpdate completed successfully!")
    print("\nNext steps:")
    print("1. Modify app/main.py to use the new PAN model")
    print("2. Restart the API server")
    print("3. Test the enhanced PAN verification")

if __name__ == "__main__":
    main()