# Driving License Model Training

This document provides instructions for training a specialized model for Indian Driving License verification.

## Overview

The system now supports training a dedicated YOLOv8 model for Driving License entity detection. This model is trained specifically on Driving License samples to improve accuracy for this document type.

## Prerequisites

1. Python 3.7 or higher
2. Required Python packages (install with `pip install -r requirements.txt`)
3. Ultralytics YOLOv8 library (`pip install ultralytics`)

## Training the Model

### 1. Prepare the Dataset

The training script uses the existing mixed dataset but creates a specialized configuration for Driving License training. The dataset already contains Driving License samples annotated with the same 5 entity classes:

- Class 0: Driving License Number
- Class 1: Name Field
- Class 2: Address Field
- Class 3: Date of Birth
- Class 4: Photo Area

### 2. Run the Training Script

Execute the training script:

```bash
python train_dl_model.py
```

This will:
1. Create a specialized dataset configuration file at `aadhar/dl_data.yaml`
2. Load a pretrained YOLOv8 nano model
3. Train the model on the mixed dataset with Driving License-focused class names
4. Save the trained model in the `runs/detect/dl_detector` directory

### 3. Training Parameters

The training script uses the following default parameters:
- Model: YOLOv8n (nano version for efficiency)
- Epochs: 50
- Image size: 640x640
- Batch size: 16
- Device: CPU (change to '0' for GPU training)

To modify these parameters, edit the [train_dl_model.py](file:///Users/rahulpoojari/Documents/mlmodel/train_dl_model.py) script.

## Model Performance

After training, the script will display validation metrics:
- mAP@0.5 (mean Average Precision at IoU threshold 0.5)
- mAP@0.5:0.95 (mean Average Precision across IoU thresholds 0.5-0.95)

## Using the Trained Model

The trained model can be used for Driving License verification through the existing API endpoint:
`POST /verify_driving_license_authenticity`

The model will be automatically loaded by the application if it's located in the expected directory.

## Future Improvements

For better performance, consider:
1. Creating a dedicated dataset with only Driving License samples
2. Adding more Driving License-specific annotations
3. Training with a larger, more diverse set of Driving License images
4. Fine-tuning hyperparameters for optimal performance