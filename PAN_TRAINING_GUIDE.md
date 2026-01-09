# PAN Card Detection Model Training Guide

## Overview

This guide explains how to train a YOLOv8 model specifically for PAN card entity detection. The model will be able to detect key elements on PAN cards such as the PAN number, name, father's name, date of birth, photo, and signature.

## Prerequisites

1. Python 3.7+
2. Required Python packages:
   ```bash
   pip install ultralytics opencv-python pyyaml
   ```

## Dataset Structure

The PAN card detection model expects the following directory structure:

```
project/
├── train/
│   ├── images/
│   └── labels/
├── valid/
│   ├── images/
│   └── labels/
├── test/
│   ├── images/
│   └── labels/
└── aadhar/
    └── pan_data.yaml
```

## Training Process

### 1. Prepare the Dataset

Run the training script which will automatically:
- Organize PAN card images from the processed data directories
- Create synthetic annotations based on typical PAN card layouts
- Set up the proper directory structure for YOLO training

```bash
python train_pan_model.py
```

### 2. Training Configuration

The training script uses the following default parameters:
- **Model**: YOLOv8n (nano version for faster training)
- **Epochs**: 50
- **Image Size**: 640x640
- **Batch Size**: 16
- **Device**: CPU (change to '0' for GPU training)

You can customize these parameters by modifying the `train_pan_model()` function call in the main section.

### 3. Model Outputs

After training, the model will be saved in:
```
runs/detect/pan_detector/
```

The best performing model weights will be in:
```
runs/detect/pan_detector/weights/best.pt
```

## Improving Model Performance

### 1. Real Annotations

For production use, replace the synthetic annotations with real annotated data. Each annotation file should contain bounding boxes in YOLO format:
```
<class_id> <center_x> <center_y> <width> <height>
```

Where all values are normalized (0-1).

### 2. Increase Training Time

For better accuracy:
- Increase epochs to 100-200
- Use a larger model (yolov8s.pt or yolov8m.pt)
- Fine-tune hyperparameters

### 3. Data Augmentation

The YOLOv8 trainer automatically applies augmentations. You can customize these in the training configuration.

## Using the Trained Model

### 1. Inference Script

Create a simple inference script to test your trained model:

```python
from ultralytics import YOLO

# Load the trained model
model = YOLO('runs/detect/pan_detector/weights/best.pt')

# Run inference
results = model('path/to/pan_card_image.jpg')

# Process results
for result in results:
    boxes = result.boxes  # Boxes object for bbox outputs
    probs = result.probs  # Class probabilities for classification outputs
    keypoints = result.keypoints  # Keypoints for pose estimation
```

### 2. Integration with PAN Verification System

The trained model can be integrated with the existing PAN verification system by updating the model path in the API endpoint.

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure ultralytics is installed:
   ```bash
   pip install ultralytics
   ```

2. **Memory Issues**: Reduce batch size or image size:
   ```python
   train_pan_model(batch=8, imgsz=320)
   ```

3. **Slow Training**: Use GPU if available:
   ```python
   # In train_pan_model() function, change:
   device='0'  # instead of 'cpu'
   ```

## Next Steps

1. Collect and annotate real PAN card images for better accuracy
2. Experiment with different model sizes (yolov8s, yolov8m, yolov8l)
3. Fine-tune the model on specific types of PAN cards
4. Integrate with the enhanced PAN verification system

## Note on Synthetic Annotations

The current implementation uses synthetic annotations based on typical PAN card layouts. For production use, you should:

1. Collect real PAN card images with proper annotations
2. Use annotation tools like LabelImg or Roboflow to create accurate bounding boxes
3. Re-train the model with real annotated data for better performance