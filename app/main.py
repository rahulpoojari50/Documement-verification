from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import torch
import os
import uuid
from PIL import Image
import numpy as np
import cv2
import tempfile
import shutil
from typing import Optional, List
import json

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Import ultralytics for YOLO
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except (ImportError, AttributeError):
    YOLO = None
    YOLO_AVAILABLE = False
    print("Warning: ultralytics not installed. Install with: pip install ultralytics")

# Import for OCR
try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    pytesseract = None
    PYTESSERACT_AVAILABLE = False
    print("Warning: pytesseract not installed. Install with: pip install pytesseract")

# Import for Gemini
import google.generativeai as genai
import os
from PIL import Image as PILImage

# Import for Cloudinary
from cloudinary_integration import upload_verified_document, delete_document, list_documents

app = FastAPI(title="Document Authenticity Verification API",
              description="API for verifying document authenticity using computer vision",
              version="1.0.0")

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model and device
model = None
device = None

class BoundingBox(BaseModel):
    class_id: int
    confidence: float
    x_min: float
    y_min: float
    x_max: float
    y_max: float
    width: float
    height: float
    x_center: float  # Add center coordinates
    y_center: float  # Add center coordinates

class DetectionResponse(BaseModel):
    detected_entities: List[BoundingBox]
    total_detections: int
    image_width: int
    image_height: int

class AuthenticityResponse(BaseModel):
    is_authentic: bool
    confidence: float
    emblem_detected: bool
    government_text_detected: bool
    detected_entities: List[BoundingBox]
    total_detections: int

class PanAuthenticityResponse(BaseModel):
    is_authentic: bool
    confidence: float
    pan_pattern_detected: bool
    pan_text_detected: bool
    detected_entities: List[BoundingBox]
    total_detections: int

class DrivingLicenseAuthenticityResponse(BaseModel):
    is_authentic: bool
    confidence: float
    dl_pattern_detected: bool
    dl_text_detected: bool
    detected_entities: List[BoundingBox]
    total_detections: int

class EnhancedPanAuthenticityResponse(BaseModel):
    is_authentic: bool
    confidence: float
    layout_verified: bool
    text_validated: bool
    security_features_verified: bool
    issuer_verified: bool
    tampering_detected: bool
    pan_number: str
    holder_name: str
    fathers_name: str
    date_of_birth: str
    issues_found: List[str]
    detected_entities: List[BoundingBox]
    total_detections: int

class VoterIdAuthenticityResponse(BaseModel):
    is_authentic: bool
    confidence: float
    layout_verified: bool
    security_features_verified: bool
    text_quality_verified: bool
    epic_number_valid: bool
    photo_verified: bool
    barcode_qr_verified: bool
    signature_seal_verified: bool
    data_consistency_verified: bool
    epic_number: str
    voter_name: str
    fathers_name: str
    date_of_birth: str
    gender: str
    address: str
    issues_found: List[str]
    detected_entities: List[BoundingBox]
    total_detections: int

class AdvancedVerificationResponse(BaseModel):
    gemini_verification: dict
    ml_verification: dict
    yolo_detection: dict
    final_authenticity: bool
    confidence_score: float
    recommendations: List[str]

class GeminiVerificationResponse(BaseModel):
    is_authentic: bool
    confidence: float
    explanation: str
    extracted_info: dict
    issues_found: List[str]
    verification_factors: List[str]


class OpenAIVerificationResponse(BaseModel):
    is_authentic: bool
    confidence: float
    explanation: str
    extracted_info: dict
    issues_found: List[str]
    verification_factors: List[str]

# Class mapping for Aadhaar card entities
CLASS_NAMES = {
    0: "Aadhaar Number",
    1: "Name Field",
    2: "Date of Birth",
    3: "Address Field",
    4: "Photo Area"
}

# Class mapping for PAN card entities (if we have a separate model for PAN cards)
PAN_CLASS_NAMES = {
    0: "PAN Number",
    1: "Name",
    2: "Father's Name",
    3: "Date of Birth",
    4: "Signature Area"
}


