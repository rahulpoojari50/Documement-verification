"""
Check Cloudinary for verified documents
"""

import cloudinary
import cloudinary.api
import os

# Configure Cloudinary
cloudinary.config(
    cloud_name="dlrf0evj0",
    api_key="978394893957497",
    api_secret="XxzS-1R-SCMYGvM6Or3BRmZ8SW0",
    secure=True
)

def list_verified_documents():
    """List all verified documents in Cloudinary"""
    try:
        print("Checking Cloudinary for verified documents...")
        
        # List resources in the verified_documents folder
        resources = cloudinary.api.resources(
            type="upload",
            prefix="verified_documents/",
            max_results=100
        )
        
        print(f"Found {len(resources['resources'])} verified documents:")
        
        if len(resources['resources']) == 0:
            print("No verified documents found in Cloudinary.")
            return
            
        for i, resource in enumerate(resources['resources'], 1):
            print(f"{i}. Public ID: {resource['public_id']}")
            print(f"   URL: {resource['secure_url']}")
            print(f"   Created: {resource['created_at']}")
            print()
            
    except Exception as e:
        print(f"Error accessing Cloudinary: {str(e)}")
        
        # Check if it's an authentication error
        if "Unauthorized" in str(e) or "401" in str(e):
            print("Authentication failed. Please check your Cloudinary credentials.")
        elif "404" in str(e):
            print("Folder not found. No documents have been uploaded yet.")

if __name__ == "__main__":
    list_verified_documents()