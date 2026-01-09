# Aadhaar Card Entity Detection System

This project trains a YOLOv8 model to detect entities on Aadhaar cards using a custom dataset.

## Dataset Information

The dataset contains Aadhaar card images with annotations for 5 different entity classes:
- Class 0: [Entity type 0 - to be determined based on actual data]
- Class 1: [Entity type 1 - to be determined based on actual data]
- Class 2: [Entity type 2 - to be determined based on actual data]
- Class 3: [Entity type 3 - to be determined based on actual data]
- Class 4: [Entity type 4 - to be determined based on actual data]

The dataset follows the YOLO format with the following structure:
```
aadhar/
├── data.yaml
├── train/
│   ├── images/
│   └── labels/
├── valid/
│   ├── images/
│   └── labels/
└── test/
    ├── images/
    └── labels/
```

## Installation

1. Install the required dependencies:
```bash
pip install ultralytics
```

## Training the Model

You can train the model using either the Python API or the CLI approach:

### Option 1: Python API Approach

```bash
python aadhar_detection_model.py
```

### Option 2: CLI Approach (Recommended)

```bash
# Training
yolo detect train model=yolov8n.pt data=aadhar/data.yaml epochs=50 imgsz=640 batch=16 name=aadhar_detector device=cpu

# Validation
yolo detect val model=runs/detect/aadhar_detector/weights/best.pt data=aadhar/data.yaml device=cpu
```

## Model Usage

After training, you can use the model to detect entities on new Aadhaar card images:

### Python Usage
```python
from ultralytics import YOLO

# Load the trained model
model = YOLO('runs/detect/aadhar_detector/weights/best.pt')

# Run prediction on an image
results = model('path/to/aadhaar/image.jpg')

# Process results
for result in results:
    boxes = result.boxes  # Boxes object for bbox outputs
    probs = result.probs  # Class probabilities for classification outputs
    # ... process results as needed
```

### CLI Usage
```bash
yolo detect predict model=runs/detect/aadhar_detector/weights/best.pt source=path/to/aadhaar/image.jpg
```

## Model Performance

The model performance will be displayed after training and validation. Key metrics include:
- mAP@0.5 (mean Average Precision at IoU threshold 0.5)
- mAP@0.5:0.95 (mean Average Precision across IoU thresholds 0.5-0.95)
- Precision and Recall values

## Customization

You can customize the training process by modifying the following parameters:
- `epochs`: Number of training epochs (default: 50)
- `imgsz`: Image size for training (default: 640)
- `batch`: Batch size (default: 16)
- `device`: Training device ('cpu' or GPU index like '0')

For GPU training, change `device=cpu` to `device=0` (or appropriate GPU index).