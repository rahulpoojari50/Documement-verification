# Enhanced PAN Card Verification Module

This module provides comprehensive verification of Indian PAN (Permanent Account Number) cards with advanced security checks and validation features.

## Features

### 1. Layout & Template Verification
- Detects standard PAN card layout and structure
- Verifies alignment and spacing between fields
- Compares with authoritative PAN templates
- Detects PVC vs paper versions
- Validates expected region positions for photo/signature

### 2. Text Extraction & Format Validation
- Uses OCR (Tesseract) to extract key fields:
  - Holder Name
  - Father's Name
  - Date of Birth (or Date of Allotment)
  - PAN Number
  - Signature text/area (if present as text)
- Validates PAN number format using regex: `^[A-Z]{5}[0-9]{4}[A-Z]$`
- Ensures DOB format is valid (DD/MM/YYYY or YYYY-MM-DD)
- Flags mismatches or impossible values (e.g., DOB in future)

### 3. Visual & Security Feature Inspection
- Verifies presence and position of photograph and signature block
- Checks for correct size and alignment of visual elements
- Detects security printing patterns (microtext/guilloche)
- Identifies lamination artifacts or PVC sheen
- Checks for color consistency and edges around pasted/edited regions

### 4. Logo & Issuer Text Check
- Confirms presence and correct spelling of issuing authority
- Validates microprint or small security texts
- Detects font mismatches

### 5. Tampering & Forgery Detection
- Uses image-based tamper detection:
  - Localized blur detection
  - Inconsistent noise levels
  - Unnatural borders around photo/text
  - Duplicate pixel regions
- Detects replaced photo or pasted regions via error level analysis
- Checks for inconsistent DPI or mixed-resampling artifacts

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Backend API Endpoint

The enhanced PAN verification is available through the `/verify_enhanced_pan_authenticity` endpoint:

```bash
curl -X POST "http://localhost:8000/verify_enhanced_pan_authenticity" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@path/to/pan_card.jpg"
```

### Direct Module Usage

```python
from pan_verification.pan_verifier import PanCardVerifier

# Initialize the verifier
verifier = PanCardVerifier()

# Verify a PAN card image
result = verifier.verify_pan_card("path/to/pan_card.jpg")

# Access verification results
print(f"Is Authentic: {result.is_authentic}")
print(f"Confidence: {result.confidence}")
print(f"PAN Number: {result.pan_number}")
```

## API Response Format

The API returns a JSON response with the following structure:

```json
{
  "is_authentic": true,
  "confidence": 0.95,
  "layout_verified": true,
  "text_validated": true,
  "security_features_verified": true,
  "issuer_verified": true,
  "tampering_detected": false,
  "pan_number": "ABCDE1234F",
  "holder_name": "John Doe",
  "fathers_name": "Jane Doe",
  "date_of_birth": "01/01/1990",
  "issues_found": [],
  "detected_entities": [...],
  "total_detections": 5
}
```

## Technical Details

### Verification Workflow

1. **Preprocessing**: Image is loaded and converted to appropriate formats for different analysis techniques
2. **Layout Analysis**: Verifies physical structure and dimensions of the PAN card
3. **Text Extraction**: OCR is performed to extract textual information
4. **Format Validation**: Extracted data is validated against expected formats and rules
5. **Security Inspection**: Visual security features are analyzed
6. **Issuer Verification**: Official texts and logos are checked
7. **Tampering Detection**: Image forensics techniques are applied
8. **Confidence Scoring**: Overall confidence is calculated based on all verification steps

### Confidence Scoring

The confidence score is calculated using a weighted system:
- Layout Verification: 20%
- Text Validation: 30%
- Security Features: 20%
- Issuer Verification: 15%
- Tampering Detection: -15% (if detected)

## Dependencies

- OpenCV for image processing
- Tesseract OCR for text extraction
- NumPy for numerical operations
- SciPy for scientific computing
- Scikit-learn for machine learning utilities

## Limitations

1. **OCR Accuracy**: Dependent on image quality and clarity
2. **Template Matching**: May not work with all variations of PAN card designs
3. **Security Feature Detection**: Some advanced security features may require specialized equipment
4. **Tampering Detection**: Sophisticated forgeries may not be detected

## Future Enhancements

1. **Deep Learning Models**: Train specialized models for PAN card verification
2. **Advanced Security Checks**: Implement more sophisticated security feature detection
3. **Multi-language Support**: Add support for regional language PAN cards
4. **Database Integration**: Connect to official PAN databases for verification
5. **Mobile Optimization**: Optimize for mobile device processing