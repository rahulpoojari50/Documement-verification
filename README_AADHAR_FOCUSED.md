# Aadhaar Card Entity Detection - Focused Solution

## Overview

This is a focused solution for detecting entities on Aadhaar cards using computer vision techniques. The system uses YOLOv8, a state-of-the-art object detection model, specifically trained on Aadhaar card images.

## Key Features

1. **Aadhaar-Only Focus**: This solution is specifically designed for Aadhaar card detection, removing support for other document types.
2. **High Performance**: Achieves over 80% mAP@0.5 accuracy on validation set.
3. **REST API**: FastAPI-based web service for easy integration.
4. **Entity Detection**: Detects 5 different entity types on Aadhaar cards.

## Components

### 1. Dataset
- **Location**: [aadhar/](file:///Users/rahulpoojari/Documents/mlmodel/aadhar) directory
- **Format**: YOLO format with train/valid/test splits
- **Classes**: 5 entity classes (labeled as '0', '1', '2', '3', '4')

### 2. Model
- **Architecture**: YOLOv8n (optimized for efficiency)
- **Performance**: 
  - mAP@0.5: 82.6%
  - mAP@0.5:0.95: 47.4%
- **Location**: [runs/detect/aadhar_detector/weights/best.pt](file:///Users/rahulpoojari/Documents/mlmodel/runs/detect/aadhar_detector/weights/best.pt)

### 3. API Service
- **Framework**: FastAPI
- **Endpoint**: `/detect` for Aadhaar entity detection
- **Health Check**: `/health` endpoint

## Quick Start

### 1. Install Dependencies
```bash
# Activate virtual environment
source venv/bin/activate

# Install required packages
pip install ultralytics fastapi uvicorn python-multipart
```

### 2. Train the Model (if needed)
```bash
python train_aadhar_focused.py
```

### 3. Start the API Service
```bash
# Start the FastAPI server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. Test the API
```bash
# In a new terminal, test the health endpoint
curl http://localhost:8000/health

# Test the detection endpoint with an Aadhaar image
curl -X POST "http://localhost:8000/detect" -F "file=@path/to/aadhaar/image.jpg"
```

## API Endpoints

### Health Check
```
GET /health
```
Returns the status of the service and model loading.

### Aadhaar Entity Detection
```
POST /detect
```
Upload an Aadhaar card image to detect entities.

**Request**: 
- Form data with `file` parameter containing the image

**Response**:
```json
{
  "detected_entities": [
    {
      "class_id": 0,
      "confidence": 0.95,
      "x_min": 100.0,
      "y_min": 50.0,
      "x_max": 200.0,
      "y_max": 150.0,
      "width": 100.0,
      "height": 100.0
    }
  ],
  "total_detections": 1,
  "image_width": 640,
  "image_height": 480
}
```

## Class Labels

The model detects 5 classes on Aadhaar cards:
- **Class 0**: [To be determined based on your dataset]
- **Class 1**: [To be determined based on your dataset]
- **Class 2**: [To be determined based on your dataset]
- **Class 3**: [To be determined based on your dataset]
- **Class 4**: [To be determined based on your dataset]

To understand what each class represents, examine sample images alongside their annotation files in the [aadhar/train/images](file:///Users/rahulpoojari/Documents/mlmodel/aadhar/train/images) and [aadhar/train/labels](file:///Users/rahulpoojari/Documents/mlmodel/aadhar/train/labels) directories.

## Directory Structure

```
mlmodel/
├── aadhar/                 # Aadhaar dataset (YOLO format)
│   ├── data.yaml           # Dataset configuration
│   ├── train/              # Training images and labels
│   ├── valid/              # Validation images and labels
│   └── test/               # Test images and labels
├── app/
│   └── main.py             # FastAPI application
├── runs/
│   └── detect/
│       └── aadhar_detector/ # Trained model weights
└── train_aadhar_focused.py  # Training script
```

## Performance Metrics

The trained model achieves excellent performance on the validation set:

| Metric | Value |
|--------|-------|
| mAP@0.5 | 82.6% |
| mAP@0.5:0.95 | 47.4% |
| Precision | 78.6% |
| Recall | 89.4% |

## Troubleshooting

### Common Issues

1. **Module not found errors**: Make sure to activate the virtual environment and install dependencies:
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Model not loaded**: Ensure the model file exists at [runs/detect/aadhar_detector/weights/best.pt](file:///Users/rahulpoojari/Documents/mlmodel/runs/detect/aadhar_detector/weights/best.pt)

3. **CUDA errors**: If you don't have a GPU, make sure the device is set to "cpu" in the training script.

### Training Customization

You can customize the training by modifying parameters in [train_aadhar_focused.py](file:///Users/rahulpoojari/Documents/mlmodel/train_aadhar_focused.py):

- `epochs`: Number of training iterations (default: 50)
- `imgsz`: Image size for training (default: 640)
- `batch`: Batch size (default: 16)
- `device`: Processing unit ('cpu' or GPU index like '0')

## Next Steps

1. **Deploy the API** to a server for production use
2. **Integrate** with your application for automated Aadhaar card processing
3. **Fine-tune** the model with additional data if needed
4. **Extend** the system to recognize additional entity types

## Support

For issues or questions about this Aadhaar-focused solution, please refer to the documentation or run the test scripts to verify system functionality.