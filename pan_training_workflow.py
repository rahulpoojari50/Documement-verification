#!/usr/bin/env python3
"""
Complete workflow for training and deploying PAN card detection model
"""

import os
import sys
import subprocess
from pathlib import Path

def check_prerequisites():
    """
    Check if all prerequisites are installed
    """
    print("Checking prerequisites...")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("✗ Python 3.7+ is required")
        return False
    
    # Check if pip is available
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        print("✓ pip is available")
    except subprocess.CalledProcessError:
        print("✗ pip is not available")
        return False
    
    # Check if required packages can be imported
    required_packages = ['ultralytics', 'cv2', 'yaml']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'cv2':
                import cv2
            elif package == 'yaml':
                import yaml
            else:
                __import__(package)
            print(f"✓ {package} is available")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} is not available")
    
    if missing_packages:
        print(f"Missing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install ultralytics opencv-python pyyaml")
        return False
    
    # Check if pretrained model exists
    if not Path("yolov8n.pt").exists():
        print("✗ Pretrained YOLOv8 model (yolov8n.pt) not found")
        print("Download it from: https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt")
        return False
    
    print("✓ All prerequisites met")
    return True

def run_training():
    """
    Run the PAN card model training
    """
    print("Starting PAN card model training...")
    
    try:
        # Import and run training
        sys.path.append('.')
        from train_pan_model import train_pan_model
        
        # Run training with default parameters
        # For a quick test, you can reduce epochs and batch size
        model = train_pan_model(epochs=50, batch=16, imgsz=640)
        
        print("✓ Training completed successfully")
        return True
        
    except Exception as e:
        print(f"✗ Training failed: {e}")
        return False

def deploy_model():
    """
    Deploy the trained model to the system
    """
    print("Deploying trained model...")
    
    # Check if trained model exists
    trained_model_path = Path("runs/detect/pan_detector/weights/best.pt")
    if not trained_model_path.exists():
        print(f"✗ Trained model not found at: {trained_model_path}")
        return False
    
    # Create models directory
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    # Copy trained model
    target_path = models_dir / "pan_model.pt"
    try:
        import shutil
        shutil.copy(trained_model_path, target_path)
        print(f"✓ Model deployed to: {target_path}")
        return True
    except Exception as e:
        print(f"✗ Failed to deploy model: {e}")
        return False

def update_api():
    """
    Update the API to use the new PAN model
    """
    print("Updating API to use PAN model...")
    
    api_file = Path("app/main.py")
    if not api_file.exists():
        print(f"✗ API file not found: {api_file}")
        return False
    
    # For now, we'll just print instructions
    # In a real implementation, you would modify the API code
    print("✓ API update instructions:")
    print("  1. Modify app/main.py to load 'models/pan_model.pt'")
    print("  2. Create a separate PAN detection endpoint if needed")
    print("  3. Restart the API server")
    
    return True

def main():
    """
    Main workflow function
    """
    print("PAN Card Detection Model Training and Deployment Workflow")
    print("=" * 60)
    
    # Step 1: Check prerequisites
    print("\nStep 1: Checking prerequisites...")
    if not check_prerequisites():
        print("\nPlease fix the prerequisite issues and try again.")
        return
    
    # Step 2: Run training
    print("\nStep 2: Running model training...")
    if not run_training():
        print("\nTraining failed. Please check the error messages.")
        return
    
    # Step 3: Deploy model
    print("\nStep 3: Deploying trained model...")
    if not deploy_model():
        print("\nModel deployment failed.")
        return
    
    # Step 4: Update API
    print("\nStep 4: Updating API...")
    if not update_api():
        print("\nAPI update failed.")
        return
    
    print("\n" + "=" * 60)
    print("Workflow completed successfully!")
    print("\nNext steps:")
    print("1. Modify app/main.py to use the new PAN model")
    print("2. Restart the API server: python app/main.py")
    print("3. Test the enhanced PAN verification through the web interface")
    print("4. Use the 'Enhanced PAN' tab to verify real PAN cards")

if __name__ == "__main__":
    main()