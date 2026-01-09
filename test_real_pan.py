#!/usr/bin/env python3
"""
Test script to verify real PAN card detection
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from pan_verification.pan_verifier import PanCardVerifier
import glob

def test_real_pan_cards():
    """Test the PAN verification system with real PAN card images"""
    
    print("Testing PAN verification with real PAN card images")
    print("=" * 50)
    
    # Create verifier instance
    verifier = PanCardVerifier()
    
    # Look for PAN card images in the data directory
    pan_image_paths = []
    
    # Check processed original images
    processed_paths = glob.glob('data/processed/train/original/*pan*.jpg')
    pan_image_paths.extend(processed_paths)
    
    # Check raw original images
    raw_paths = glob.glob('data/raw/original_pan/*.jpg')
    pan_image_paths.extend(raw_paths)
    
    if not pan_image_paths:
        print("No PAN card images found in data directories")
        print("Please ensure PAN card images are available in:")
        print("  - data/processed/train/original/")
        print("  - data/raw/original_pan/")
        return
    
    print(f"Found {len(pan_image_paths)} PAN card images")
    
    # Test each PAN card image
    for i, image_path in enumerate(pan_image_paths[:5]):  # Test first 5 images
        print(f"\nTesting image {i+1}: {os.path.basename(image_path)}")
        print("-" * 40)
        
        try:
            # Verify the PAN card
            result = verifier.verify_pan_card(image_path)
            
            # Print results
            print(f"Overall Result: {'LIKELY REAL' if result.is_authentic else 'POSSIBLY FAKE'}")
            print(f"Confidence Level: {result.confidence:.2f}")
            print(f"Layout Verified: {result.layout_verified}")
            print(f"Text Validated: {result.text_validated}")
            print(f"Security Features Verified: {result.security_features_verified}")
            print(f"Issuer Verified: {result.issuer_verified}")
            print(f"Tampering Detected: {result.tampering_detected}")
            print(f"Extracted PAN Number: '{result.pan_number}'")
            print(f"Holder Name: '{result.holder_name}'")
            
            if result.issues_found:
                print("Issues Found:")
                for issue in result.issues_found[:3]:  # Show first 3 issues
                    print(f"  - {issue}")
                if len(result.issues_found) > 3:
                    print(f"  ... and {len(result.issues_found) - 3} more issues")
            else:
                print("No Issues Found")
                
        except Exception as e:
            print(f"Error processing image: {e}")
            import traceback
            traceback.print_exc()

def test_specific_pan_format():
    """Test specific PAN format validation rules"""
    
    print("\n\nTesting specific PAN format validation rules")
    print("=" * 50)
    
    verifier = PanCardVerifier()
    
    # Test cases
    test_cases = [
        {
            "name": "Valid Individual PAN",
            "pan": "ABCDE1234F",
            "holder_name": "John Doe Smith",
            "should_be_valid": True
        },
        {
            "name": "Valid Company PAN",
            "pan": "ABCDE1234C",
            "holder_name": "ABC Company Ltd",
            "should_be_valid": True
        },
        {
            "name": "Invalid Format",
            "pan": "ABCD1234E",
            "holder_name": "John Doe",
            "should_be_valid": False
        },
        {
            "name": "Invalid 4th Character",
            "pan": "ABCX1234D",
            "holder_name": "John Doe",
            "should_be_valid": False
        },
        {
            "name": "Surname Mismatch",
            "pan": "ABCDE1234F",
            "holder_name": "John Doe Williams",
            "should_be_valid": False
        }
    ]
    
    for test_case in test_cases:
        print(f"\nTest: {test_case['name']}")
        print(f"PAN: {test_case['pan']}")
        print(f"Holder Name: {test_case['holder_name']}")
        
        result = verifier._validate_pan_format(
            test_case['pan'], 
            test_case['holder_name']
        )
        
        print(f"Valid: {result['valid']}")
        if result['issues']:
            print(f"Issues: {result['issues']}")
        
        expected = test_case['should_be_valid']
        actual = result['valid']
        
        if expected == actual:
            print("✓ Test PASSED")
        else:
            print(f"✗ Test FAILED (Expected: {expected}, Actual: {actual})")

if __name__ == "__main__":
    test_real_pan_cards()
    test_specific_pan_format()