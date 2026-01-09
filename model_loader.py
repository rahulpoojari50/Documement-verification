"""
Model Loader for Document Verification
Loads a trained TensorFlow/Keras model and provides prediction functionality
"""

import tensorflow as tf
import os

# Global variable to hold the loaded model
_model = None

def load_model(model_path="document_verifier.h5"):
    """
    Load the document verification model once
    
    Args:
        model_path (str): Path to the saved model file
        
    Returns:
        tf.keras.Model: Loaded model
    """
    global _model
    if _model is None:
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        _model = tf.keras.models.load_model(model_path)
        print(f"Model loaded successfully from {model_path}")
    return _model

def predict_document(image_path, model_path="document_verifier.h5"):
    """
    Predict if a document is REAL or FAKE using the loaded model
    
    Args:
        image_path (str): Path to the image file to predict
        model_path (str): Path to the model file (used if model not yet loaded)
        
    Returns:
        str: "REAL" if document is authentic, "FAKE" otherwise
    """
    # Load model if not already loaded
    model = load_model(model_path)
    
    # Check if image file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    # Preprocess the image
    img = tf.keras.preprocessing.image.load_img(
        image_path, target_size=(224, 224)
    )
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = img / 255.0
    img = img.reshape(1, 224, 224, 3)
    
    # Make prediction
    prediction = model.predict(img)[0][0]
    
    # Log the prediction value for debugging
    print(f"DEBUG: Model prediction value for {image_path}: {prediction}")
    
    # Use a more conservative threshold for REAL classification
    # Only classify as REAL if very confident (> 0.7), otherwise FAKE
    if prediction > 0.7:
        return "REAL"
    else:
        return "FAKE"

# Example usage (if running as main module)
if __name__ == "__main__":
    # This would be used for testing
    # prediction = predict_document("test_docs/aadhaar1.jpg")
    # print("Prediction:", prediction)
    pass