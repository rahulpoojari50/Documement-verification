import cloudinary
import cloudinary.uploader
import cloudinary.api
import base64
import os

# Configure Cloudinary directly
cloudinary.config(
    cloud_name="dlrf0evj0",
    api_key="978394893957497",
    api_secret="XxzS-1R-SCMYGvM6Or3BRmZ8SW0",  # Fixed the last character from 'O' to '0'
    secure=True
)

# Print configuration to verify
config = cloudinary.config()
print("Cloudinary configuration:")
print(f"  Cloud name: {config.cloud_name}")
print(f"  API key: {config.api_key}")
print(f"  API secret length: {len(config.api_secret) if config.api_secret else 0}")
print(f"  Secure: {config.secure}")

# First, let's try to list documents
print("\nTesting list_documents...")
try:
    docs = cloudinary.api.resources(
        type="upload",
        prefix="verified_documents/",
        max_results=100
    )
    print(f"Success! Found {len(docs.get('resources', []))} documents")
    for doc in docs.get('resources', [])[:3]:
        print(f"  - {doc.get('secure_url', 'No URL')}")
except Exception as e:
    print(f"Error listing documents: {e}")

# Now, let's create a simple test image and upload it
print("\nTesting upload...")
try:
    # Create a simple 1x1 pixel PNG image
    image_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    image_bytes = base64.b64decode(image_data)
    
    # Save to a temporary file
    with open("test_image.png", "wb") as f:
        f.write(image_bytes)
    
    # Upload the file
    result = cloudinary.uploader.upload(
        "test_image.png",
        folder="verified_documents",
        resource_type="image"
    )
    
    print(f"Success! Uploaded document:")
    print(f"  Public ID: {result.get('public_id', 'N/A')}")
    print(f"  URL: {result.get('secure_url', 'N/A')}")
    
    # Clean up
    os.remove("test_image.png")
except Exception as e:
    print(f"Error uploading document: {e}")
    # Clean up if the file exists
    if os.path.exists("test_image.png"):
        os.remove("test_image.png")