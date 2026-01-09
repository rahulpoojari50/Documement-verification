"""
Test the strict verification with critical error detection
"""

import requests
import base64
import os

def test_strict_verification():
    """Test the strict verification that treats critical errors as definitive proof of fake documents"""
    print("Testing strict verification with critical error detection...")
    
    # Create a simple test image
    image_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    image_bytes = base64.b64decode(image_data)
    
    with open("test_document.png", "wb") as f:
        f.write(image_bytes)
    
    try:
        # Test the enhanced Gemini verification endpoint
        with open("test_document.png", "rb") as f:
            files = {"file": ("test_document.png", f, "image/png")}
            response = requests.post("http://localhost:8000/verify_document_with_gemini", files=files)
        
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("Success!")
            print(f"Is Authentic: {result.get('is_authentic', 'N/A')}")
            print(f"Confidence: {result.get('confidence', 'N/A')}")
            print(f"Explanation: {result.get('explanation', 'N/A')[:200]}...")
            
            if result.get('issues_found'):
                print("Issues Found:")
                for issue in result.get('issues_found', [])[:10]:  # Show first 10 issues
                    print(f"  - {issue}")
                    
            if result.get('verification_factors'):
                print("Verification Factors Checked:")
                for factor in result.get('verification_factors', [])[:5]:  # Show first 5 factors
                    print(f"  - {factor}")
                    
            # Check if critical errors are properly detected
            issues = result.get('issues_found', [])
            critical_errors_detected = any(
                "spelling" in str(issue).lower() or 
                "indiya" in str(issue).lower() or
                "sequential" in str(issue).lower() or
                "stock image" in str(issue).lower() or
                "fake" in str(issue).lower() or
                "mismatch" in str(issue).lower()
                for issue in issues
            )
            
            if critical_errors_detected:
                print("\n✅ Critical errors properly detected - document correctly marked as fake")
            elif not result.get('is_authentic', True):
                print("\n⚠️ Document marked as fake but critical errors not explicitly detected")
            else:
                print("\nℹ️ Document marked as authentic")
                
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")
    finally:
        # Clean up test images
        if os.path.exists("test_document.png"):
            os.remove("test_document.png")
            print(f"Cleaned up test image: test_document.png")

if __name__ == "__main__":
    test_strict_verification()