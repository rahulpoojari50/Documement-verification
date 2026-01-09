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
            print(f"  Authentic: {result.is_authentic}")
            print(f"  Confidence: {result.confidence:.2f}")
            if result.pan_number:
                print(f"  PAN Number: {result.pan_number}")
            if result.issues_found:
                print(f"  Issues: {', '.join(result.issues_found)}")
        except Exception as e:
            print(f"  Error: {e}")
    
    print("\n" + "=" * 50)
    
    # Test fake PAN cards
    print("Testing Fake PAN Cards:")
    print("-" * 30)
    
    fake_samples = glob.glob("data/raw/fake_pan/*.jpg")
    for sample in fake_samples[:5]:  # Test first 5 fake samples
        print(f"\nTesting: {Path(sample).name}")
        try:
            result = verifier.verify_pan_card(sample)
            print(f"  Authentic: {result.is_authentic}")
            print(f"  Confidence: {result.confidence:.2f}")
            if result.pan_number:
                print(f"  PAN Number: {result.pan_number}")
            if result.issues_found:
                print(f"  Issues: {', '.join(result.issues_found)}")
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    test_pan_classification()