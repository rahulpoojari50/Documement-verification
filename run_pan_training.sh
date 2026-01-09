#!/bin/bash

# PAN Card Model Training Script

echo "PAN Card Detection Model Training"
echo "================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install required packages
echo "Installing required packages..."
pip install ultralytics opencv-python pyyaml

# Check if pretrained model exists
if [ ! -f "yolov8n.pt" ]; then
    echo "Downloading pretrained YOLOv8 model..."
    wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
fi

# Run training
echo "Starting PAN card model training..."
python train_pan_model.py

echo "Training completed!"
echo "Model saved in runs/detect/pan_detector/weights/best.pt"