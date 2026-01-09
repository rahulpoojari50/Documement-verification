import os
import sys

# Attempt to import ultralytics
try:
    from ultralytics import YOLO
    ULTRALYTICS_AVAILABLE = True
except ImportError:
    ULTRALYTICS_AVAILABLE = False
    print("Warning: ultralytics not installed. Install with: pip install ultralytics")

def create_dl_dataset_yaml():
    """
    Create a dataset configuration file specifically for Driving License training
    """
    # Create the dataset configuration
    dl_data = {
        'train': '../train/images',
        'val': '../valid/images',
        'test': '../test/images',
        'nc': 5,
        'names': ['dl_number', 'name', 'address', 'dob', 'photo']
    }
    
    # Write to file
    dl_yaml_path = os.path.join('aadhar', 'dl_data.yaml')
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(dl_yaml_path), exist_ok=True)
    
    import yaml
    with open(dl_yaml_path, 'w') as f:
        yaml.dump(dl_data, f, default_flow_style=False)
    
    print(f"Created Driving License dataset configuration at: {dl_yaml_path}")
    return dl_yaml_path

def train_dl_model():
    """
    Train a YOLOv8 model on the Driving License dataset
    """
    if not ULTRALYTICS_AVAILABLE:
        print("Cannot train model: ultralytics library not available")
        print("Please install ultralytics with: pip install ultralytics")
        sys.exit(1)
    
    # Create DL-specific dataset configuration
    dl_yaml_path = create_dl_dataset_yaml()
    
    # Load a pretrained YOLOv8 model (we'll use nano version for faster training)
    model = YOLO('yolov8n.pt')
    
    print(f"Training Driving License model with dataset: {dl_yaml_path}")
    print("This may take some time depending on your hardware...")
    
    # Train the model with fewer epochs for demonstration
    results = model.train(
        data=dl_yaml_path,     # Path to our dataset YAML file
        epochs=5,              # Reduced number of epochs for faster training
        imgsz=640,             # Image size for training
        batch=16,              # Batch size (adjust based on your GPU memory)
        name='dl_detector',    # Name of the training run
        device='cpu'           # Use CPU for training (change to 0 if you have a compatible GPU)
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
    
    print("Starting Driving License entity detection model training...")
    
    # Train the model
    trained_model = train_dl_model()
    
    # Validate the model
    metrics = validate_model(trained_model)
    if metrics:
        print(f"Validation mAP50: {metrics.box.map50}")
        print(f"Validation mAP50-95: {metrics.box.map}")
    
    print("Driving License model training completed successfully!")
    print("Model saved in the 'runs/detect/dl_detector' directory")

if __name__ == "__main__":
    main()