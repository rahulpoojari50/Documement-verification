"""
Connect Model + Cloudinary
This is the core logic that connects document verification with Cloudinary storage
"""

from model_loader import predict_document
from cloudinary_upload import upload_verified_document

def process_document(image_path, model_path="document_verifier.h5"):
    """
    Process a document through the complete verification and storage pipeline
    
    Args:
        image_path (str): Path to the image file to process
        model_path (str): Path to the model file
        
    Returns:
        dict: Result of the processing with status and details
    """
    try:
        # 1. Call model for prediction
        prediction = predict_document(image_path, model_path)
        
        print("MODEL OUTPUT:", prediction)
        
        # 2. Upload to Cloudinary regardless of prediction (with appropriate status)
        url, public_id = upload_verified_document(image_path)
        
        # 3. Return result with appropriate status
        if prediction == "REAL":
            return {
                "status": "VERIFIED",
                "prediction": prediction,
                "image_url": url,
                "public_id": public_id,
                "message": "Document verified as REAL and uploaded to Cloudinary"
            }
        else:
            return {
                "status": "UPLOADED_WITH_WARNING",
                "prediction": prediction,
                "image_url": url,
                "public_id": public_id,
                "message": "Document uploaded to Cloudinary but ML model classified it as FAKE"
            }
        
    except Exception as e:
        return {
            "status": "ERROR",
            "message": f"Processing failed: {str(e)}",
            "prediction": None
        }

# Example usage (if running as main module)
if __name__ == "__main__":
    # This would be used for testing
    # response = process_document("test_docs/aadhaar1.jpg")
    # print(response)
    pass