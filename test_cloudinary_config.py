import cloudinary
import os

# Print environment variables
print("Environment variables:")
print(f"CLOUDINARY_URL: {os.environ.get('CLOUDINARY_URL', 'Not set')}")
print(f"CLOUDINARY_API_SECRET: {os.environ.get('CLOUDINARY_API_SECRET', 'Not set')}")

# Cloudinary configuration
cloudinary.config(
    cloud_name="dlrf0evj0",
    api_key="978394893957497",
    api_secret="XxzS-1R-SCMYGvM6Or3BRmZ8SWO",
    secure=True
)

# Print configuration
config = cloudinary.config()
print("\nCloudinary configuration:")
print(f"Cloud name: {config.cloud_name}")
print(f"API key: {config.api_key}")
print(f"API secret: {config.api_secret}")
print(f"Secure: {config.secure}")