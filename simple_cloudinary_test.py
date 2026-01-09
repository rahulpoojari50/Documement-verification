import requests
import base64

# Test the list documents endpoint
print("Testing list documents endpoint...")
try:
    response = requests.get("http://localhost:8000/list_documents")
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Found {len(data.get('resources', []))} documents")
        for doc in data.get('resources', [])[:3]:
            print(f"  - {doc.get('secure_url', 'No URL')}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Exception: {e}")

# Test the upload endpoint (we'll create a simple image in memory)
print("\nTesting upload document endpoint...")
try:
    # Create a simple base64 encoded image (1x1 pixel PNG)
    image_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    image_bytes = base64.b64decode(image_data)
    
    files = {'file': ('test.png', image_bytes, 'image/png')}
    response = requests.post("http://localhost:8000/upload_verified_document", files=files)
    
    print(f"Status code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Uploaded document:")
        print(f"  Public ID: {data.get('public_id', 'N/A')}")
        print(f"  URL: {data.get('url', 'N/A')}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Exception: {e}")