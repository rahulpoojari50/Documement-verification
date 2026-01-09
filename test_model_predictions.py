"""
Test the model predictions directly to see what values it's returning
"""

import sys
sys.path.append('/Users/rahulpoojari/Documents/mlmodel')

from model_loader import predict_document
import tensorflow as tf
import os

def test_model_predictions():
    """Test the model predictions directly"""
    # Paths to our test documents
    real_doc = "/Users/rahulpoojari/Documents/mlmodel/test_docs/test_aadhaar_card.png"
    fake_doc = "/Users/rahulpoojari/Documents/mlmodel/test_docs/fake_aadhaar_card.png"
    
    # Load the model
    model_path = "document_verifier.h5"
    if not os.path.exists(model_path):
        print(f"Model file not found: {model_path}")
        return
    
    print("Loading model...")
    model = tf.keras.models.load_model(model_path)
    print(f"Model loaded successfully from {model_path}")
    
    # Test both documents
    for doc_path, doc_name in [(real_doc, "Real Document"), (fake_doc, "Fake Document")]:
        if not os.path.exists(doc_path):
            print(f"{doc_name} not found: {doc_path}")
            continue
            
        print(f"\n--- Testing {doc_name} ---")
        print(f"Document path: {doc_path}")
        
        # Get direct prediction value
        img = tf.keras.preprocessing.image.load_img(doc_path, target_size=(224, 224))
        img = tf.keras.preprocessing.image.img_to_array(img)
        img = img / 255.0
        img = img.reshape(1, 224, 224, 3)
        
        prediction = model.predict(img)[0][0]
        result = "REAL" if prediction > 0.5 else "FAKE"
        
        print(f"Raw prediction value: {prediction}")
        print(f"Thresholded result: {result}")
        print(f"Classification: {result}")
        
        # Also test with our function
        func_result = predict_document(doc_path, model_path)
        print(f"Function result: {func_result}")

if __name__ == "__main__":
    test_model_predictions()