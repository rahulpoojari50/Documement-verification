import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import numpy as np
import cv2
import os
import argparse
from scripts.train import DocumentClassifier
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def load_model(model_path, device):
    """Load trained model"""
    checkpoint = torch.load(model_path, map_location=device)
    model_architecture = checkpoint.get('model_architecture', 'efficientnet')
    
    model = DocumentClassifier(num_classes=2, model_name=model_architecture).to(device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    return model, model_architecture

def preprocess_image(image_path):
    """Preprocess image for inference"""
    # Define transforms
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Load image
    image = Image.open(image_path).convert('RGB')
    original_image = np.array(image)
    
    # Apply transforms
    input_tensor = transform(image)
    input_batch = input_tensor.unsqueeze(0)  # Add batch dimension
    
    return input_batch, original_image

def generate_gradcam(model, input_tensor, target_class=None, device='cpu'):
    """Generate Grad-CAM heatmap"""
    model.eval()
    
    # Register hooks to get feature maps and gradients
    features = {}
    gradients = {}
    
    def get_features(name):
        def hook(module, input, output):
            features[name] = output
        return hook
    
    def get_gradients(name):
        def hook(module, grad_input, grad_output):
            gradients[name] = grad_output[0]
        return hook
    
    # Register hooks on the last convolutional layer
    if hasattr(model.backbone, 'features'):
        # For EfficientNet and MobileNet
        target_layer = model.backbone.features[-1]
    else:
        # For ResNet
        target_layer = model.backbone.layer4[-1]
    
    hook1 = target_layer.register_forward_hook(get_features('feat'))
    hook2 = target_layer.register_backward_hook(get_gradients('grad'))
    
    # Forward pass
    input_tensor = input_tensor.to(device)
    output = model(input_tensor)
    
    # Get predicted class
    if target_class is None:
        target_class = output.argmax(dim=1)
    
    # Backward pass
    model.zero_grad()
    one_hot = torch.zeros_like(output)
    one_hot.scatter_(1, target_class.unsqueeze(0).unsqueeze(0), 1)
    output.backward(gradient=one_hot, retain_graph=True)
    
    # Get features and gradients
    feat = features['feat']
    grad = gradients['grad']
    
    # Global average pooling of gradients
    weights = torch.mean(grad, dim=(2, 3), keepdim=True)
    
    # Weighted sum of feature maps
    cam = torch.sum(weights * feat, dim=1, keepdim=True)
    cam = torch.relu(cam)
    
    # Normalize
    cam -= torch.min(cam)
    cam /= torch.max(cam) + 1e-8
    
    # Remove hooks
    hook1.remove()
    hook2.remove()
    
    return cam.detach().cpu().numpy()[0, 0]

def overlay_heatmap(original_image, heatmap, alpha=0.4):
    """Overlay heatmap on original image"""
    # Resize heatmap to match original image
    heatmap_resized = cv2.resize(heatmap, (original_image.shape[1], original_image.shape[0]))
    
    # Convert heatmap to RGB
    heatmap_rgb = cv2.applyColorMap(np.uint8(255 * heatmap_resized), cv2.COLORMAP_JET)
    
    # Overlay heatmap on original image
    overlay = cv2.addWeighted(original_image, 1-alpha, heatmap_rgb, alpha, 0)
    
    return overlay

def predict_document(model, image_path, device='cpu'):
    """Predict if document is original or fake"""
    # Preprocess image
    input_tensor, original_image = preprocess_image(image_path)
    
    # Move to device
    input_tensor = input_tensor.to(device)
    
    # Forward pass
    with torch.no_grad():
        output = model(input_tensor)
        probabilities = torch.softmax(output, dim=1)
        confidence, predicted = torch.max(probabilities, 1)
    
    # Convert to numpy
    confidence = confidence.item()
    predicted = predicted.item()
    probabilities = probabilities.cpu().numpy()[0]
    
    # Class labels
    class_labels = ['Fake', 'Original']
    predicted_label = class_labels[predicted]
    
    # Generate Grad-CAM heatmap
    heatmap = generate_gradcam(model, input_tensor, predicted, device)
    
    # Overlay heatmap
    heatmap_overlay = overlay_heatmap(original_image, heatmap)
    
    return {
        'predicted_label': predicted_label,
        'confidence': confidence,
        'probabilities': probabilities.tolist(),
        'heatmap': heatmap,
        'heatmap_overlay': heatmap_overlay
    }

def main():
    parser = argparse.ArgumentParser(description='Inference script for document authenticity detection')
    parser.add_argument('--model-path', type=str, required=True, help='Path to trained model')
    parser.add_argument('--image-path', type=str, required=True, help='Path to image for prediction')
    parser.add_argument('--save-heatmap', action='store_true', help='Save heatmap overlay image')
    
    args = parser.parse_args()
    
    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Using device: {device}')
    
    # Load model
    print('Loading model...')
    model, architecture = load_model(args.model_path, device)
    print(f'Loaded {architecture} model')
    
    # Check if image exists
    if not os.path.exists(args.image_path):
        print(f'Error: Image path {args.image_path} does not exist')
        return
    
    # Predict
    print('Performing prediction...')
    result = predict_document(model, args.image_path, device)
    
    # Print results
    print('\n=== Prediction Results ===')
    print(f'Predicted Label: {result["predicted_label"]}')
    print(f'Confidence: {result["confidence"]:.4f}')
    print(f'Fake Probability: {result["probabilities"][0]:.4f}')
    print(f'Original Probability: {result["probabilities"][1]:.4f}')
    
    # Save heatmap if requested
    if args.save_heatmap:
        os.makedirs('results', exist_ok=True)
        heatmap_path = 'results/heatmap_overlay.jpg'
        cv2.imwrite(heatmap_path, cv2.cvtColor(result['heatmap_overlay'], cv2.COLOR_RGB2BGR))
        print(f'Heatmap overlay saved to {heatmap_path}')
    
    print('\nPrediction complete!')

if __name__ == '__main__':
    main()