"""
Create a proper test document image for verification
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_test_aadhaar():
    """Create a test Aadhaar card image"""
    # Create a white image with Aadhaar-like dimensions
    width, height = 800, 500
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Try to use a default font or fallback
    try:
        font_large = ImageFont.truetype("arial.ttf", 36)
        font_medium = ImageFont.truetype("arial.ttf", 24)
        font_small = ImageFont.truetype("arial.ttf", 18)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw header
    draw.rectangle([0, 0, width, 60], fill='#1a73e8')
    draw.text((width//2, 30), "GOVERNMENT OF INDIA", fill='white', font=font_large, anchor="mm")
    
    # Draw UIDAI logo area
    draw.rectangle([20, 80, 120, 180], outline='black')
    draw.text((70, 130), "UIDAI", fill='black', font=font_medium, anchor="mm")
    
    # Draw personal info section
    y_pos = 200
    draw.text((50, y_pos), "Name: Rajesh Kumar", fill='black', font=font_medium)
    y_pos += 40
    draw.text((50, y_pos), "DOB: 15/08/1990", fill='black', font=font_medium)
    y_pos += 40
    draw.text((50, y_pos), "Gender: MALE", fill='black', font=font_medium)
    y_pos += 40
    draw.text((50, y_pos), "Address: 123, MG Road, Bangalore, Karnataka", fill='black', font=font_medium)
    
    # Draw Aadhaar number
    y_pos += 60
    draw.text((50, y_pos), "Aadhaar Number: 1234 5678 9012", fill='black', font=font_large)
    
    # Draw QR code area
    draw.rectangle([600, 200, 750, 350], outline='black')
    draw.text((675, 275), "QR CODE", fill='black', font=font_medium, anchor="mm")
    
    # Draw photo area
    draw.rectangle([600, 50, 750, 180], outline='black')
    draw.text((675, 115), "PHOTO", fill='black', font=font_medium, anchor="mm")
    
    # Draw footer
    y_pos = height - 50
    draw.text((width//2, y_pos), "THIS IS A TEST DOCUMENT - NOT FOR OFFICIAL USE", fill='red', font=font_small, anchor="mm")
    
    # Save the image
    image.save('/Users/rahulpoojari/Documents/mlmodel/test_docs/test_aadhaar_card.png')
    print("Test Aadhaar card created: test_docs/test_aadhaar_card.png")
    return '/Users/rahulpoojari/Documents/mlmodel/test_docs/test_aadhaar_card.png'

def create_fake_aadhaar():
    """Create a fake Aadhaar card with intentional errors"""
    # Create a white image with Aadhaar-like dimensions
    width, height = 800, 500
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Try to use a default font or fallback
    try:
        font_large = ImageFont.truetype("arial.ttf", 36)
        font_medium = ImageFont.truetype("arial.ttf", 24)
        font_small = ImageFont.truetype("arial.ttf", 18)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # Draw header with intentional error
    draw.rectangle([0, 0, width, 60], fill='#1a73e8')
    draw.text((width//2, 30), "GOVERNMENT OF INDIYA", fill='white', font=font_large, anchor="mm")  # Intentional error: INDIYA instead of INDIA
    
    # Draw UIDAI logo area
    draw.rectangle([20, 80, 120, 180], outline='black')
    draw.text((70, 130), "UIDAI", fill='black', font=font_medium, anchor="mm")
    
    # Draw personal info section
    y_pos = 200
    draw.text((50, y_pos), "Name: John Doe", fill='black', font=font_medium)
    y_pos += 40
    draw.text((50, y_pos), "DOB: 01/01/2000", fill='black', font=font_medium)
    y_pos += 40
    draw.text((50, y_pos), "Gender: MALE", fill='black', font=font_medium)
    y_pos += 40
    draw.text((50, y_pos), "Address: 456, Fake Street, Mumbai, Maharashtra", fill='black', font=font_medium)
    
    # Draw fake Aadhaar number with suspicious pattern
    y_pos += 60
    draw.text((50, y_pos), "Aadhaar Number: 0011 0022 0033", fill='black', font=font_large)  # Suspicious sequential pattern
    
    # Draw QR code area
    draw.rectangle([600, 200, 750, 350], outline='black')
    draw.text((675, 275), "QR CODE", fill='black', font=font_medium, anchor="mm")
    
    # Draw photo area
    draw.rectangle([600, 50, 750, 180], outline='black')
    draw.text((675, 115), "PHOTO", fill='black', font=font_medium, anchor="mm")
    
    # Draw footer
    y_pos = height - 50
    draw.text((width//2, y_pos), "THIS IS A FAKE TEST DOCUMENT", fill='red', font=font_small, anchor="mm")
    
    # Save the image
    image.save('/Users/rahulpoojari/Documents/mlmodel/test_docs/fake_aadhaar_card.png')
    print("Fake Aadhaar card created: test_docs/fake_aadhaar_card.png")
    return '/Users/rahulpoojari/Documents/mlmodel/test_docs/fake_aadhaar_card.png'

if __name__ == "__main__":
    # Create both test images
    real_doc = create_test_aadhaar()
    fake_doc = create_fake_aadhaar()
    print(f"Created real document: {real_doc}")
    print(f"Created fake document: {fake_doc}")