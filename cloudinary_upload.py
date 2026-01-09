"""
Cloudinary Upload Function
Handles uploading verified documents to Cloudinary storage
"""

import cloudinary
import cloudinary.uploader
import os

# Configure Cloudinary (uses CLOUDINARY_URL environment variable)
cloudinary.config(secure=True)

def upload_verified_document(image_path):
    """
    Upload a verified document to Cloudinary
    
    Args:
        image_path (str): Path to the image file to upload
        
    Returns:
        tuple: (secure_url, public_id) of the uploaded document
        
    Raises:
        Exception: If upload fails
    """
    # Check if image file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    try:
        # Upload the image to Cloudinary
        result = cloudinary.uploader.upload(
            image_path,
            folder="verified_documents",
            resource_type="image"
        )
        
        return result["secure_url"], result["public_id"]
    except Exception as e:
        raise Exception(f"Failed to upload document: {str(e)}")

# Example usage (if running as main module)
if __name__ == "__main__":
    # This would be used for testing
    # url, public_id = upload_verified_document("test_docs/aadhaar1.jpg")
    # print(f"Uploaded: {url}")
    pass