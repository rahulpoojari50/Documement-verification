import base64
import os

# Create test_docs directory if it doesn't exist
os.makedirs('test_docs', exist_ok=True)

# Create a simple 1x1 pixel PNG image
image_data = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=='
image_bytes = base64.b64decode(image_data)

# Save to a test file
with open('test_docs/sample_document.jpg', 'wb') as f:
    f.write(image_bytes)

print('Created sample test image at test_docs/sample_document.jpg')