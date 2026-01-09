#!/usr/bin/env python3
"""
Test script for PAN card authenticity classifier
"""

import os
import sys
from pathlib import Path
import glob

# Add the project root to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))

from pan_verification.pan_verifier import PanCardVerifier

def test_pan_classification():
    """Test the PAN card classification with real and fake samples"""
    
    print("Testing PAN Card Authenticity Classification")
    print("=" * 50)
    
    # Initialize the PAN card verifier (which will load the classifier)
    verifier = PanCardVerifier()
    
    # Test real PAN cards
    print("Testing Real PAN Cards:")
    print("-" * 30)
    
    real_samples = glob.glob("data/raw/original_pan/*.jpg")
    for sample in real_samples[:5]:  # Test first 5 real samples
        print(f"\nTesting: {Path(sample).name}")
        try:
            result = verifier.verify_pan_card(sample)
            print(f"  Overall Result: {'AUTHENTIC' if result.is_authentic else 'FAKE'}")
            print(f"  Confidence: {result.confidence:.2f}")
            print(f"  PAN Number: '{result.pan_number}'")
            print(f"  Issues Found: {len(result.issues_found)}")
        except Exception as e:
            print(f"  Error: {e}")
    
    # Test fake PAN cards
    print("\n\nTesting Fake PAN Cards:")
    print("-" * 30)
    
    fake_samples = glob.glob("data/raw/fake_pan/*.jpg")
    for sample in fake_samples[:5]:  # Test first 5 fake samples
        print(f"\nTesting: {Path(sample).name}")
        try:
            result = verifier.verify_pan_card(sample)
            print(f"  Overall Result: {'AUTHENTIC' if result.is_authentic else 'FAKE'}")
            print(f"  Confidence: {result.confidence:.2f}")
            print(f"  PAN Number: '{result.pan_number}'")
            print(f"  Issues Found: {len(result.issues_found)}")
        except Exception as e:
            print(f"  Error: {e}")
    
    # Test with processed data as well
    print("\n\nTesting Processed PAN Cards:")
    print("-" * 30)
    
    processed_real = glob.glob("data/processed/train/original/*pan*.jpg")
    processed_fake = glob.glob("data/processed/train/fake/*pan*.jpg")
    
    print(f"Found {len(processed_real)} processed real PAN cards")
    print(f"Found {len(processed_fake)} processed fake PAN cards")
    
    # Test a few processed samples
    for sample in processed_real[:3]:
        print(f"\nTesting processed real: {Path(sample).name}")
        try:
            result = verifier.verify_pan_card(sample)
            print(f"  Overall Result: {'AUTHENTIC' if result.is_authentic else 'FAKE'}")
            print(f"  Confidence: {result.confidence:.2f}")
            print(f"  PAN Number: '{result.pan_number}'")
        except Exception as e:
            print(f"  Error: {e}")
    
    for sample in processed_fake[:3]:
        print(f"\nTesting processed fake: {Path(sample).name}")
        try:
            result = verifier.verify_pan_card(sample)
            print(f"  Overall Result: {'AUTHENTIC' if result.is_authentic else 'FAKE'}")
            print(f"  Confidence: {result.confidence:.2f}")
            print(f"  PAN Number: '{result.pan_number}'")
        except Exception as e:
            print(f"  Error: {e}")

def test_individual_images():
    """Test individual images to see detailed results"""
    
    print("\n\nDetailed Testing of Individual Images:")
    print("=" * 50)
    
    verifier = PanCardVerifier()
    
    # Test one real and one fake image in detail
    real_sample = "data/raw/original_pan/original_pan_sample_1.jpg"
    fake_sample = "data/raw/fake_pan/fake_pan_sample_1.jpg"
    
    if os.path.exists(real_sample):
        print(f"\nDetailed analysis of real PAN: {Path(real_sample).name}")
        try:
            result = verifier.verify_pan_card(real_sample)
            print(f"  Authenticity: {'AUTHENTIC' if result.is_authentic else 'FAKE'}")
            print(f"  Confidence: {result.confidence:.2f}")
            print(f"  Layout Verified: {result.layout_verified}")
            print(f"  Text Validated: {result.text_validated}")
            print(f"  Security Features: {result.security_features_verified}")
            print(f"  Issuer Verified: {result.issuer_verified}")
            print(f"  Tampering Detected: {result.tampering_detected}")
            print(f"  PAN Number: '{result.pan_number}'")
            print(f"  Holder Name: '{result.holder_name}'")
            if result.issues_found:
                print("  Issues:")
                for issue in result.issues_found[:5]:  # Show first 5 issues
                    print(f"    - {issue}")
        except Exception as e:
            print(f"  Error: {e}")
    
    if os.path.exists(fake_sample):
        print(f"\nDetailed analysis of fake PAN: {Path(fake_sample).name}")
        try:
            result = verifier.verify_pan_card(fake_sample)
            print(f"  Authenticity: {'AUTHENTIC' if result.is_authentic else 'FAKE'}")
            print(f"  Confidence: {result.confidence:.2f}")
            print(f"  Layout Verified: {result.layout_verified}")
            print(f"  Text Validated: {result.text_validated}")
            print(f"  Security Features: {result.security_features_verified}")
            print(f"  Issuer Verified: {result.issuer_verified}")
            print(f"  Tampering Detected: {result.tampering_detected}")
            print(f"  PAN Number: '{result.pan_number}'")
            print(f"  Holder Name: '{result.holder_name}'")
            if result.issues_found:
                print("  Issues:")
                for issue in result.issues_found[:5]:  # Show first 5 issues
                    print(f"    - {issue}")
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    test_pan_classification()
    test_individual_images()