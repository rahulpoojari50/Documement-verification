# Document Verification System (Aadhaar, PAN Cards & Driving Licenses)

## Overview

This repository contains a complete machine learning solution for detecting entities and verifying authenticity on Indian government-issued identification documents, including Aadhaar cards, PAN cards, and Driving Licenses. The system uses YOLOv8, a state-of-the-art object detection model, combined with OCR techniques to identify and verify document elements.

## Key Components

### 1. Dataset
- **Format**: YOLO format with train/valid/test splits
- **Size**: 1,852 training, 529 validation, 265 test images
- **Classes**: 5 entity classes (labeled as '0', '1', '2', '3', '4')
- **Annotations**: Bounding boxes in normalized coordinates
- **Document Types**: Aadhaar cards, PAN cards, and Driving Licenses

### 2. Trained Model
- **Architecture**: YOLOv8n (nano version for efficiency)
- **Performance**: 
  - mAP@0.5: 82.6%
  - mAP@0.5:0.95: 47.4%
  - Precision: 78.6%
  - Recall: 89.4%
- **Location**: [runs/detect/aadhar_detector/weights/best.pt](file:///Users/rahulpoojari/Documents/mlmodel/runs/detect/aadhar_detector/weights/best.pt)

### 3. Scripts

#### Training
- [simple_train_aadhar.py](file:///Users/rahulpoojari/Documents/mlmodel/simple_train_aadhar.py) - Simplified training script
- [aadhar_detection_model.py](file:///Users/rahulpoojari/Documents/mlmodel/aadhar_detection_model.py) - Python API approach
- [train_aadhar_cli.py](file:///Users/rahulpoojari/Documents/mlmodel/train_aadhar_cli.py) - CLI wrapper approach
- [train_dl_model.py](file:///Users/rahulpoojari/Documents/mlmodel/train_dl_model.py) - Driving License specialized training

#### Inference
- [aadhar_inference.py](file:///Users/rahulpoojari/Documents/mlmodel/aadhar_inference.py) - Complete inference system
- [demo_aadhar_inference.py](file:///Users/rahulpoojari/Documents/mlmodel/demo_aadhar_inference.py) - Demonstration script

#### Validation
- [direct_validate_aadhar.py](file:///Users/rahulpoojari/Documents/mlmodel/direct_validate_aadhar.py) - Direct Python validation
- [validate_aadhar_model.py](file:///Users/rahulpoojari/Documents/mlmodel/validate_aadhar_model.py) - CLI-based validation

#### Testing
- [test_aadhar_system.py](file:///Users/rahulpoojari/Documents/mlmodel/test_aadhar_system.py) - System component testing
- [test_ultralytics.py](file:///Users/rahulpoojari/Documents/mlmodel/test_ultralytics.py) - Library testing
- [test_pan_verification.py](file:///Users/rahulpoojari/Documents/mlmodel/test_pan_verification.py) - PAN verification testing
- [test_dl_verification.py](file:///Users/rahulpoojari/Documents/mlmodel/test_dl_verification.py) - Driving License verification testing

### 4. Documentation
- [README_AADHAR_MODEL.md](file:///Users/rahulpoojari/Documents/mlmodel/README_AADHAR_MODEL.md) - Detailed usage guide
- [AADHAR_FINAL_SUMMARY.md](file:///Users/rahulpoojari/Documents/mlmodel/AADHAR_FINAL_SUMMARY.md) - Final project summary
- [FINAL_AADHAR_SOLUTION.md](file:///Users/rahulpoojari/Documents/mlmodel/FINAL_AADHAR_SOLUTION.md) - Complete solution overview
- [PAN_VERIFICATION_README.md](file:///Users/rahulpoojari/Documents/mlmodel/PAN_VERIFICATION_README.md) - PAN card verification documentation
- [PAN_IMPLEMENTATION_SUMMARY.md](file:///Users/rahulpoojari/Documents/mlmodel/PAN_IMPLEMENTATION_SUMMARY.md) - PAN implementation details
- [COMPLETE_SYSTEM_SUMMARY.md](file:///Users/rahulpoojari/Documents/mlmodel/COMPLETE_SYSTEM_SUMMARY.md) - Complete system overview
- [DRIVING_LICENSE_TRAINING_README.md](file:///Users/rahulpoojari/Documents/mlmodel/DRIVING_LICENSE_TRAINING_README.md) - Driving License training documentation

## Quick Start

### 1. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 2. Run Inference Demo
```bash
python demo_aadhar_inference.py
```

### 3. Process Your Own Aadhaar Cards
```bash
python aadhar_inference.py
```

### 4. Start the Web Interface
```bash
# In one terminal, start the backend:
cd app && python main.py

# In another terminal, start the frontend:
cd frontend && npm start
```

### 5. Start with AI API Keys (Optional)

For enhanced document verification using AI services:

```bash
# Secure method - loads API keys from .env file:
./start_services_secure.sh

# Alternative methods:
# To start with both Gemini and OpenAI API keys configured:
./start_services_with_ai_keys.sh

# To set only the Gemini API key:
./set_gemini_key.sh

# To set only the OpenAI API key:
./set_openai_key.sh
```

Replace the placeholder API keys in the `.env` file or scripts with your actual API keys from:
- Gemini: https://ai.google.dev/
- OpenAI: https://platform.openai.com/

Create a `.env` file in the project root with your API keys:
```bash
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
GEMINI_API_KEY=your-gemini-api-key-here
```

## Model Performance

The trained model achieves excellent performance on the validation set:

| Metric | Value |
|--------|-------|
| mAP@0.5 | 82.6% |
| mAP@0.5:0.95 | 47.4% |
| Precision | 78.6% |
| Recall | 89.4% |

## Requirements

- Python 3.13.5
- Ultralytics 8.3.227
- PyTorch 2.9.0
- Node.js (for frontend)
- macOS (Apple M2) or compatible system

## Usage Examples

### CLI Inference
```bash
yolo detect predict model=runs/detect/aadhar_detector/weights/best.pt source=path/to/image.jpg
```

### Python Inference
```python
from ultralytics import YOLO

model = YOLO('runs/detect/aadhar_detector/weights/best.pt')
results = model('path/to/image.jpg')
```

## Web Interface Features

### Aadhaar Card Verification
1. **Entity Detection**:
   - Detects 5 key entities on Aadhaar cards
   - Provides bounding boxes with confidence scores
   - Calculates center coordinates and area measurements

2. **Authenticity Verification**:
   - Detects Indian emblem symbol in top-left corner
   - Verifies "Government of India" text using OCR
   - Provides authenticity confidence scoring

### PAN Card Verification
1. **Basic Pattern Detection**:
   - Analyzes top portion of document for PAN-specific patterns
   - Extracts and validates PAN number format using OCR

2. **Enhanced Verification** (New):
   - Comprehensive layout & template verification
   - Advanced text extraction & format validation
   - Visual & security feature inspection
   - Logo & issuer text verification
   - Tampering & forgery detection

3. **Authenticity Assessment**:
   - Combines all verification methods for comprehensive authenticity assessment

### AI-Powered Document Verification (New)
1. **Gemini AI Verification**:
   - Advanced document analysis using Google's Gemini AI
   - Comprehensive authenticity assessment with detailed explanations
   - Spelling error detection as primary authenticity determinant
   - Information extraction from document images

2. **OpenAI GPT Verification** (New):
   - Advanced document analysis using OpenAI's GPT models
   - Comprehensive authenticity assessment with detailed explanations
   - Spelling error detection as primary authenticity determinant
   - Information extraction from document images

### Driving License Verification
1. **Pattern Detection**:
   - Analyzes document layout for Driving License-specific patterns

2. **Text Verification**:
   - Extracts and validates Driving License number format using OCR

3. **Authenticity Assessment**:
   - Combines pattern and text analysis for authenticity verification

## About the Classes

The dataset contains 5 classes labeled as '0', '1', '2', '3', '4'. These likely represent:
- 0: Name field
- 1: Address field
- 2: Date of birth field
- 3: Aadhaar number field
- 4: Photo area

## Next Steps

1. Use the trained model for processing Aadhaar, PAN, and Driving License documents in your application
2. Fine-tune the model with additional data if needed
3. Deploy the model in a production environment
4. Extend the system to recognize additional entity types
5. Train dedicated models for PAN card and Driving License detection

## Support

For issues or questions, please check the documentation files or run the test scripts to verify system functionality.# Documement-verification
