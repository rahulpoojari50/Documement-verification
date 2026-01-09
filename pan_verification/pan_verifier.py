"""
Comprehensive PAN Card Verification System

This module implements a complete PAN card verification system with the following features:
1. Layout & Template Verification
2. Text Extraction & Format Validation
3. Visual & Security Feature Inspection
4. Logo & Issuer Text Check
5. Tampering & Forgery Detection
"""

import cv2
import numpy as np
from PIL import Image
import pytesseract
from typing import Dict, List, Tuple, Optional
import re
from dataclasses import dataclass
from scipy import ndimage
from sklearn.feature_extraction.image import extract_patches_2d
import hashlib
from datetime import datetime
# import qrcode  # Temporarily commented out due to import issues
# from pyzbar import pyzbar  # Temporarily commented out due to import issues
import pickle
from pathlib import Path


@dataclass
class PanVerificationResult:
    """Data class to store PAN verification results"""
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
    extracted_fields: Dict[str, str]
    issues_found: List[str]


class PanCardVerifier:
    """Comprehensive PAN Card Verification System"""
    
    def __init__(self):
        """Initialize the PAN card verifier"""
        self.pan_pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
        self.dob_patterns = [
            r'\b(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/\d{4}\b',  # DD/MM/YYYY
            r'\b\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])\b'   # YYYY-MM-DD
        ]
        self.issuer_texts = [
            "INCOME TAX DEPARTMENT",
            "GOVERNMENT OF INDIA"
        ]
        # PAN card type codes
        self.pan_type_codes = {
            'P': 'Individual',
            'C': 'Company',
            'H': 'HUF (Hindu Undivided Family)',
            'A': 'Association of Persons (AOP)',
            'T': 'AOP (Trust)',
            'F': 'Firm',
            'L': 'Local Authority',
            'J': 'Artificial Juridical Person',
            'G': 'Government'
        }
        
        # Try to load the trained classifier
        self.authenticity_classifier = None
        try:
            classifier_path = Path("models/pan_authenticity_classifier.pkl")
            if classifier_path.exists():
                with open(classifier_path, 'rb') as f:
                    self.authenticity_classifier = pickle.load(f)
        except Exception as e:
            print(f"Warning: Could not load PAN authenticity classifier: {e}")
    
    def verify_pan_card(self, image_path: str) -> PanVerificationResult:
        """
        Perform comprehensive verification of a PAN card
        
        Args:
            image_path: Path to the PAN card image
            
        Returns:
            PanVerificationResult: Verification results
        """
        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError("Could not load image")
        
        # Convert to PIL Image for some operations
        pil_image = Image.open(image_path)
        
        # Initialize result object
        result = PanVerificationResult(
            is_authentic=False,
            confidence=0.0,
            layout_verified=False,
            text_validated=False,
            security_features_verified=False,
            issuer_verified=False,
            tampering_detected=False,
            pan_number="",
            holder_name="",
            fathers_name="",
            date_of_birth="",
            extracted_fields={},
            issues_found=[]
        )
        
        # Use the trained classifier as the primary method for authenticity determination
        classifier_confidence = 0.0
        classifier_prediction = 0  # 0 = fake, 1 = real
        
        if self.authenticity_classifier is not None:
            try:
                # Extract features for classification
                features = self._extract_simple_features(image_path)
                if features is not None:
                    features = features.reshape(1, -1)
                    classifier_prediction = self.authenticity_classifier.predict(features)[0]
                    classifier_probability = self.authenticity_classifier.predict_proba(features)[0]
                    
                    # Use classifier result as primary confidence
                    classifier_confidence = float(max(classifier_probability))
                    result.confidence = classifier_confidence
                    
                    # Set authenticity based on classifier prediction
                    # If classifier predicts real (1) with high confidence, mark as authentic
                    # If classifier predicts fake (0) with high confidence, mark as inauthentic
                    if classifier_prediction == 1:
                        result.is_authentic = True
                    else:
                        result.is_authentic = False
                        result.issues_found.append("Classifier indicates this is likely a fake PAN card")
                        
                    # Early return if classifier is confident
                    if classifier_confidence > 0.6:
                        return result
            except Exception as e:
                print(f"Classifier error: {e}")
        
        # Fallback to rule-based verification if classifier fails or is not confident enough
        # Extract and validate text
        text_results = self._extract_and_validate_text(image)
        result.text_validated = text_results['valid']
        result.pan_number = text_results.get('pan_number', '')
        result.holder_name = text_results.get('holder_name', '')
        result.fathers_name = text_results.get('fathers_name', '')
        result.date_of_birth = text_results.get('date_of_birth', '')
        result.extracted_fields = text_results.get('fields', {})
        
        if not result.text_validated:
            result.issues_found.extend(text_results.get('issues', []))
        
        # Verify layout
        layout_results = self._verify_layout(image, pil_image)
        result.layout_verified = layout_results['verified']
        if not result.layout_verified:
            result.issues_found.extend(layout_results.get('issues', []))
        
        # Verify security features
        security_results = self._verify_security_features(image)
        result.security_features_verified = security_results['verified']
        if not result.security_features_verified:
            result.issues_found.extend(security_results.get('issues', []))
        
        # Verify issuer
        issuer_results = self._verify_issuer_text(image)
        result.issuer_verified = issuer_results['verified']
        if not result.issuer_verified:
            result.issues_found.extend(issuer_results.get('issues', []))
        
        # Detect tampering
        tampering_results = self._detect_tampering(image)
        result.tampering_detected = tampering_results['detected']
        if result.tampering_detected:
            result.issues_found.extend(tampering_results.get('issues', []))
        
        # Calculate overall confidence
        result.confidence = self._calculate_confidence(result)
        
        # Final authenticity decision
        # Lower the threshold for authenticity to reduce false negatives
        # Real PAN cards may fail some tests but should still be considered authentic
        # if the core elements (PAN number format, basic layout) are correct
        result.is_authentic = result.confidence >= 0.5 and not result.tampering_detected
        
        # Override with classifier result if available and more confident
        if self.authenticity_classifier is not None and classifier_confidence > 0.5:
            result.confidence = classifier_confidence
            if classifier_prediction == 1:
                result.is_authentic = True
                # Remove any issues that might have been added by rule-based verification
                # if the classifier is confident it's real
                if classifier_confidence > 0.6:
                    result.issues_found = [issue for issue in result.issues_found 
                                        if not issue.startswith("Classifier indicates")]
            else:
                result.is_authentic = False
                if "Classifier indicates this is likely a fake PAN card" not in result.issues_found:
                    result.issues_found.append("Classifier indicates this is likely a fake PAN card")
        
        return result
    
    def _extract_and_validate_text(self, image: np.ndarray) -> Dict:
        """
        Extract and validate text from PAN card
        
        Args:
            image: OpenCV image array
            
        Returns:
            Dict with text extraction results
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply multiple preprocessing techniques to improve OCR
        # 1. Normal threshold
        _, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # 2. Adaptive threshold
        thresh2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        # 3. Bilateral filter to reduce noise while keeping edges sharp
        filtered = cv2.bilateralFilter(gray, 9, 75, 75)
        _, thresh3 = cv2.threshold(filtered, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Try OCR on all versions
        texts = []
        for img in [gray, thresh1, thresh2, thresh3]:
            try:
                text = pytesseract.image_to_string(img)
                texts.append(text)
            except:
                pass
        
        # Combine all OCR results
        combined_text = " ".join(texts)
        
        # Extract fields
        fields = {}
        pan_number = ""
        holder_name = ""
        fathers_name = ""
        date_of_birth = ""
        issues = []
        
        # Extract PAN number
        pan_matches = re.findall(self.pan_pattern, combined_text)
        if pan_matches:
            pan_number = pan_matches[0]
        else:
            issues.append("PAN number not found or invalid format")
        
        # Validate PAN format
        if pan_number:
            format_validation = self._validate_pan_format(pan_number, holder_name)
            if not format_validation['valid']:
                issues.extend(format_validation['issues'])
        
        # Extract other fields (simplified)
        # In a real implementation, this would be more sophisticated
        if "Name" in combined_text:
            # Simple extraction - in practice this would be more robust
            name_match = re.search(r"Name\s*:\s*([A-Z\s]+)", combined_text)
            if name_match:
                holder_name = name_match.group(1).strip()
        
        if "Father" in combined_text or "Father's" in combined_text:
            father_match = re.search(r"(?:Father|Father's) Name\s*:\s*([A-Z\s]+)", combined_text)
            if father_match:
                fathers_name = father_match.group(1).strip()
        
        # Extract date of birth
        for pattern in self.dob_patterns:
            dob_matches = re.findall(pattern, combined_text)
            if dob_matches:
                date_of_birth = dob_matches[0]
                break
        
        # Determine validity
        valid = len(pan_number) > 0  # Simplified validation
        
        return {
            'valid': valid,
            'pan_number': pan_number,
            'holder_name': holder_name,
            'fathers_name': fathers_name,
            'date_of_birth': date_of_birth,
            'fields': fields,
            'issues': issues
        }
    
    def _validate_pan_format(self, pan_number: str, holder_name: str) -> Dict:
        """
        Validate PAN number format according to specific requirements
        """
        issues = []
        valid = True
        
        # 1. PAN number format must match the pattern AAAAA9999A
        if not re.match(self.pan_pattern, pan_number):
            issues.append("PAN number format does not match AAAAA9999A pattern")
            valid = False
            return {'valid': valid, 'issues': issues}
        
        # 2. Validate the meaning of the 4th character (P/C/H/A/T/F etc.)
        fourth_char = pan_number[3]
        if fourth_char not in self.pan_type_codes:
            issues.append(f"Invalid PAN type code '{fourth_char}' at position 4")
            valid = False
        
        # 3. The 5th character must match the first letter of the surname
        fifth_char = pan_number[4]
        if holder_name:
            # Extract surname (last word in name)
            name_parts = holder_name.strip().split()
            if name_parts:
                surname_first_letter = name_parts[-1][0].upper() if name_parts[-1] else ''
                if fifth_char != surname_first_letter:
                    issues.append(f"5th character '{fifth_char}' does not match first letter of surname '{surname_first_letter}'")
                    valid = False
        else:
            issues.append("Holder name not found for surname validation")
            valid = False
        
        return {'valid': valid, 'issues': issues}
    
    def _verify_layout(self, image: np.ndarray, pil_image: Image.Image) -> Dict:
        """
        Verify PAN card layout and template
        
        Args:
            image: OpenCV image array
            pil_image: PIL Image object
            
        Returns:
            Dict with verification results
        """
        height, width = image.shape[:2]
        aspect_ratio = width / height
        
        # Check basic dimensions (PAN cards are typically 3:2 ratio)
        expected_ratio = 1.5  # 3:2 ratio
        # Increase tolerance for real scanned PAN cards
        ratio_tolerance = 0.35
        
        # Basic aspect ratio check
        ratio_check = abs(aspect_ratio - expected_ratio) <= ratio_tolerance
        
        # Check for photo area (typically in top-right)
        photo_area_verified = self._verify_photo_area(image)
        
        # Check for signature area (typically in bottom-right)
        signature_area_verified = self._verify_signature_area(image)
        
        verified = ratio_check and photo_area_verified and signature_area_verified
        
        issues = []
        if not ratio_check:
            issues.append(f"Aspect ratio {aspect_ratio:.2f} doesn't match expected {expected_ratio}")
        if not photo_area_verified:
            issues.append("Photo area not detected")
        if not signature_area_verified:
            issues.append("Signature area not detected")
        
        return {
            'verified': verified,
            'issues': issues
        }
    
    def _verify_photo_area(self, image: np.ndarray) -> bool:
        """
        Verify the presence and position of photo area
        
        Args:
            image: OpenCV image array
            
        Returns:
            bool: True if photo area is verified
        """
        height, width = image.shape[:2]
        
        # Define region where photo is expected (top-right)
        photo_region = image[int(height * 0.1):int(height * 0.5), 
                            int(width * 0.7):int(width * 0.95)]
        
        # Convert to grayscale
        gray = cv2.cvtColor(photo_region, cv2.COLOR_BGR2GRAY)
        
        # Calculate variance of Laplacian to detect blur
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # Photo area should have sufficient detail (not blurred)
        # Lower the threshold for real scanned images
        return laplacian_var > 30
    
    def _verify_signature_area(self, image: np.ndarray) -> bool:
        """
        Verify the presence and position of signature area
        
        Args:
            image: OpenCV image array
            
        Returns:
            bool: True if signature area is verified
        """
        height, width = image.shape[:2]
        
        # Define region where signature is expected (bottom-right)
        signature_region = image[int(height * 0.7):int(height * 0.9), 
                                int(width * 0.7):int(width * 0.95)]
        
        # Convert to grayscale
        gray = cv2.cvtColor(signature_region, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold to separate signature from background
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Count non-zero pixels (signature pixels)
        signature_pixels = cv2.countNonZero(thresh)
        total_pixels = thresh.shape[0] * thresh.shape[1]
        
        # Signature area should have a reasonable amount of content
        # Lower threshold for real scanned signatures
        signature_ratio = signature_pixels / total_pixels
        return 0.05 <= signature_ratio <= 0.7
    
    def _verify_security_features(self, image: np.ndarray) -> Dict:
        """
        Verify security features on PAN card
        
        Args:
            image: OpenCV image array
            
        Returns:
            Dict with verification results
        """
        # Convert to HSV for color analysis
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Check for blue color (typical PAN card color)
        lower_blue = np.array([90, 50, 50])
        upper_blue = np.array([130, 255, 255])
        blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
        blue_percentage = np.sum(blue_mask > 0) / (image.shape[0] * image.shape[1])
        
        # Check for hologram-like effects (simplified)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.sum(edges > 0) / (image.shape[0] * image.shape[1])
        
        # Security features are often difficult to verify in scanned images
        # So we'll be more lenient in our verification
        verified = blue_percentage > 0.1 or edge_density > 0.05
        
        issues = []
        if not verified:
            issues.append("Security features not clearly detected (may be due to scanning quality)")
        
        return {
            'verified': verified,
            'issues': issues
        }
    
    def _verify_issuer_text(self, image: np.ndarray) -> Dict:
        """
        Verify issuer text on PAN card
        
        Args:
            image: OpenCV image array
            
        Returns:
            Dict with verification results
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Extract text using OCR
        text = pytesseract.image_to_string(gray)
        
        # Check for required issuer texts
        found_issuers = []
        for issuer in self.issuer_texts:
            if issuer.lower() in text.lower():
                found_issuers.append(issuer)
        
        verified = len(found_issuers) > 0
        
        issues = []
        if not verified:
            issues.append("Required issuer text not found")
        
        return {
            'verified': verified,
            'issues': issues,
            'found_issuers': found_issuers
        }
    
    def _detect_tampering(self, image: np.ndarray) -> Dict:
        """
        Detect signs of tampering or forgery
        
        Args:
            image: OpenCV image array
            
        Returns:
            Dict with tampering detection results
        """
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # 1. Localized blur detection
        blur_detected = self._detect_blur_inconsistencies(gray)
        
        # 2. Inconsistent noise levels
        noise_inconsistent = self._detect_noise_inconsistencies(gray)
        
        # 3. Unnatural borders around photo/text
        unnatural_borders = self._detect_unnatural_borders(image)
        
        # 4. Duplicate pixel regions
        duplicates_detected = self._detect_duplicate_regions(gray)
        
        # 5. Inconsistent DPI or mixed-resampling
        dpi_inconsistent = self._detect_dpi_inconsistencies(image)
        
        # Tampering detected if any of these are true
        detected = (
            blur_detected or 
            noise_inconsistent or 
            unnatural_borders or 
            duplicates_detected or 
            dpi_inconsistent
        )
        
        issues = []
        if blur_detected:
            issues.append("Localized blur inconsistencies detected")
        if noise_inconsistent:
            issues.append("Inconsistent noise levels detected")
        if unnatural_borders:
            issues.append("Unnatural borders detected")
        if duplicates_detected:
            issues.append("Duplicate pixel regions detected")
        if dpi_inconsistent:
            issues.append("Inconsistent DPI/resampling detected")
        
        # Reduce sensitivity for real scanned documents
        # Only flag as tampered if multiple indicators are present
        detected = len(issues) >= 2
        
        return {
            'detected': detected,
            'issues': issues
        }
    
    def _detect_blur_inconsistencies(self, gray: np.ndarray) -> bool:
        """Detect localized blur inconsistencies"""
        h, w = gray.shape
        # Divide image into quadrants
        quadrants = [
            gray[0:h//2, 0:w//2],      # Top-left
            gray[0:h//2, w//2:w],      # Top-right
            gray[h//2:h, 0:w//2],      # Bottom-left
            gray[h//2:h, w//2:w]       # Bottom-right
        ]
        
        variances = []
        for quadrant in quadrants:
            if quadrant.size > 0:
                laplacian_var = cv2.Laplacian(quadrant, cv2.CV_64F).var()
                variances.append(laplacian_var)
        
        if len(variances) < 4:
            return False
            
        # Check if variances differ significantly
        mean_var = np.mean(variances)
        std_var = np.std(variances)
        
        # Less sensitive for scanned documents
        return std_var / (mean_var + 1e-6) > 0.8
    
    def _detect_noise_inconsistencies(self, gray: np.ndarray) -> bool:
        """Detect inconsistent noise levels"""
        h, w = gray.shape
        # Divide image into quadrants
        quadrants = [
            gray[0:h//2, 0:w//2],      # Top-left
            gray[0:h//2, w//2:w],      # Top-right
            gray[h//2:h, 0:w//2],      # Bottom-left
            gray[h//2:h, w//2:w]       # Bottom-right
        ]
        
        noise_levels = []
        for quadrant in quadrants:
            if quadrant.size > 0:
                # Estimate noise as standard deviation of Laplacian
                laplacian = cv2.Laplacian(quadrant, cv2.CV_64F)
                noise_level = np.std(laplacian)
                noise_levels.append(noise_level)
        
        if len(noise_levels) < 4:
            return False
            
        # Check if noise levels differ significantly
        mean_noise = np.mean(noise_levels)
        std_noise = np.std(noise_levels)
        
        # Less sensitive for scanned documents
        return std_noise / (mean_noise + 1e-6) > 0.7
    
    def _detect_unnatural_borders(self, image: np.ndarray) -> bool:
        """Detect unnatural borders around photo/text areas"""
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply edge detection
        edges = cv2.Canny(gray, 50, 150)
        
        # Look for straight horizontal/vertical lines (could indicate cutting/pasting)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=100, maxLineGap=10)
        
        if lines is None:
            return False
        
        # Count horizontal and vertical lines
        horizontal_lines = 0
        vertical_lines = 0
        
        for line in lines:
            x1, y1, x2, y2 = line[0]
            angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
            
            # Horizontal lines (within 10 degrees of horizontal)
            if abs(angle) < 10 or abs(angle - 180) < 10:
                horizontal_lines += 1
            # Vertical lines (within 10 degrees of vertical)
            elif abs(angle - 90) < 10 or abs(angle + 90) < 10:
                vertical_lines += 1
        
        # Less sensitive for naturally occurring lines in documents
        return (horizontal_lines + vertical_lines) > 20
    
    def _detect_duplicate_regions(self, gray: np.ndarray) -> bool:
        """Detect duplicate pixel regions that might indicate copy-paste"""
        h, w = gray.shape
        
        # Compare quadrants for similarity
        top_left = gray[0:h//2, 0:w//2]
        top_right = gray[0:h//2, w//2:w]
        bottom_left = gray[h//2:h, 0:w//2]
        bottom_right = gray[h//2:h, w//2:w]
        
        # Resize all quadrants to same size for comparison
        min_h = min(top_left.shape[0], top_right.shape[0], bottom_left.shape[0], bottom_right.shape[0])
        min_w = min(top_left.shape[1], top_right.shape[1], bottom_left.shape[1], bottom_right.shape[1])
        
        if min_h == 0 or min_w == 0:
            return False
            
        top_left = cv2.resize(top_left, (min_w, min_h))
        top_right = cv2.resize(top_right, (min_w, min_h))
        bottom_left = cv2.resize(bottom_left, (min_w, min_h))
        bottom_right = cv2.resize(bottom_right, (min_w, min_h))
        
        # Calculate similarities
        similarities = []
        pairs = [(top_left, top_right), (top_left, bottom_left), (top_left, bottom_right),
                 (top_right, bottom_left), (top_right, bottom_right), (bottom_left, bottom_right)]
        
        for img1, img2 in pairs:
            # Normalize images
            img1_norm = (img1 - np.mean(img1)) / (np.std(img1) + 1e-6)
            img2_norm = (img2 - np.mean(img2)) / (np.std(img2) + 1e-6)
            
            # Calculate correlation
            correlation = np.corrcoef(img1_norm.flatten(), img2_norm.flatten())[0, 1]
            similarities.append(correlation)
        
        # Check if any pair is suspiciously similar
        # Less sensitive for natural repetitions in documents
        return max(similarities) > 0.95
    
    def _detect_dpi_inconsistencies(self, image: np.ndarray) -> bool:
        """Detect inconsistent DPI or mixed resampling"""
        # Check for moire patterns that might indicate resampling
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply FFT to detect periodic patterns
        f = np.fft.fft2(gray)
        fshift = np.fft.fftshift(f)
        magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)
        
        # Look for strong peaks in frequency domain (indicative of resampling)
        # Threshold for strong peaks
        peak_threshold = np.mean(magnitude_spectrum) + 2 * np.std(magnitude_spectrum)
        strong_peaks = np.sum(magnitude_spectrum > peak_threshold)
        
        # Less sensitive for naturally occurring patterns
        return strong_peaks > (gray.shape[0] * gray.shape[1]) * 0.05
    
    def _calculate_confidence(self, result: PanVerificationResult) -> float:
        """
        Calculate overall confidence score based on verification results
        
        Args:
            result: PanVerificationResult object
            
        Returns:
            float: Confidence score between 0.0 and 1.0
        """
        # Adjusted weighted scoring system to be more lenient for real PAN cards
        weights = {
            'layout': 0.25,         # Increased weight for layout verification
            'text': 0.35,           # Increased weight for text validation (most important)
            'security': 0.15,       # Reduced weight for security features (often fail on scanned images)
            'issuer': 0.15,         # Reduced weight for issuer verification (may fail on poor quality scans)
            'tampering_penalty': -0.1  # Reduced penalty for tampering (less aggressive)
        }
        
        score = 0.0
        
        # Add scores for positive verifications
        if result.layout_verified:
            score += weights['layout']
        if result.text_validated:
            score += weights['text']
        if result.security_features_verified:
            score += weights['security']
        if result.issuer_verified:
            score += weights['issuer']
        
        # Apply penalty for tampering
        if result.tampering_detected:
            score += weights['tampering_penalty']
        
        # Ensure score is between 0 and 1
        score = max(0.0, min(1.0, score))
        
        return score
    
    def _extract_simple_features(self, image_path):
        """
        Extract simple features for PAN authenticity classification
        
        Args:
            image_path (str): Path to the PAN card image
            
        Returns:
            np.array: Feature vector or None if failed
        """
        try:
            # Load image
            image = cv2.imread(image_path)
            if image is None:
                return None
            
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Feature 1-3: Basic image statistics
            mean_intensity = np.mean(gray)
            std_intensity = np.std(gray)
            hist_entropy = -np.sum((np.histogram(gray, bins=256)[0] / gray.size) * 
                                  np.log2(np.histogram(gray, bins=256)[0] / gray.size + 1e-10))
            
            # Feature 4-5: Edge detection statistics
            edges = cv2.Canny(gray, 50, 150)
            edge_density = np.sum(edges > 0) / edges.size
            edge_mean = np.mean(edges[edges > 0]) if np.sum(edges > 0) > 0 else 0
            
            # Feature 6: Blur detection
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Feature 7: Color uniformity (convert to HSV)
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            hue_hist = cv2.calcHist([hsv], [0], None, [50], [0, 180])
            hue_uniformity = -np.sum((hue_hist / np.sum(hue_hist)) * 
                                    np.log2(hue_hist / np.sum(hue_hist) + 1e-10))
            
            # Feature 8-9: Image dimensions
            height, width = image.shape[:2]
            aspect_ratio = width / height
            
            # Feature 10: Gradient magnitude
            grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            gradient_magnitude = np.sqrt(grad_x**2 + grad_y**2)
            mean_gradient = np.mean(gradient_magnitude)
            std_gradient = np.std(gradient_magnitude)
            
            # Feature 11-12: Frequency domain features
            f = np.fft.fft2(gray)
            fshift = np.fft.fftshift(f)
            magnitude_spectrum = np.abs(fshift)
            freq_mean = np.mean(magnitude_spectrum)
            freq_std = np.std(magnitude_spectrum)
            
            # Feature 13-14: Corner detection
            corners = cv2.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.01, minDistance=10)
            corner_count = len(corners) if corners is not None else 0
            corner_density = corner_count / (width * height)
            
            # Feature 15-16: Blob detection
            params = cv2.SimpleBlobDetector_Params()
            detector = cv2.SimpleBlobDetector_create(params)
            keypoints = detector.detect(gray)
            blob_count = len(keypoints)
            avg_blob_area = np.mean([kp.size for kp in keypoints]) if keypoints else 0
            
            # Feature 17: Structuredness (ratio of structured to unstructured regions)
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            structured_pixels = np.sum(binary == 0)  # Assuming dark text on light background
            structuredness = structured_pixels / (width * height)
            
            # Feature 18: Texture features (Local Binary Pattern simplified)
            # Simple texture measure using local variance
            kernel = np.ones((5,5),np.float32)/25
            smoothed = cv2.filter2D(gray,-1,kernel)
            texture_diff = np.abs(gray.astype(np.float32) - smoothed.astype(np.float32))
            normalized_texture = np.mean(texture_diff) / 255.0
            
            # Feature 19-20: Additional geometric features
            # Contour based features
            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contour_areas = [cv2.contourArea(cnt) for cnt in contours]
            avg_contour_area = np.mean(contour_areas) if contour_areas else 0
            contour_density = sum(contour_areas) / (width * height) if contour_areas else 0
            
            # Return feature vector
            features = np.array([
                mean_intensity,
                std_intensity,
                hist_entropy,
                edge_density,
                edge_mean,
                laplacian_var,
                hue_uniformity,
                width,
                height,
                aspect_ratio,
                mean_gradient,
                std_gradient,
                freq_mean,
                freq_std,
                corner_count,
                corner_density,
                blob_count,
                avg_blob_area,
                structuredness,
                normalized_texture
            ])
            
            return features
        except Exception as e:
            print(f"Error extracting features: {e}")
            return None