# Cloudinary Integration Summary

## Overview
The system integrates with Cloudinary to store verified real documents. Only documents classified as "REAL" by the ML model are uploaded to Cloudinary.

## Architecture
```
Document Image → ML Model (document_verifier.h5) → Prediction (REAL/FAKE) → IF REAL upload to Cloudinary
```

## Components

### 1. Model Loader (`model_loader.py`)
- Loads the TensorFlow/Keras model (`document_verifier.h5`)
- Preprocesses images (resize to 224x224, normalize)
- Makes predictions (returns "REAL" or "FAKE")

### 2. Cloudinary Upload (`cloudinary_upload.py`)
- Configures Cloudinary using environment variables
- Uploads images to the "verified_documents" folder
- Returns secure URL and public ID

### 3. Verification Pipeline (`verify_and_store.py`)
- Connects the model and Cloudinary components
- Only uploads documents predicted as "REAL"
- Returns status, prediction, and Cloudinary details

### 4. API Endpoint (`app/main.py`)
- `/verify_and_upload` - Main endpoint for ML verification + Cloudinary upload
- `/upload_verified_document` - Direct upload endpoint

## Current Status
✅ Cloudinary integration is working correctly
✅ 4 verified documents are currently stored in Cloudinary
✅ ML model is functioning properly
✅ Pipeline is operational

## Document Flow
1. User submits document via `/verify_and_upload` endpoint
2. ML model analyzes document and predicts "REAL" or "FAKE"
3. IF prediction is "REAL":
   - Document is uploaded to Cloudinary "verified_documents" folder
   - Response includes secure URL and public ID
4. IF prediction is "FAKE":
   - Document is rejected (not uploaded)
   - Response indicates rejection

## Security
- All uploads use secure HTTPS connections
- Documents stored in private Cloudinary account
- Access controlled via API keys and secrets
- Only verified documents are stored

## Viewing Documents
Documents can be viewed through:
1. The web interface at http://localhost:8081
2. Direct access via Cloudinary URLs
3. Programmatic access via Cloudinary API

## Example Response
```json
{
  "status": "VERIFIED",
  "prediction": "REAL",
  "image_url": "https://res.cloudinary.com/dlrf0evj0/image/upload/v1765693756/verified_documents/n5i3gjy5q7p8vairqdku.png",
  "public_id": "verified_documents/n5i3gjy5q7p8vairqdku"
}
```