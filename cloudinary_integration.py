"""
Cloudinary Integration for Document Storage
This module provides functions to upload, view, and delete verified documents using Cloudinary.
"""

import cloudinary
import cloudinary.uploader
import cloudinary.api
import os
from typing import Dict, Any, Optional

# Cloudinary configuration
cloudinary.config(
    cloud_name="dlrf0evj0",
    api_key="978394893957497",
    api_secret="XxzS-1R-SCMYGvM6Or3BRmZ8SW0",  # Fixed the last character from 'O' to '0'
    secure=True
)

def upload_verified_document(image_path: str, folder: str = "verified_documents") -> Dict[str, str]:
    """
    Upload a verified document to Cloudinary.
    
    Args:
        image_path (str): Path to the image file to upload
        folder (str): Folder name in Cloudinary to store the document (default: "verified_documents")
    
    Returns:
        dict: Dictionary containing public_id and url of the uploaded document
    
    Raises:
        Exception: If upload fails
    """
    try:
        # Upload the image to Cloudinary
        result = cloudinary.uploader.upload(
            image_path,
            folder=folder,
            resource_type="image"
        )
        
        return {
            "public_id": result["public_id"],
            "url": result["secure_url"]
        }
    except Exception as e:
        raise Exception(f"Failed to upload document: {str(e)}")

def delete_document(public_id: str) -> bool:
    """
    Delete a document from Cloudinary.
    
    Args:
        public_id (str): Public ID of the document to delete
    
    Returns:
        bool: True if deletion was successful
    
    Raises:
        Exception: If deletion fails
    """
    try:
        cloudinary.uploader.destroy(public_id)
        return True
    except Exception as e:
        raise Exception(f"Failed to delete document: {str(e)}")

def list_documents(prefix: str = "verified_documents/", max_results: int = 100) -> Dict[str, Any]:
    """
    List all stored documents in Cloudinary.
    
    Args:
        prefix (str): Prefix to filter resources (default: "verified_documents/")
        max_results (int): Maximum number of results to return (default: 100)
    
    Returns:
        dict: Dictionary containing the list of resources
    
    Raises:
        Exception: If listing fails
    """
    try:
        return cloudinary.api.resources(
            type="upload",
            prefix=prefix,
            max_results=max_results
        )
    except Exception as e:
        raise Exception(f"Failed to list documents: {str(e)}")

def get_document_url(public_id: str) -> str:
    """
    Get the secure URL for a document using its public ID.
    
    Args:
        public_id (str): Public ID of the document
    
    Returns:
        str: Secure URL of the document
    """
    return cloudinary.utils.cloudinary_url(public_id, secure=True)[0]

# Example usage
if __name__ == "__main__":
    # Example: Upload a document
    # doc = upload_verified_document("aadhaar_real.jpg")
    # print("Stored at:", doc["url"])
    
    # Example: List all documents
    # docs = list_documents()
    # for d in docs["resources"]:
    #     print(d["secure_url"])
    
    # Example: Delete a document
    # delete_document("verified_documents/xxxxx")
    pass