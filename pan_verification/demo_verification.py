#!/usr/bin/env python3
"""
Demo script to demonstrate the enhanced PAN card verification system
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pan_verification.pan_verifier import PanCardVerifier, PanVerificationResult
import re

def demo_pan_verification():
    """Demonstrate the enhanced PAN card verification system"""
    
    # Create a mock result to demonstrate the enhanced features
    print("Enhanced PAN Card Verification System Demo")
    print("=" * 50)
    
    # Create a verifier instance
    verifier = PanCardVerifier()
    
    # Show the PAN format validation rules
    print("\n1. PAN Format Validation Rules:")
    print(f"   - Pattern: {verifier.pan_pattern}")
    print("   - 4th Character Meanings:")
    for code, meaning in verifier.pan_type_codes.items():
        print(f"     {code}: {meaning}")
    
    # Test cases with different scenarios
    test_cases = [
        {
            "name": "Valid Individual PAN",
            "pan_number": "ABCPD1234E",
            "holder_name": "John Doe David",
            "expected_authentic": True,
            "description": "Valid PAN with correct surname match"
        },
        {
            "name": "Invalid Format PAN",
            "pan_number": "ABCD1234E",
            "holder_name": "John Doe",
            "expected_authentic": False,
            "description": "Incorrect format (missing one character)"
        },
        {
            "name": "Invalid 4th Character",
            "pan_number": "ABCX1234D",
            "holder_name": "John Doe",
            "expected_authentic": False,
            "description": "Invalid 4th character 'X'"
        },
        {
            "name": "Surname Mismatch",
            "pan_number": "ABCPD1234E",
            "holder_name": "John Doe Williams",
            "expected_authentic": False,
            "description": "5th character 'D' doesn't match surname 'Williams'"
        }
    ]
    
    print("\n2. Test Cases:")
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n   Test Case {i}: {test_case['name']}")
        print(f"   Description: {test_case['description']}")
        print(f"   PAN Number: {test_case['pan_number']}")
        print(f"   Holder Name: {test_case['holder_name']}")
        
        # Validate PAN format
        validation_result = verifier._validate_pan_format(
            test_case['pan_number'], 
            test_case['holder_name']
        )
        
        print(f"   Validation Result: {'PASS' if validation_result['valid'] else 'FAIL'}")
        if validation_result['issues']:
            print(f"   Issues Found: {validation_result['issues']}")
        
        print(f"   Expected: {'PASS' if test_case['expected_authentic'] else 'FAIL'}")

    # Demonstrate a complete verification result (mock)
    print("\n3. Sample Verification Result:")
    print("(This demonstrates the full structure of verification results)")
    
    # Create a mock result
    mock_result = PanVerificationResult(
        is_authentic=True,
        confidence=0.85,
        layout_verified=True,
        text_validated=True,
        security_features_verified=True,
        issuer_verified=True,
        tampering_detected=False,
        pan_number="ABCPD1234E",
        holder_name="John Smith",
        fathers_name="Robert Smith",
        date_of_birth="15/08/1990",
        extracted_fields={
            "pan_number": "ABCPD1234E",
            "holder_name": "John Smith",
            "fathers_name": "Robert Smith",
            "date_of_birth": "15/08/1990"
        },
        issues_found=[]
    )
    
    print_verification_result(mock_result)
    
    # Demonstrate a fake detection result
    print("\n4. Sample Fake Detection Result:")
    
    fake_result = PanVerificationResult(
        is_authentic=False,
        confidence=0.25,
        layout_verified=True,
        text_validated=False,
        security_features_verified=False,
        issuer_verified=False,
        tampering_detected=True,
        pan_number="ABCD1234E",  # Invalid format
        holder_name="John Smith",
        fathers_name="Robert Smith",
        date_of_birth="15/08/1990",
        extracted_fields={
            "pan_number": "ABCD1234E",
            "holder_name": "John Smith",
            "fathers_name": "Robert Smith",
            "date_of_birth": "15/08/1990"
        },
        issues_found=[
            "PAN number format does not match AAAAA9999A pattern",
            "Invalid PAN type code 'D' at position 4",
            "Security features verification failed",
            "Issuer verification failed",
            "Possible tampering detected"
        ]
    )
    
    print_verification_result(fake_result)

def print_verification_result(result: PanVerificationResult):
    """Print a formatted verification result"""
    print(f"   Overall Result: {'LIKELY REAL' if result.is_authentic else 'POSSIBLY FAKE'}")
    print(f"   Confidence Level: {result.confidence:.2f}")
    print(f"   Layout Verified: {result.layout_verified}")
    print(f"   Text Validated: {result.text_validated}")
    print(f"   Security Features Verified: {result.security_features_verified}")
    print(f"   Issuer Verified: {result.issuer_verified}")
    print(f"   Tampering Detected: {result.tampering_detected}")
    print(f"   Extracted PAN Number: {result.pan_number}")
    print(f"   Holder Name: {result.holder_name}")
    print(f"   Father's Name: {result.fathers_name}")
    print(f"   Date of Birth: {result.date_of_birth}")
    
    if result.issues_found:
        print("   Issues Found:")
        for issue in result.issues_found:
            print(f"     - {issue}")
    else:
        print("   No Issues Found")

if __name__ == "__main__":
    demo_pan_verification()