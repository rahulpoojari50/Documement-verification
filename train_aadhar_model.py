import os
import sys

# Attempt to import ultralytics
try:
    from ultralytics import YOLO
    ULTRALYTICS_AVAILABLE = True
except ImportError:
    ULTRALYTICS_AVAILABLE = False
    print("Warning: ultralytics not installed. Install with: pip install ultralytics")

def train_aadhar_model():
    """
    Train a YOLOv8 model on the Aadhaar card dataset
    """
    if not ULTRALYTICS_AVAILABLE:
        print("Cannot train model: ultralytics library not available")
        print("Please install ultralytics with: pip install ultralytics")
        sys.exit(1)
    
    # Load a pretrained YOLOv8 model (we'll use nano version for faster training)
    model = YOLO('yolov8n.pt')
    
    # Define the path to our dataset configuration
    data_yaml_path = os.path.join('aadhar', 'data.yaml')
    
    print(f"Training model with dataset: {data_yaml_path}")
    print("This may take some time depending on your hardware...")
    
    # Train the model
    results = model.train(
        data=data_yaml_path,  # Path to our dataset YAML file
        epochs=50,            # Number of training epochs
        imgsz=640,            # Image size for training
        batch_size=16,        # Batch size (adjust based on your GPU memory)
        name='aadhar_model',  # Name of the training run
        device='cpu'          # Use CPU for training (change to 0 if you have a compatible GPU)
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
    
    print("Starting Aadhaar card entity detection model training...")
    
    # Train the model
    trained_model = train_aadhar_model()
    
    # Validate the model
    metrics = validate_model(trained_model)
    if metrics:
        print(f"Validation mAP50: {metrics.box.map50}")
        print(f"Validation mAP50-95: {metrics.box.map}")
    
    print("Training completed successfully!")
    print("Model saved in the 'runs/detect/aadhar_model' directory")

if __name__ == "__main__":
    main()