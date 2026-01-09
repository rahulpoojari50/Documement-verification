# Aadhaar Card Entity Detection System - Summary

## System Overview

I've analyzed your Aadhaar card dataset and created a complete solution for training and using an object detection model to identify entities on Aadhaar cards.

## Dataset Analysis

Your dataset has the following characteristics:
- **Format**: YOLO format with train/valid/test splits
- **Images**: 1,852 training, 529 validation, 265 test images
- **Annotations**: Bounding box labels in normalized coordinates
- **Classes**: 5 classes (labeled as '0', '1', '2', '3', '4')

## Solution Components

### 1. Model Training Scripts

I've created two approaches for training the model:

#### CLI Approach (Recommended)
```bash
# Training command
yolo detect train model=yolov8n.pt data=aadhar/data.yaml epochs=50 imgsz=640 batch=16 name=aadhar_detector device=cpu

# Validation command
yolo detect val model=runs/detect/aadhar_detector/weights/best.pt data=aadhar/data.yaml device=cpu
```

#### Python API Approach
- [aadhar_detection_model.py](file:///Users/rahulpoojari/Documents/mlmodel/aadhar_detection_model.py) - Direct Python API training
- [train_aadhar_cli.py](file:///Users/rahulpoojari/Documents/mlmodel/train_aadhar_cli.py) - Wrapper around CLI commands

### 2. Inference Scripts

- [aadhar_inference.py](file:///Users/rahulpoojari/Documents/mlmodel/aadhar_inference.py) - Script for running inference on new Aadhaar card images

### 3. Documentation

- [README_AADHAR_MODEL.md](file:///Users/rahulpoojari/Documents/mlmodel/README_AADHAR_MODEL.md) - Comprehensive guide for using the system

## How to Use This System

### Step 1: Install Dependencies
```bash
pip install ultralytics
```

### Step 2: Train the Model
Choose one of these approaches:

**Option A: CLI Training (Recommended)**
```bash
yolo detect train model=yolov8n.pt data=aadhar/data.yaml epochs=50 imgsz=640 batch=16 name=aadhar_detector device=cpu
```

**Option B: Python Script**
```bash
python aadhar_detection_model.py
```

### Step 3: Validate the Model
After training, validate the model performance:
```bash
yolo detect val model=runs/detect/aadhar_detector/weights/best.pt data=aadhar/data.yaml device=cpu
```

### Step 4: Run Inference
Use the trained model to detect entities on new Aadhaar card images:
```bash
python aadhar_inference.py
```

Or use the CLI directly:
```bash
yolo detect predict model=runs/detect/aadhar_detector/weights/best.pt source=path/to/aadhaar/image.jpg
```

## Expected Results

After training, you'll have:
- A trained YOLOv8 model optimized for Aadhaar card entity detection
- Performance metrics including mAP@0.5 and mAP@0.5:0.95
- Ability to detect all 5 classes of entities on Aadhaar cards
- Saved model weights for future use

## Customization Options

You can adjust these parameters for better performance:
- `epochs`: Increase for better accuracy (but longer training)
- `imgsz`: Adjust based on your hardware capabilities
- `batch`: Increase if you have more GPU memory
- `device`: Change to '0' to use GPU instead of CPU

## Notes About the Classes

The dataset currently has 5 classes labeled as '0', '1', '2', '3', '4'. To understand what each class represents, you would need to examine the actual Aadhaar cards and their annotations. Typically, these might represent:
- 0: Name field
- 1: Address field
- 2: Date of birth field
- 3: Aadhaar number field
- 4: Photo area

However, you should verify these based on your actual dataset annotations.