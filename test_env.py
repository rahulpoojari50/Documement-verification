import torch
import torchvision
import cv2
import numpy as np

print("Environment check:")
print(f"PyTorch version: {torch.__version__}")
print(f"Torchvision version: {torchvision.__version__}")
print(f"OpenCV version: {cv2.__version__}")

# Test creating a simple tensor
x = torch.randn(3, 4)
print(f"Tensor test: {x}")

# Test creating a simple image
img = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
print(f"Image test shape: {img.shape}")

print("All tests passed!")