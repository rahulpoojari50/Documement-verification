import os
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

def create_sample_images():
    """Create sample images for testing the data preparation pipeline"""
    
    # Create directories if they don't exist
    dirs = [
        'data/raw/fake_aadhar',
        'data/raw/original_aadhar',
        'data/raw/fake_pan',
        'data/raw/original_pan',
        'data/raw/fake_dl',
        'data/raw/original_dl'
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    # Create sample images for each category
    categories = [
        ('fake_aadhar', 15),
        ('original_aadhar', 15),
        ('fake_pan', 10),
        ('original_pan', 10),
        ('fake_dl', 8),
        ('original_dl', 8)
    ]
    
    for category, count in categories:
        for i in range(count):
            # Create a sample image
            img = np.random.randint(0, 255, (400, 600, 3), dtype=np.uint8)
            
            # Add some text to make it look like a document
            pil_img = Image.fromarray(img)
            draw = ImageDraw.Draw(pil_img)
            
            try:
                # Try to use a default font
                font = ImageFont.load_default()
            except:
                # If that fails, just draw without font
                font = None
            
            # Draw text on image
            text = f"{category.upper()} SAMPLE {i+1}"
            draw.text((50, 50), text, fill=(255, 255, 255), font=font)
            
            # Convert back to OpenCV format
            img_with_text = np.array(pil_img)
            
            # Save image
            filename = f"{category}_sample_{i+1}.jpg"
            filepath = os.path.join(f'data/raw/{category}', filename)
            cv2.imwrite(filepath, img_with_text)
    
    print("Sample images created successfully!")

if __name__ == "__main__":
    create_sample_images()