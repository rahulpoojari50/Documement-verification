"""
Test the spelling-focused verification
"""

import requests
import base64
import os

def test_spelling_focus():
    """Test the spelling-focused verification that considers documents fake only if spelling errors are found"""
    print("Testing spelling-focused verification...")
    
    # Create a simple test image
    image_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    image_bytes = base64.b64decode(image_data)
    
    with open("test_document.png", "wb") as f:
        f.write(image_bytes)
    
    try:
        # Test the spelling-focused Gemini verification endpoint
        with open("test_document.png", "rb") as f:
            files = {"file": ("test_document.png", f, "image/png")}
            response = requests.post("http://127.0.0.1:8000/verify_document_with_gemini", files=files)
        
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
                    
            # Check if spelling errors are properly detected
            issues = result.get('issues_found', [])
            spelling_errors_detected = any(
                ("spelling" in str(issue).lower() and "government" in str(issue).lower()) or
                ("indiya" in str(issue).lower() and "india" in str(issue).lower()) or
                ("misspell" in str(issue).lower() and "government" in str(issue).lower())
                for issue in issues
            )
            
            if spelling_errors_detected:
                print("\n✅ Spelling errors properly detected - document correctly marked as fake")
            elif result.get('is_authentic', False):
                print("\n✅ No spelling errors found - document correctly marked as authentic")
            else:
                print("\nℹ️ Document marked as fake but not due to spelling errors")
                
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
    test_spelling_focus()