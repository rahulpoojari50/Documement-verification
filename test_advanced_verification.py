"""
Test the advanced verification endpoint
"""

import requests
import os

def test_advanced_verification():
    """Test the advanced verification endpoint"""
    print("=== Testing Advanced Verification Endpoint ===")
    
    # Test with our generated documents
    test_images = [
        "/Users/rahulpoojari/Documents/mlmodel/test_docs/test_aadhaar_card.png",
        "/Users/rahulpoojari/Documents/mlmodel/test_docs/fake_aadhaar_card.png"
    ]
    
    for image_path in test_images:
        if not os.path.exists(image_path):
            print(f"❌ File not found: {image_path}")
            continue
            
        print(f"\n--- Testing: {os.path.basename(image_path)} ---")
        
        try:
            with open(image_path, "rb") as f:
                files = {"file": (os.path.basename(image_path), f, "image/png")}
                response = requests.post("http://localhost:8000/advanced_verify_document", files=files)
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Advanced verification successful!")
                print(f"Final Authenticity: {result.get('final_authenticity')}")
                print(f"Confidence Score: {result.get('confidence_score'):.2f}")
                
                recommendations = result.get('recommendations', [])
                if recommendations:
                    print("Recommendations:")
                    for rec in recommendations:
                        print(f"  - {rec}")
                        
                # Show individual verification results
                print("\nIndividual Results:")
                gemini = result.get('gemini_verification', {})
                print(f"  Gemini: {gemini.get('is_authentic', 'N/A')} (confidence: {gemini.get('confidence', 0):.2f})")
                
                ml = result.get('ml_verification', {})
                print(f"  ML Model: {ml.get('prediction', 'N/A')} (confidence: {ml.get('confidence', 0):.2f})")
                
                yolo = result.get('yolo_detection', {})
                print(f"  YOLO Detection: {yolo.get('total_detections', 0)} entities detected")
                
            else:
                print(f"❌ Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_advanced_verification()