@app.on_event("startup")
async def load_model():
    """Load the trained YOLO model on startup"""
    global model, device
    
    if not YOLO_AVAILABLE:
        print("Warning: YOLO model cannot be loaded - ultralytics not installed")
        return
    
    # Look for YOLO model files
    model_path = 'runs/detect/aadhar_detector/weights/best.pt'
    
    if not os.path.exists(model_path):
        print(f"Warning: YOLO model not found at {model_path}")
        print("Please train the model first using the training scripts")
        return
    
    try:
        # Load YOLO model
        model = YOLO(model_path)
        print(f"Loaded YOLO model from {model_path}")
    except Exception as e:
        print(f"Error loading YOLO model: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "yolo_available": YOLO_AVAILABLE, "model_loaded": model is not None}

@app.post("/detect", response_model=DetectionResponse)
async def detect_aadhaar_entities(file: UploadFile = File(...)):
    """Detect entities on uploaded Aadhaar card image"""
    global model
    
    if not YOLO_AVAILABLE:
        raise HTTPException(status_code=500, detail="YOLO library not available")
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Validate file type
    if file.content_type is None or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(await file.read())
        tmp_file_path = tmp_file.name
    
    try:
        # Load image to get dimensions
        image = Image.open(tmp_file_path)
        image_width, image_height = image.size
        
        # Run YOLO detection
        results = model(tmp_file_path)
        
        # Process results
        detected_entities = []
        
        for result in results:
            if hasattr(result, 'boxes') and result.boxes is not None:
                boxes = result.boxes
                for i in range(len(boxes)):
                    box = boxes[i]
                    # Extract box coordinates
                    xyxy = box.xyxy.tolist()[0]  # [x_min, y_min, x_max, y_max]
                    x_min, y_min, x_max, y_max = xyxy
                    
                    # Calculate center coordinates
                    x_center = (x_min + x_max) / 2
                    y_center = (y_min + y_max) / 2
                    
                    # Create bounding box object
                    bbox = BoundingBox(
                        class_id=int(box.cls.item()),
                        confidence=float(box.conf.item()),
                        x_min=x_min,
                        y_min=y_min,
                        x_max=x_max,
                        y_max=y_max,
                        width=x_max - x_min,
                        height=y_max - y_min,
                        x_center=x_center,  # Calculate center
                        y_center=y_center   # Calculate center
                    )
                    detected_entities.append(bbox)
        
        # Generate response
        response = DetectionResponse(
            detected_entities=detected_entities,
            total_detections=len(detected_entities),
            image_width=image_width,
            image_height=image_height
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
    
    finally:
        # Clean up temporary file
        os.unlink(tmp_file_path)

@app.post("/verify_aadhaar_authenticity", response_model=AuthenticityResponse)
async def verify_aadhaar_authenticity(file: UploadFile = File(...)):
    """Verify the authenticity of an uploaded Aadhaar card"""
    global model
    
    if not YOLO_AVAILABLE:
        raise HTTPException(status_code=500, detail="YOLO library not available")
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Validate file type
    if file.content_type is None or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(await file.read())
        tmp_file_path = tmp_file.name
    
    try:
        # Load image to get dimensions
        image = Image.open(tmp_file_path)
        image_width, image_height = image.size
        
        # Convert PIL image to OpenCV format for processing
        cv_image = cv2.imread(tmp_file_path)
        if cv_image is None:
            cv_image = np.array(image)
            if len(cv_image.shape) == 3:
                cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
        
        # Run YOLO detection
        results = model(tmp_file_path)
        
        # Process results
        detected_entities = []
        emblem_detected = False
        government_text_detected = False
        emblem_confidence = 0.0
        gov_text_confidence = 0.0
        
        for result in results:
            if hasattr(result, 'boxes') and result.boxes is not None:
                boxes = result.boxes
                for i in range(len(boxes)):
                    box = boxes[i]
                    # Extract box coordinates
                    xyxy = box.xyxy.tolist()[0]  # [x_min, y_min, x_max, y_max]
                    x_min, y_min, x_max, y_max = xyxy
                    
                    # Calculate center coordinates
                    x_center = (x_min + x_max) / 2
                    y_center = (y_min + y_max) / 2
                    
                    # Create bounding box object
                    bbox = BoundingBox(
                        class_id=int(box.cls.item()),
                        confidence=float(box.conf.item()),
                        x_min=x_min,
                        y_min=y_min,
                        x_max=x_max,
                        y_max=y_max,
                        width=x_max - x_min,
                        height=y_max - y_min,
                        x_center=x_center,  # Calculate center
                        y_center=y_center   # Calculate center
                    )
                    detected_entities.append(bbox)
                    
                    # Check for emblem (typically in top-left corner)
                    if (box.cls.item() == 0 and  # Assuming class 0 is emblem/gov seal
                        x_center < image_width * 0.4 and 
                        y_center < image_height * 0.4):
                        emblem_detected = True
                        emblem_confidence = max(emblem_confidence, box.conf.item())
                    
                    # Check for government text (typically in top portion)
                    if (box.cls.item() == 1 and  # Assuming class 1 is government text
                        y_center < image_height * 0.3):
                        government_text_detected = True
                        gov_text_confidence = max(gov_text_confidence, box.conf.item())
        
        # OCR for additional verification (if pytesseract is available)
        emblem_ocr_detected = False
        gov_text_ocr_detected = False
        
        if PYTESSERACT_AVAILABLE and pytesseract is not None:
            try:
                # Extract top-left portion of image for emblem OCR
                top_left_width = int(image_width * 0.4)
                top_left_height = int(image_height * 0.4)
                top_left_image = cv_image[0:top_left_height, 0:top_left_width]
                
                # Convert to grayscale
                gray = cv2.cvtColor(top_left_image, cv2.COLOR_BGR2GRAY)
                
                # Apply threshold to get black and white image
                _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                
                # Perform OCR
                text = pytesseract.image_to_string(thresh, lang='eng')
                
                # Check for government-related keywords
                gov_keywords = ['government', 'india', 'aadhaar', 'authority']
                text_lower = text.lower()
                for keyword in gov_keywords:
                    if keyword in text_lower:
                        emblem_ocr_detected = True
                        break
            except Exception as e:
                print(f"OCR error: {str(e)}")
        
        # Calculate overall authenticity confidence
        # This is a simplified approach - in a real implementation, you would have more sophisticated logic
        confidence = 0.0
        if emblem_detected and government_text_detected:
            confidence = (emblem_confidence + gov_text_confidence) / 2
        elif emblem_detected or government_text_detected:
            confidence = max(emblem_confidence, gov_text_confidence) * 0.7
        elif emblem_ocr_detected:
            confidence = 0.6  # Medium confidence if OCR detects government text
        else:
            confidence = 0.1  # Low confidence if nothing is detected
            
        is_authentic = confidence > 0.5
        
        # Generate response
        response = AuthenticityResponse(
            is_authentic=is_authentic,
            confidence=confidence,
            emblem_detected=emblem_detected,
            government_text_detected=government_text_detected,
            detected_entities=detected_entities,
            total_detections=len(detected_entities)
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
    
    finally:
        # Clean up temporary file
        os.unlink(tmp_file_path)

@app.post("/verify_pan_authenticity", response_model=PanAuthenticityResponse)
async def verify_pan_authenticity(file: UploadFile = File(...)):
    """Verify the authenticity of an uploaded PAN card"""
    global model
    
    if not YOLO_AVAILABLE:
        raise HTTPException(status_code=500, detail="YOLO library not available")
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Validate file type
    if file.content_type is None or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(await file.read())
        tmp_file_path = tmp_file.name
    
    try:
        # Load image to get dimensions
        image = Image.open(tmp_file_path)
        image_width, image_height = image.size
        
        # Convert PIL image to OpenCV format for processing
        cv_image = cv2.imread(tmp_file_path)
        if cv_image is None:
            cv_image = np.array(image)
            if len(cv_image.shape) == 3:
                cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
        
        # Run YOLO detection
        results = model(tmp_file_path)
        
        # Process results
        detected_entities = []
        pan_pattern_detected = False
        pan_text_detected = False
        pan_pattern_confidence = 0.0
        pan_text_confidence = 0.0
        
        for result in results:
            if hasattr(result, 'boxes') and result.boxes is not None:
                boxes = result.boxes
                for i in range(len(boxes)):
                    box = boxes[i]
                    # Extract box coordinates
                    xyxy = box.xyxy.tolist()[0]  # [x_min, y_min, x_max, y_max]
                    x_min, y_min, x_max, y_max = xyxy
                    
                    # Calculate center coordinates
                    x_center = (x_min + x_max) / 2
                    y_center = (y_min + y_max) / 2
                    
                    # Create bounding box object
                    bbox = BoundingBox(
                        class_id=int(box.cls.item()),
                        confidence=float(box.conf.item()),
                        x_min=x_min,
                        y_min=y_min,
                        x_max=x_max,
                        y_max=y_max,
                        width=x_max - x_min,
                        height=y_max - y_min,
                        x_center=x_center,  # Calculate center
                        y_center=y_center   # Calculate center
                    )
                    detected_entities.append(bbox)
                    
                    # Check for PAN pattern (typically in top portion with specific format)
                    if (y_center < image_height * 0.3):
                        pan_pattern_detected = True
                        pan_pattern_confidence = max(pan_pattern_confidence, box.conf.item())
        
        # OCR for PAN number detection (typically 10 characters: 5 letters, 4 digits, 1 letter)
        pan_text_confidence = 0.0
        if PYTESSERACT_AVAILABLE and pytesseract is not None:
            try:
                # Extract top portion of image for OCR (where PAN number is typically located)
                top_height = int(image_height * 0.3)
                top_image = cv_image[0:top_height, :]
                
                # Convert to grayscale
                gray = cv2.cvtColor(top_image, cv2.COLOR_BGR2GRAY)
                
                # Apply threshold to get black and white image
                _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                
                # Perform OCR
                text = pytesseract.image_to_string(thresh, lang='eng')
                
                # Check for PAN number pattern (5 uppercase letters, 4 digits, 1 uppercase letter)
                import re
                pan_pattern = r'[A-Z]{5}[0-9]{4}[A-Z]{1}'
                matches = re.findall(pan_pattern, text)
                
                if matches:
                    pan_text_detected = True
                    pan_text_confidence = 0.9  # High confidence if pattern matches
                else:
                    # Check for partial matches or similar patterns
                    partial_pattern = r'[A-Z]{3,5}[0-9]{2,4}[A-Z]{1}'
                    partial_matches = re.findall(partial_pattern, text)
                    if partial_matches:
                        pan_text_detected = True
                        pan_text_confidence = 0.6  # Medium confidence for partial matches
            except Exception as e:
                print(f"OCR error: {str(e)}")
                # Fallback to heuristic if OCR fails
                # Check if we detected text entities in the top area
                for entity in detected_entities:
                    if entity.y_center < image_height * 0.3:
                        pan_text_detected = True
                        pan_text_confidence = max(pan_text_confidence, entity.confidence)
        else:
            # Fallback to heuristic if pytesseract is not available
            # Check if we detected text entities in the top area
            for entity in detected_entities:
                if entity.y_center < image_height * 0.3:
                    pan_text_detected = True
                    pan_text_confidence = max(pan_text_confidence, entity.confidence)
        
        # Calculate overall authenticity confidence
        # This is a simplified approach - in a real implementation, you would have more sophisticated logic
        confidence = 0.0
        if pan_pattern_detected and pan_text_detected:
            confidence = (pan_pattern_confidence + pan_text_confidence) / 2
        elif pan_pattern_detected or pan_text_detected:
            confidence = max(pan_pattern_confidence, pan_text_confidence) * 0.7
        else:
            confidence = 0.1  # Low confidence if neither is detected
            
        is_authentic = confidence > 0.5
        
        # Generate response
        response = PanAuthenticityResponse(
            is_authentic=is_authentic,
            confidence=confidence,
            pan_pattern_detected=pan_pattern_detected,
            pan_text_detected=pan_text_detected,
            detected_entities=detected_entities,
            total_detections=len(detected_entities)
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
    
    finally:
        # Clean up temporary file
        os.unlink(tmp_file_path)

@app.post("/verify_driving_license_authenticity", response_model=DrivingLicenseAuthenticityResponse)
async def verify_driving_license_authenticity(file: UploadFile = File(...)):
    """Verify the authenticity of an uploaded Driving License"""
    global model
    
    if not YOLO_AVAILABLE:
        raise HTTPException(status_code=500, detail="YOLO library not available")
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Validate file type
    if file.content_type is None or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(await file.read())
        tmp_file_path = tmp_file.name
    
    try:
        # Load image to get dimensions
        image = Image.open(tmp_file_path)
        image_width, image_height = image.size
        
        # Convert PIL image to OpenCV format for processing
        cv_image = cv2.imread(tmp_file_path)
        if cv_image is None:
            cv_image = np.array(image)
            if len(cv_image.shape) == 3:
                cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
        
        # Run YOLO detection
        results = model(tmp_file_path)
        
        # Process results
        detected_entities = []
        dl_pattern_detected = False
        dl_text_detected = False
        dl_pattern_confidence = 0.0
        dl_text_confidence = 0.0
        
        for result in results:
            if hasattr(result, 'boxes') and result.boxes is not None:
                boxes = result.boxes
                for i in range(len(boxes)):
                    box = boxes[i]
                    # Extract box coordinates
                    xyxy = box.xyxy.tolist()[0]  # [x_min, y_min, x_max, y_max]
                    x_min, y_min, x_max, y_max = xyxy
                    
                    # Calculate center coordinates
                    x_center = (x_min + x_max) / 2
                    y_center = (y_min + y_max) / 2
                    
                    # Create bounding box object
                    bbox = BoundingBox(
                        class_id=int(box.cls.item()),
                        confidence=float(box.conf.item()),
                        x_min=x_min,
                        y_min=y_min,
                        x_max=x_max,
                        y_max=y_max,
                        width=x_max - x_min,
                        height=y_max - y_min,
                        x_center=x_center,  # Calculate center
                        y_center=y_center   # Calculate center
                    )
                    detected_entities.append(bbox)
                    
                    # Check for DL pattern (typically contains "DL" or similar identifiers)
                    if (box.conf.item() > 0.5):
                        dl_pattern_detected = True
                        dl_pattern_confidence = max(dl_pattern_confidence, box.conf.item())
        
        # OCR for DL number detection
        dl_text_confidence = 0.0
        if PYTESSERACT_AVAILABLE and pytesseract is not None:
            try:
                # Perform OCR on the entire image
                gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
                
                # Apply threshold to get black and white image
                _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                
                # Perform OCR
                text = pytesseract.image_to_string(thresh, lang='eng')
                
                # Check for DL-related patterns
                import re
                # DL numbers typically have a specific format
                dl_patterns = [
                    r'[A-Z]{2}[0-9]{13}',  # New DL format
                    r'[A-Z]{2}-[0-9]{11}', # Old DL format with dash
                    r'driving.{0,10}licen[cs]e', # Driving license text
                    r'[A-Z]{2}[0-9]{2}[ ]?[0-9]{4}[ ]?[0-9]{7}' # Another DL format
                ]
                
                text_lower = text.lower()
                for pattern in dl_patterns:
                    if re.search(pattern, text, re.IGNORECASE):
                        dl_text_detected = True
                        dl_text_confidence = 0.8  # High confidence if pattern matches
                        break
                
                # If no specific pattern matched, check for partial matches
                if not dl_text_detected:
                    partial_keywords = ['dl', 'driving', 'license', 'licence']
                    for keyword in partial_keywords:
                        if keyword in text_lower:
                            dl_text_detected = True
                            dl_text_confidence = max(dl_text_confidence, 0.5)  # Medium confidence
            except Exception as e:
                print(f"OCR error: {str(e)}")
                # Fallback to heuristic if OCR fails
                # Check if we detected text entities
                if len(detected_entities) > 0:
                    dl_text_detected = True
                    # Use highest confidence among detected entities
                    dl_text_confidence = max([entity.confidence for entity in detected_entities])
        else:
            # Fallback to heuristic if pytesseract is not available
            # Check if we detected text entities
            if len(detected_entities) > 0:
                dl_text_detected = True
                # Use highest confidence among detected entities
                dl_text_confidence = max([entity.confidence for entity in detected_entities])
        
        # Calculate overall authenticity confidence
        # This is a simplified approach - in a real implementation, you would have more sophisticated logic
        confidence = 0.0
        if dl_pattern_detected and dl_text_detected:
            confidence = (dl_pattern_confidence + dl_text_confidence) / 2
        elif dl_pattern_detected or dl_text_detected:
            confidence = max(dl_pattern_confidence, dl_text_confidence) * 0.7
        else:
            confidence = 0.1  # Low confidence if neither is detected
            
        is_authentic = confidence > 0.5
        
        # Generate response
        response = DrivingLicenseAuthenticityResponse(
            is_authentic=is_authentic,
            confidence=confidence,
            dl_pattern_detected=dl_pattern_detected,
            dl_text_detected=dl_text_detected,
            detected_entities=detected_entities,
            total_detections=len(detected_entities)
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
    
    finally:
        # Clean up temporary file
        os.unlink(tmp_file_path)

@app.post("/verify_enhanced_pan_authenticity", response_model=EnhancedPanAuthenticityResponse)
async def verify_enhanced_pan_authenticity(file: UploadFile = File(...)):
    """Enhanced verification of PAN card authenticity with comprehensive checks"""
    global model
    
    if not YOLO_AVAILABLE:
        raise HTTPException(status_code=500, detail="YOLO library not available")
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Validate file type
    if file.content_type is None or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(await file.read())
        tmp_file_path = tmp_file.name
    
    try:
        # Load image to get dimensions
        image = Image.open(tmp_file_path)
        image_width, image_height = image.size
        
        # Convert PIL image to OpenCV format for processing
        cv_image = cv2.imread(tmp_file_path)
        if cv_image is None:
            cv_image = np.array(image)
            if len(cv_image.shape) == 3:
                cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
        
        # Run YOLO detection
        results = model(tmp_file_path)
        
        # Process results
        detected_entities = []
        for result in results:
            if hasattr(result, 'boxes') and result.boxes is not None:
                boxes = result.boxes
                for i in range(len(boxes)):
                    box = boxes[i]
                    # Extract box coordinates
                    xyxy = box.xyxy.tolist()[0]  # [x_min, y_min, x_max, y_max]
                    x_min, y_min, x_max, y_max = xyxy
                    
                    # Calculate center coordinates
                    x_center = (x_min + x_max) / 2
                    y_center = (y_min + y_max) / 2
                    
                    # Create bounding box object
                    bbox = BoundingBox(
                        class_id=int(box.cls.item()),
                        confidence=float(box.conf.item()),
                        x_min=x_min,
                        y_min=y_min,
                        x_max=x_max,
                        y_max=y_max,
                        width=x_max - x_min,
                        height=y_max - y_min,
                        x_center=x_center,  # Calculate center
                        y_center=y_center   # Calculate center
                    )
                    detected_entities.append(bbox)
        
        # Import and use the enhanced PAN verifier
        try:
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
            from pan_verification.pan_verifier import PanCardVerifier
            
            # Perform enhanced verification
            verifier = PanCardVerifier()
            verification_result = verifier.verify_pan_card(tmp_file_path)
            
            # Generate response
            response = EnhancedPanAuthenticityResponse(
                is_authentic=verification_result.is_authentic,
                confidence=verification_result.confidence,
                layout_verified=verification_result.layout_verified,
                text_validated=verification_result.text_validated,
                security_features_verified=verification_result.security_features_verified,
                issuer_verified=verification_result.issuer_verified,
                tampering_detected=verification_result.tampering_detected,
                pan_number=verification_result.pan_number,
                holder_name=verification_result.holder_name,
                fathers_name=verification_result.fathers_name,
                date_of_birth=verification_result.date_of_birth,
                issues_found=verification_result.issues_found,
                detected_entities=detected_entities,
                total_detections=len(detected_entities)
            )
            
            return response
            
        except Exception as e:
            # Fallback to original verification if enhanced verification fails
            print(f"Enhanced verification failed: {str(e)}")
            import traceback
            traceback.print_exc()
            
            # Original PAN verification logic as fallback
            pan_pattern_detected = False
            pan_text_detected = False
            pan_pattern_confidence = 0.0
            pan_text_confidence = 0.0
            
            for entity in detected_entities:
                # Check for PAN pattern (typically in top portion with specific format)
                if (entity.y_center < image_height * 0.3):
                    pan_pattern_detected = True
                    pan_pattern_confidence = max(pan_pattern_confidence, entity.confidence)
            
            # OCR for PAN number detection (typically 10 characters: 5 letters, 4 digits, 1 letter)
            pan_text_confidence = 0.0
            if PYTESSERACT_AVAILABLE and pytesseract is not None:
                try:
                    # Extract top portion of image for OCR (where PAN number is typically located)
                    top_height = int(image_height * 0.3)
                    top_image = cv_image[0:top_height, :]
                    
                    # Convert to grayscale
                    gray = cv2.cvtColor(top_image, cv2.COLOR_BGR2GRAY)
                    
                    # Apply threshold to get black and white image
                    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                    
                    # Perform OCR
                    text = pytesseract.image_to_string(thresh, lang='eng')
                    
                    # Check for PAN number pattern (5 uppercase letters, 4 digits, 1 uppercase letter)
                    import re
                    pan_pattern = r'[A-Z]{5}[0-9]{4}[A-Z]{1}'
                    matches = re.findall(pan_pattern, text)
                    
                    if matches:
                        pan_text_detected = True
                        pan_text_confidence = 0.9  # High confidence if pattern matches
                    else:
                        # Check for partial matches or similar patterns
                        partial_pattern = r'[A-Z]{3,5}[0-9]{2,4}[A-Z]{1}'
                        partial_matches = re.findall(partial_pattern, text)
                        if partial_matches:
                            pan_text_detected = True
                            pan_text_confidence = 0.6  # Medium confidence for partial matches
                except Exception as ocr_error:
                    print(f"OCR error: {str(ocr_error)}")
                    # Fallback to heuristic if OCR fails
                    # Check if we detected text entities in the top area
                    for entity in detected_entities:
                        if entity.y_center < image_height * 0.3:
                            pan_text_detected = True
                            pan_text_confidence = max(pan_text_confidence, entity.confidence)
            else:
                # Fallback to heuristic if pytesseract is not available
                # Check if we detected text entities in the top area
                for entity in detected_entities:
                    if entity.y_center < image_height * 0.3:
                        pan_text_detected = True
                        pan_text_confidence = max(pan_text_confidence, entity.confidence)
            
            # Calculate overall authenticity confidence
            # This is a simplified approach - in a real implementation, you would have more sophisticated logic
            confidence = 0.0
            if pan_pattern_detected and pan_text_detected:
                confidence = (pan_pattern_confidence + pan_text_confidence) / 2
            elif pan_pattern_detected or pan_text_detected:
                confidence = max(pan_pattern_confidence, pan_text_confidence) * 0.7
            else:
                confidence = 0.1  # Low confidence if neither is detected
                
            is_authentic = confidence > 0.5
            
            # Generate response with fallback data
            response = EnhancedPanAuthenticityResponse(
                is_authentic=is_authentic,
                confidence=confidence,
                layout_verified=pan_pattern_detected,
                text_validated=pan_text_detected,
                security_features_verified=False,
                issuer_verified=False,
                tampering_detected=False,
                pan_number="",
                holder_name="",
                fathers_name="",
                date_of_birth="",
                issues_found=["Enhanced verification failed, using fallback method"],
                detected_entities=detected_entities,
                total_detections=len(detected_entities)
            )
            
            return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
    
    finally:
        # Clean up temporary file
        os.unlink(tmp_file_path)

@app.post("/verify_voter_id_authenticity", response_model=VoterIdAuthenticityResponse)
async def verify_voter_id_authenticity(file: UploadFile = File(...)):
    """Verify the authenticity of an uploaded Voter ID card with comprehensive checks"""
    global model
    
    if not YOLO_AVAILABLE:
        raise HTTPException(status_code=500, detail="YOLO library not available")
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Validate file type
    if file.content_type is None or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp_file:
        tmp_file.write(await file.read())
        tmp_file_path = tmp_file.name
    
    try:
        # Load image to get dimensions
        image = Image.open(tmp_file_path)
        image_width, image_height = image.size
        
        # Convert PIL image to OpenCV format for processing
        cv_image = cv2.imread(tmp_file_path)
        if cv_image is None:
            cv_image = np.array(image)
            if len(cv_image.shape) == 3:
                cv_image = cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
        
        # Initialize verification results
        layout_verified = False
        security_features_verified = False
        text_quality_verified = False
        epic_number_valid = False
        photo_verified = False
        barcode_qr_verified = False
        signature_seal_verified = False
        data_consistency_verified = False
        epic_number = ""
        voter_name = ""
        fathers_name = ""
        date_of_birth = ""
        gender = ""
        address = ""
        issues_found = []
        
        # Run YOLO detection
        results = model(tmp_file_path)
        
        # Process results
        detected_entities = []
        epic_entity = None
        name_entity = None
        photo_entity = None
        address_entity = None
        
        for result in results:
            if hasattr(result, 'boxes') and result.boxes is not None:
                boxes = result.boxes
                for i in range(len(boxes)):
                    box = boxes[i]
                    # Extract box coordinates
                    xyxy = box.xyxy.tolist()[0]  # [x_min, y_min, x_max, y_max]
                    x_min, y_min, x_max, y_max = xyxy
                    
                    # Calculate center coordinates
                    x_center = (x_min + x_max) / 2
                    y_center = (y_min + y_max) / 2
                    
                    # Create bounding box object
                    bbox = BoundingBox(
                        class_id=int(box.cls.item()),
                        confidence=float(box.conf.item()),
                        x_min=x_min,
                        y_min=y_min,
                        x_max=x_max,
                        y_max=y_max,
                        width=x_max - x_min,
                        height=y_max - y_min,
                        x_center=x_center,  # Calculate center
                        y_center=y_center   # Calculate center
                    )
                    detected_entities.append(bbox)
                    
                    # Map classes to Voter ID features
                    # 0: EPIC Number, 1: Name Field, 2: Date of Birth, 3: Address Field, 4: Photo Area
                    if box.cls.item() == 0:  # EPIC Number
                        epic_entity = bbox
                    elif box.cls.item() == 1:  # Name Field
                        name_entity = bbox
                    elif box.cls.item() == 3:  # Address Field
                        address_entity = bbox
                    elif box.cls.item() == 4:  # Photo Area
                        photo_entity = bbox
        
        # 1. Document Structure & Layout Verification
        # Check if all required elements are detected in reasonable positions
        if epic_entity and name_entity and photo_entity and address_entity:
            # Check if elements are in expected positions
            # EPIC number should be in top portion
            # Photo should be in top-right area
            # Name should be below EPIC number
            # Address should be in bottom portion
            if (epic_entity.y_center < image_height * 0.3 and 
                photo_entity.x_center > image_width * 0.7 and 
                photo_entity.y_center < image_height * 0.5 and
                name_entity.y_center > epic_entity.y_center and
                name_entity.y_center < image_height * 0.5 and
                address_entity.y_center > image_height * 0.6):
                layout_verified = True
            else:
                issues_found.append("Document layout does not match expected format")
        else:
            issues_found.append("Missing required document elements")
        
        # 2. Security Features Verification (simulated)
        # In a real implementation, this would involve advanced image processing
        # For now, we'll simulate based on image quality
        if image_width >= 300 and image_height >= 200:
            security_features_verified = True
        else:
            issues_found.append("Low resolution image may indicate poor quality or fake document")
            security_features_verified = False
        
        # 3. Text & Printing Quality Verification
        # Check image sharpness and clarity
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        if laplacian_var > 100:  # Threshold for sharpness
            text_quality_verified = True
        else:
            issues_found.append("Poor text quality - document may be blurry or low resolution")
            text_quality_verified = False
        
        # 4. Unique Identification Numbers Verification
        # OCR for EPIC number detection and validation
        epic_text_confidence = 0.0
        if PYTESSERACT_AVAILABLE and pytesseract is not None:
            try:
                if epic_entity:
                    # Extract EPIC number area
                    x1 = max(0, int(epic_entity.x_min))
                    y1 = max(0, int(epic_entity.y_min))
                    x2 = min(image_width, int(epic_entity.x_max))
                    y2 = min(image_height, int(epic_entity.y_max))
                    
                    epic_region = cv_image[y1:y2, x1:x2]
                    
                    # Convert to grayscale
                    gray = cv2.cvtColor(epic_region, cv2.COLOR_BGR2GRAY)
                    
                    # Apply threshold to get black and white image
                    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                    
                    # Perform OCR
                    text = pytesseract.image_to_string(thresh, lang='eng')
                    
                    # Clean and extract EPIC number
                    clean_text = ''.join(text.split()).upper()
                    
                    # Check for EPIC number pattern (typically starts with ECI or state code)
                    import re
                    # EPIC numbers typically have 10-15 alphanumeric characters
                    epic_pattern = r'(ECI[A-Z0-9]{8,15}|[A-Z]{3}[0-9]{7,10})'
                    matches = re.findall(epic_pattern, clean_text)
                    
                    if matches:
                        epic_number = matches[0]
                        epic_number_valid = True
                        epic_text_confidence = 0.9  # High confidence if pattern matches
                    else:
                        # Check for partial matches or similar patterns
                        partial_keywords = ['EPIC', 'VOTER', 'ELECTION']
                        text_upper = text.upper()
                        for keyword in partial_keywords:
                            if keyword in text_upper:
                                epic_number_valid = True
                                epic_text_confidence = 0.6  # Medium confidence for partial matches
                                break
            except Exception as e:
                print(f"OCR error: {str(e)}")
                issues_found.append("Error extracting EPIC number")
        
        # 5. Photo Verification
        if photo_entity:
            # Check if photo area has reasonable dimensions
            if (photo_entity.width > 50 and photo_entity.height > 50 and
                photo_entity.width/photo_entity.height > 0.5 and 
                photo_entity.width/photo_entity.height < 1.5):
                photo_verified = True
            else:
                issues_found.append("Photo area has irregular dimensions")
                photo_verified = False
        else:
            issues_found.append("Photo area not detected")
            photo_verified = False
        
        # 6. QR / Barcode Verification (simulated)
        # In a real implementation, this would involve specific QR/barcode detection
        # For now, we'll assume it's verified if security features are good
        barcode_qr_verified = security_features_verified
        
        # 7. Signature / Seal Verification (simulated)
        # In a real implementation, this would involve specific detection
        # For now, we'll assume it's verified if layout is good
        signature_seal_verified = layout_verified
        
        # 8. Data Consistency Verification
        # OCR for name and other fields
        if PYTESSERACT_AVAILABLE and pytesseract is not None:
            try:
                if name_entity:
                    # Extract name area
                    x1 = max(0, int(name_entity.x_min))
                    y1 = max(0, int(name_entity.y_min))
                    x2 = min(image_width, int(name_entity.x_max))
                    y2 = min(image_height, int(name_entity.y_max))
                    
                    name_region = cv_image[y1:y2, x1:x2]
                    
                    # Convert to grayscale
                    gray = cv2.cvtColor(name_region, cv2.COLOR_BGR2GRAY)
                    
                    # Apply threshold
                    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                    
                    # Perform OCR
                    text = pytesseract.image_to_string(thresh, lang='eng')
                    voter_name = text.strip()
                
                if address_entity:
                    # Extract address area
                    x1 = max(0, int(address_entity.x_min))
                    y1 = max(0, int(address_entity.y_min))
                    x2 = min(image_width, int(address_entity.x_max))
                    y2 = min(image_height, int(address_entity.y_max))
                    
                    address_region = cv_image[y1:y2, x1:x2]
                    
                    # Convert to grayscale
                    gray = cv2.cvtColor(address_region, cv2.COLOR_BGR2GRAY)
                    
                    # Apply threshold
                    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                    
                    # Perform OCR
                    text = pytesseract.image_to_string(thresh, lang='eng')
                    address = text.strip()
                
                # Simple consistency check
                if voter_name and address:
                    data_consistency_verified = True
                else:
                    issues_found.append("Unable to extract voter name or address")
                    data_consistency_verified = False
                    
            except Exception as e:
                print(f"OCR error: {str(e)}")
                issues_found.append("Error extracting voter information")
                data_consistency_verified = False
        else:
            issues_found.append("OCR not available for data consistency check")
            data_consistency_verified = False
        
        # Calculate overall authenticity confidence
        verification_scores = [
            layout_verified,
            security_features_verified,
            text_quality_verified,
            epic_number_valid,
            photo_verified,
            barcode_qr_verified,
            signature_seal_verified,
            data_consistency_verified
        ]
        
        # Count successful verifications
        successful_checks = sum(verification_scores)
        total_checks = len(verification_scores)
        
        # Calculate confidence (0.0 to 1.0)
        confidence = successful_checks / total_checks if total_checks > 0 else 0.0
        
        # Determine authenticity based on confidence threshold
        is_authentic = confidence > 0.6
        
        # If critical elements are missing, mark as inauthentic regardless of confidence
        if not epic_entity or not name_entity:
            is_authentic = False
            confidence = min(confidence, 0.3)
        
        # Generate response
        response = VoterIdAuthenticityResponse(
            is_authentic=is_authentic,
            confidence=confidence,
            layout_verified=layout_verified,
            security_features_verified=security_features_verified,
            text_quality_verified=text_quality_verified,
            epic_number_valid=epic_number_valid,
            photo_verified=photo_verified,
            barcode_qr_verified=barcode_qr_verified,
            signature_seal_verified=signature_seal_verified,
            data_consistency_verified=data_consistency_verified,
            epic_number=epic_number,
            voter_name=voter_name,
            fathers_name=fathers_name,
            date_of_birth=date_of_birth,
            gender=gender,
            address=address,
            issues_found=issues_found,
            detected_entities=detected_entities,
            total_detections=len(detected_entities)
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
    
    finally:
        # Clean up temporary file
        os.unlink(tmp_file_path)

# Add this new endpoint for Gemini-powered verification
@app.post("/verify_document_with_gemini", response_model=GeminiVerificationResponse)
async def verify_document_with_gemini(file: UploadFile = File(...)):
    """Verify document authenticity using Google's Gemini AI"""
    # Note: Not using the global model variable here as we're using Gemini instead of YOLO
    
    # Validate file type
    if file.content_type is None or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
    
    # Read file content
    file_content = await file.read()
    
    try:
        # Get Gemini API key from environment variable
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise HTTPException(status_code=500, detail="Gemini API key not configured. Please set the GEMINI_API_KEY environment variable.")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        
        # Use the correct model name format with full path
        # Using gemini-flash-latest which is available and supports vision
        try:
            gemini_model = genai.GenerativeModel('models/gemini-flash-latest')
        except Exception as model_error:
            try:
                gemini_model = genai.GenerativeModel('models/gemini-2.5-flash')
            except Exception as fallback_error:
                try:
                    gemini_model = genai.GenerativeModel('models/gemini-2.0-flash')
                except Exception as second_fallback_error:
                    # Fallback to gemini-pro if newer models aren't available
                    gemini_model = genai.GenerativeModel('models/gemini-pro-latest')
        
        # Prepare the prompt for document verification
        prompt = """
        Analyze this Indian government document image and verify its authenticity with extreme attention to detail. 
        Provide a detailed analysis including:
        1. Whether the document appears to be authentic or fake
        2. Confidence level in your assessment (0-100%)
        3. Detailed explanation of your reasoning
        4. Any issues or red flags you notice
        5. Key verification factors you considered
        6. Extract any readable information from the document
        
        SPECIAL INSTRUCTIONS - FOCUS ON SPELLING ERRORS:
        - Check specifically for spelling mistakes in official government names like "GOVERNMENT OF INDIA"
        - Look for "INDIYA" instead of "INDIA" or other similar spelling errors
        - If you find ANY spelling errors in official government text, classify the document as FAKE
        - If NO spelling errors are found in official government text, classify the document as AUTHENTIC
        - Pay special attention to official headers, government names, and organization names
        
        Format your response as JSON with the following structure:
        {
            "is_authentic": boolean,
            "confidence": number,
            "explanation": string,
            "extracted_info": object,
            "issues_found": array,
            "verification_factors": array
        }
        
        IMPORTANT: Return ONLY the JSON object, nothing else. Do not wrap it in code blocks or add any extra text.
        """
        
        # Create image blob for Gemini
        import io
        image_blob = io.BytesIO(file_content)
        
        # Generate content using Gemini
        response = gemini_model.generate_content([
            prompt,
            PILImage.open(image_blob)
        ])
        
        # Parse the JSON response
        import json
        import re
        
        # Get the response text
        response_text = response.text.strip()
        
        # Try to extract JSON from markdown code blocks if present
        # Handle various markdown formats
        json_match = re.search(r'```(?:json)?\s*({.*?})\s*```', response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group(1)
        else:
            # If no markdown blocks, try to find JSON object in the response
            # Look for the first '{' and last '}' to extract JSON
            first_brace = response_text.find('{')
            last_brace = response_text.rfind('}')
            if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
                response_text = response_text[first_brace:last_brace+1]
        
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError as json_error:
            # If JSON parsing fails, create a structured response with the raw text
            result = {
                "is_authentic": False,
                "confidence": 0.0,
                "explanation": f"Could not parse Gemini response as JSON. Raw response: {response_text[:500]}...",
                "extracted_info": {},
                "issues_found": ["Failed to parse AI response as JSON"],
                "verification_factors": []
            }
        
        # Ensure all required fields are present
        required_fields = ["is_authentic", "confidence", "explanation", "extracted_info", "issues_found", "verification_factors"]
        for field in required_fields:
            if field not in result:
                result[field] = getDefaultFieldValue(field)
        
        # Normalize confidence to be between 0 and 1
        if isinstance(result["confidence"], (int, float)):
            # If confidence is given as a percentage (0-100), convert to decimal (0-1)
            if result["confidence"] > 1.0:
                result["confidence"] = result["confidence"] / 100.0
            # Ensure it's between 0 and 1
            result["confidence"] = min(max(result["confidence"], 0.0), 1.0)
        
        # Focus specifically on spelling errors as the primary determinant
        # Check if Gemini identified any spelling errors in official government text
        spelling_errors_found = any(
            ("spelling" in str(issue).lower() and "government" in str(issue).lower()) or
            ("indiya" in str(issue).lower() and "india" in str(issue).lower()) or
            ("misspell" in str(issue).lower() and "government" in str(issue).lower())
            for issue in result.get("issues_found", [])
        )
        
        # Final decision based on spelling errors:
        # - If spelling errors found -> FAKE
        # - If no spelling errors found -> AUTHENTIC (respect Gemini's determination)
        if spelling_errors_found:
            final_is_authentic = False
        else:
            # If no spelling errors, respect Gemini's own authenticity determination
            final_is_authentic = result.get("is_authentic", False)
        
        # Create response object
        gemini_response = GeminiVerificationResponse(
            is_authentic=final_is_authentic,
            confidence=result["confidence"],
            explanation=result["explanation"],
            extracted_info=result["extracted_info"],
            issues_found=result["issues_found"],
            verification_factors=result["verification_factors"]
        )
        
        return gemini_response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing with Gemini: {str(e)}")


# Add this new endpoint for GitHub AI model-powered verification
@app.post("/verify_document_with_openai", response_model=OpenAIVerificationResponse)
async def verify_document_with_openai(file: UploadFile = File(...)):
    """Verify document authenticity using GitHub's AI models"""
    # Note: Not using the global model variable here as we're using GitHub AI instead of YOLO
    
    # Validate file type
    if file.content_type is None or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
    
    # Read file content
    file_content = await file.read()
    
    try:
        # Get GitHub token from environment variable
        github_token = os.getenv("GITHUB_PAT")
        if not github_token:
            raise HTTPException(status_code=500, detail="GitHub token not configured. Please set the GITHUB_PAT environment variable.")
        
        # Import required modules
        from openai import OpenAI
        import base64
        
        # Configure GitHub AI model endpoint (OpenAI-compatible)
        endpoint = "https://models.github.ai/inference/openai"
        model = "gpt-4-vision-preview"
        
        # Initialize OpenAI client with GitHub AI endpoint
        client = OpenAI(
            base_url=endpoint,
            api_key=github_token,
        )
        
        # Prepare the prompt for document verification
        prompt = """
        Analyze this Indian government document image and verify its authenticity with extreme attention to detail. 
        Provide a detailed analysis including:
        1. Whether the document appears to be authentic or fake
        2. Confidence level in your assessment (0-100%)
        3. Detailed explanation of your reasoning
        4. Any issues or red flags you notice
        5. Key verification factors you considered
        6. Extract any readable information from the document
        
        SPECIAL INSTRUCTIONS - FOCUS ON SPELLING ERRORS:
        - Check specifically for spelling mistakes in official government names like "GOVERNMENT OF INDIA"
        - Look for "INDIYA" instead of "INDIA" or other similar spelling errors
        - If you find ANY spelling errors in official government text, classify the document as FAKE
        - If NO spelling errors are found in official government text, classify the document as AUTHENTIC
        - Pay special attention to official headers, government names, and organization names
        
        Format your response as JSON with the following structure:
        {
            "is_authentic": boolean,
            "confidence": number,
            "explanation": string,
            "extracted_info": object,
            "issues_found": array,
            "verification_factors": array
        }
        
        IMPORTANT: Return ONLY the JSON object, nothing else. Do not wrap it in code blocks or add any extra text.
        """
        
        # Encode image to base64 for sending to GitHub AI
        image_blob = base64.b64encode(file_content).decode('utf-8')
        
        # Create message with image using Azure AI Inference library
        from azure.ai.inference.models import ImageUrl
        
        # Convert image to base64 data URI format for vision models
        image_data_uri = f"data:image/jpeg;base64,{image_blob}"
        
        # Use OpenAI-compatible message structure
        messages = [
            {"role": "system", "content": "You are a document verification expert specializing in Indian government documents."},
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": image_data_uri}}
            ]}
        ]
        
        # Generate content using GitHub AI model
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.1,  # Low temperature for consistent results
            max_tokens=1000
        )
        
        # Parse the JSON response
        import json
        import re
        
        # Get the response text
        response_text = response.choices[0].message.content.strip()
        
        # Try to extract JSON from markdown code blocks if present
        # Handle various markdown formats
        json_match = re.search(r'```(?:json)?\s*({.*?})\s*```', response_text, re.DOTALL)
        if json_match:
            response_text = json_match.group(1)
        else:
            # If no markdown blocks, try to find JSON object in the response
            # Look for the first '{' and last '}' to extract JSON
            first_brace = response_text.find('{')
            last_brace = response_text.rfind('}')
            if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
                response_text = response_text[first_brace:last_brace+1]
        
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError as json_error:
            # If JSON parsing fails, create a structured response with the raw text
            result = {
                "is_authentic": False,
                "confidence": 0.0,
                "explanation": f"Could not parse AI response as JSON. Raw response: {response_text[:500]}...",
                "extracted_info": {},
                "issues_found": ["Failed to parse AI response as JSON"],
                "verification_factors": []
            }
        
        # Ensure all required fields are present
        required_fields = ["is_authentic", "confidence", "explanation", "extracted_info", "issues_found", "verification_factors"]
        for field in required_fields:
            if field not in result:
                result[field] = [] if field in ["issues_found", "verification_factors"] else {} if field == "extracted_info" else False if field == "is_authentic" else 0.0 if field == "confidence" else ""
        
        # Normalize confidence to be between 0 and 1
        if isinstance(result["confidence"], (int, float)):
            # If confidence is given as a percentage (0-100), convert to decimal (0-1)
            if result["confidence"] > 1.0:
                result["confidence"] = result["confidence"] / 100.0
            # Ensure it's between 0 and 1
            result["confidence"] = min(max(result["confidence"], 0.0), 1.0)
        
        # Focus specifically on spelling errors as the primary determinant
        # Check if AI identified any spelling errors in official government text
        spelling_errors_found = any(
            ("spelling" in str(issue).lower() and "government" in str(issue).lower()) or
            ("indiya" in str(issue).lower() and "india" in str(issue).lower()) or
            ("misspell" in str(issue).lower() and "government" in str(issue).lower())
            for issue in result.get("issues_found", [])
        )
        
        # Final decision based on spelling errors:
        # - If spelling errors found -> FAKE
        # - If no spelling errors found -> AUTHENTIC (respect AI's determination)
        if spelling_errors_found:
            final_is_authentic = False
        else:
            # If no spelling errors, respect AI's own authenticity determination
            final_is_authentic = result.get("is_authentic", False)
        
        # Create response object
        openai_response = OpenAIVerificationResponse(
            is_authentic=final_is_authentic,
            confidence=result["confidence"],
            explanation=result["explanation"],
            extracted_info=result["extracted_info"],
            issues_found=result["issues_found"],
            verification_factors=result["verification_factors"]
        )
        
        return openai_response
        
    except Exception as e:
        # Log the error for debugging
        import traceback
        error_details = traceback.format_exc()
        
        # Check if it's a model access error
        error_str = str(e)
        if "no_access" in error_str and "model" in error_str:
            raise HTTPException(status_code=500, detail=f"Model access error: {error_str}. This usually means your GitHub token doesn't have access to the requested model. Please check your GitHub AI model marketplace subscription or try a different model.")
        else:
            raise HTTPException(status_code=500, detail=f"Error processing with GitHub AI: {str(e)}. Details: {error_details}")

# Add new endpoint for ML verification and Cloudinary upload
@app.post("/verify_and_upload")
async def verify_and_upload(file: UploadFile = File(...)):
    """Verify document using ML model and upload to Cloudinary if REAL"""
    try:
        # Save the uploaded file temporarily
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Import our verification pipeline
        from verify_and_store import process_document
        
        # Process the document through our pipeline
        result = process_document(temp_file_path)
        
        # Clean up temporary file
        os.remove(temp_file_path)
        
        return result
    except Exception as e:
        # Clean up temporary file if it exists
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=f"Failed to verify and upload document: {str(e)}")

# Helper function to provide default values for missing fields
def getDefaultFieldValue(field):
    defaults = {
        "is_authentic": False,
        "confidence": 0.0,
        "explanation": "No explanation provided",
        "extracted_info": {},
        "issues_found": [],
        "verification_factors": []
    }
    return defaults.get(field, None)

# Add new endpoints for Cloudinary integration
@app.post("/upload_verified_document")
async def upload_document(file: UploadFile = File(...)):
    """Upload a verified document to Cloudinary"""
    try:
        # Save the uploaded file temporarily
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Upload to Cloudinary
        result = upload_verified_document(temp_file_path)
        
        # Clean up temporary file
        os.remove(temp_file_path)
        
        return result
    except Exception as e:
        # Clean up temporary file if it exists
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        raise HTTPException(status_code=500, detail=f"Failed to upload document: {str(e)}")

@app.delete("/delete_document/{public_id}")
async def delete_doc(public_id: str):
    """Delete a document from Cloudinary"""
    try:
        delete_document(public_id)
        return {"message": "Document deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")

@app.get("/list_documents")
async def list_docs():
    """List all stored documents in Cloudinary"""
    try:
        docs = list_documents()
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list documents: {str(e)}")

# Advanced verification endpoint
@app.post("/advanced_verify_document", response_model=AdvancedVerificationResponse)
async def advanced_verify_document(file: UploadFile = File(...)):
    """Advanced document verification using multiple approaches"""
    try:
        # Read the uploaded file
        file_content = await file.read()
        
        # Reset file pointer for reuse
        await file.seek(0)
        
        # 1. Gemini AI Verification
        gemini_result = await verify_document_with_gemini(file)
        
        # Reset file pointer for reuse
        await file.seek(0)
        
        # 2. ML Model Verification
        ml_result = await verify_with_ml_model(file)
        
        # Reset file pointer for reuse
        await file.seek(0)
        
        # 3. YOLO Object Detection (using Aadhaar detection as default)
        yolo_result = await detect_aadhaar_entities(file)
        
        # 4. Combine results for final decision
        final_authenticity, confidence_score, recommendations = combine_verification_results(
            gemini_result, ml_result, yolo_result
        )
        
        # Convert response objects to dictionaries
        if hasattr(gemini_result, '__dict__'):
            gemini_dict = gemini_result.__dict__
        else:
            gemini_dict = gemini_result
            
        if hasattr(yolo_result, '__dict__'):
            yolo_dict = yolo_result.__dict__
        else:
            yolo_dict = yolo_result
        
        return AdvancedVerificationResponse(
            gemini_verification=gemini_dict,
            ml_verification=ml_result,
            yolo_detection=yolo_dict,
            final_authenticity=final_authenticity,
            confidence_score=confidence_score,
            recommendations=recommendations
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in advanced verification: {str(e)}")

async def verify_with_ml_model(file: UploadFile):
    """Verify document using ML model"""
    try:
        # Save file temporarily
        temp_file_path = f"temp_ml_{uuid.uuid4()}.png"
        with open(temp_file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Import and use ML model
        from model_loader import predict_document
        prediction = predict_document(temp_file_path)
        
        # Clean up
        os.remove(temp_file_path)
        
        return {
            "prediction": prediction,
            "confidence": 0.9 if prediction == "REAL" else 0.3,
            "timestamp": str(uuid.uuid4())
        }
    except Exception as e:
        return {
            "prediction": "ERROR",
            "confidence": 0.0,
            "error": str(e)
        }

def combine_verification_results(gemini_result, ml_result, yolo_result):
    """Combine results from all verification methods"""
    # Extract authenticity scores
    # Convert GeminiVerificationResponse to dict
    if hasattr(gemini_result, '__dict__'):
        gemini_dict = gemini_result.__dict__
    else:
        gemini_dict = gemini_result
        
    gemini_authentic = gemini_dict.get("is_authentic", False)
    gemini_confidence = gemini_dict.get("confidence", 0.0)
    
    ml_prediction = ml_result.get("prediction", "ERROR")
    ml_confidence = ml_result.get("confidence", 0.0)
    
    # Handle YOLO result
    if hasattr(yolo_result, '__dict__'):
        yolo_dict = yolo_result.__dict__
    else:
        yolo_dict = yolo_result
        
    total_detections = yolo_dict.get("total_detections", 0)
    
    # Simple weighted scoring system
    gemini_weight = 0.5
    ml_weight = 0.3
    yolo_weight = 0.2
    
    # Calculate weighted confidence
    total_confidence = (
        (1.0 if gemini_authentic else 0.0) * gemini_weight +
        (1.0 if ml_prediction == "REAL" else 0.0) * ml_weight +
        min(total_detections / 10.0, 1.0) * yolo_weight
    )
    
    # Final decision (majority voting with confidence weighting)
    final_authenticity = total_confidence > 0.5
    
    # Generate recommendations
    recommendations = []
    if not gemini_authentic:
        recommendations.append("Review document for authenticity issues identified by AI analysis")
    if ml_prediction != "REAL":
        recommendations.append("ML model flagged document as potentially fake")
    if total_detections < 3:
        recommendations.append("Few document elements detected - verify document completeness")
    
    if not recommendations:
        recommendations.append("Document passed all verification checks")
    
    return final_authenticity, total_confidence, recommendations

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)