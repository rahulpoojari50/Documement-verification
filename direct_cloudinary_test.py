import base64
import os

# Add the current directory to the Python path
import sys
sys.path.append('/Users/rahulpoojari/Documents/mlmodel')

# Import our cloudinary integration module
from cloudinary_integration import upload_verified_document, list_documents

# First, let's try to list documents
print("Testing list_documents function...")
try:
    docs = list_documents()
    print(f"Success! Found {len(docs.get('resources', []))} documents")
    for doc in docs.get('resources', [])[:3]:
        print(f"  - {doc.get('secure_url', 'No URL')}")
except Exception as e:
    print(f"Error listing documents: {e}")

# Now, let's create a simple test image and upload it
print("\nTesting upload_verified_document function...")
try:
    # Create a simple 1x1 pixel PNG image
    image_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    image_bytes = base64.b64decode(image_data)
    
    # Save to a temporary file
    with open("test_image.png", "wb") as f:
        f.write(image_bytes)
    
    # Upload the file
    result = upload_verified_document("test_image.png")
    print(f"Success! Uploaded document:")
    print(f"  Public ID: {result.get('public_id', 'N/A')}")
    print(f"  URL: {result.get('url', 'N/A')}")
    
    # Clean up
    os.remove("test_image.png")
except Exception as e:
    print(f"Error uploading document: {e}")
    # Clean up if the file exists
    if os.path.exists("test_image.png"):
        os.remove("test_image.png")