"""
Debug Cloudinary Integration
"""

import cloudinary
import cloudinary.api
import os

# Configure Cloudinary with your credentials
cloudinary.config(
    cloud_name="dlrf0evj0",
    api_key="978394893957497",
    api_secret="XxzS-1R-SCMYGvM6Or3BRmZ8SW0",
    secure=True
)

def debug_cloudinary():
    """Debug Cloudinary integration and list all documents"""
    try:
        print("=== Cloudinary Debug Info ===")
        print(f"Cloud Name: dlrf0evj0")
        print(f"API Key: 978394893957497")
        print(f"API Secret: ***REDACTED***")
        print()
        
        # Test connection by listing all resources
        print("Listing ALL resources in Cloudinary account...")
        all_resources = cloudinary.api.resources(max_results=10)
        print(f"Successfully connected to Cloudinary")
        print()
        
        # List resources in the verified_documents folder specifically
        print("Listing resources in 'verified_documents' folder...")
        try:
            verified_resources = cloudinary.api.resources(
                type="upload",
                prefix="verified_documents/",
                max_results=100
            )
            count = len(verified_resources.get('resources', []))
            print(f"Verified documents found: {count}")
            
            if count > 0:
                print("\nVerified Documents:")
                for i, resource in enumerate(verified_resources['resources'], 1):
                    print(f"{i}. Name: {resource.get('public_id', 'N/A')}")
                    print(f"   URL: {resource.get('secure_url', 'N/A')}")
                    print(f"   Created: {resource.get('created_at', 'N/A')}")
                    print()
            else:
                print("No verified documents found in the 'verified_documents' folder.")
        except Exception as folder_error:
            print(f"Error accessing 'verified_documents' folder: {folder_error}")
        
        # List resources without prefix to see all folders
        print("\nAll folders/resources:")
        try:
            all_folders = cloudinary.api.resources(type="upload", max_results=50)
            folders = set()
            for resource in all_folders.get('resources', []):
                public_id = resource.get('public_id', '')
                if '/' in public_id:
                    folder = public_id.split('/')[0]
                    folders.add(folder)
            
            if folders:
                print("Available folders:")
                for folder in sorted(folders):
                    print(f"  - {folder}")
            else:
                print("No folders found.")
        except Exception as all_error:
            print(f"Error listing all resources: {all_error}")
            
    except Exception as e:
        print(f"❌ Error connecting to Cloudinary: {str(e)}")
        
        # Check for common errors
        if "unauthorized" in str(e).lower() or "401" in str(e):
            print("❌ Authentication failed. Please check your Cloudinary credentials.")
        elif "not found" in str(e).lower() or "404" in str(e):
            print("❌ Resource not found. The folder might not exist yet.")
        elif "forbidden" in str(e).lower() or "403" in str(e):
            print("❌ Access forbidden. Please check your API permissions.")

if __name__ == "__main__":
    debug_cloudinary()