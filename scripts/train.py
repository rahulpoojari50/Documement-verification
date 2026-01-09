import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, models
import os
from PIL import Image
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np
import argparse
import json
from datetime import datetime

# Custom dataset class
class DocumentDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.images = []
        self.labels = []
        
        # Load images and labels
        for label, class_name in enumerate(['fake', 'original']):
            class_dir = os.path.join(root_dir, class_name)
            if os.path.exists(class_dir):
                for img_name in os.listdir(class_dir):
                    if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                        self.images.append(os.path.join(class_dir, img_name))
                        self.labels.append(label)
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        img_path = self.images[idx]
        label = self.labels[idx]
        
        # Load image
        image = Image.open(img_path).convert('RGB')
        
        # Apply transformations
        if self.transform:
            image = self.transform(image)
            
        return image, label

# Model class using transfer learning with EfficientNet
class DocumentClassifier(nn.Module):
    def __init__(self, num_classes=2, model_name='efficientnet'):
        super(DocumentClassifier, self).__init__()
        
        if model_name == 'efficientnet':
            # Using EfficientNet-B0
            self.backbone = models.efficientnet_b0(pretrained=True)
            num_features = self.backbone.classifier[1].in_features
            # Replace the classifier
            self.backbone.classifier = nn.Linear(num_features, num_classes)
        elif model_name == 'resnet':
            # Using ResNet-50
            self.backbone = models.resnet50(pretrained=True)
            num_features = self.backbone.fc.in_features
            # Replace the final fully connected layer
            self.backbone.fc = nn.Linear(num_features, num_classes)
        else:
            # Default to MobileNetV3
            self.backbone = models.mobilenet_v3_small(pretrained=True)
            num_features = self.backbone.classifier[3].in_features
            # Replace the classifier
            self.backbone.classifier[3] = nn.Linear(num_features, num_classes)
        
        self.model_name = model_name
    
    def forward(self, x):
        return self.backbone(x)

# Training function
def train_model(model, train_loader, val_loader, criterion, optimizer, num_epochs=10, device='cpu'):
    train_losses = []
    val_accuracies = []
    
    best_val_acc = 0.0
    best_model_state = None
    
    for epoch in range(num_epochs):
        # Training phase
        model.train()
        running_loss = 0.0
        
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()
            
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * inputs.size(0)
        
        epoch_loss = running_loss / len(train_loader.dataset)
        train_losses.append(epoch_loss)
        
        # Validation phase
        model.eval()
        val_predictions = []
        val_labels = []
        
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
                
                val_predictions.extend(preds.cpu().numpy())
                val_labels.extend(labels.cpu().numpy())
        
        val_acc = accuracy_score(val_labels, val_predictions)
        val_accuracies.append(val_acc)
        
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss:.4f}, Val Acc: {val_acc:.4f}')
        
        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_model_state = model.state_dict().copy()
    
    # Load best model state
    if best_model_state is not None:
        model.load_state_dict(best_model_state)
    
    return model, train_losses, val_accuracies

# Main training function
def main():
    parser = argparse.ArgumentParser(description='Train document authenticity detection model')
    parser.add_argument('--model', type=str, default='efficientnet', 
                        choices=['efficientnet', 'resnet', 'mobilenet'],
                        help='Model architecture to use')
    parser.add_argument('--epochs', type=int, default=10, help='Number of training epochs')
    parser.add_argument('--batch-size', type=int, default=32, help='Batch size')
    parser.add_argument('--lr', type=float, default=0.001, help='Learning rate')
    parser.add_argument('--data-path', type=str, default='data/processed', help='Path to processed data')
    
    args = parser.parse_args()
    
    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Using device: {device}')
    
    # Data transforms
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=15),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    val_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Create datasets
    train_dataset = DocumentDataset(
        root_dir=os.path.join(args.data_path, 'train'),
        transform=train_transform
    )
    
    val_dataset = DocumentDataset(
        root_dir=os.path.join(args.data_path, 'val'),
        transform=val_transform
    )
    
    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False)
    
    print(f'Training samples: {len(train_dataset)}')
    print(f'Validation samples: {len(val_dataset)}')
    
    # Create model
    model = DocumentClassifier(num_classes=2, model_name=args.model).to(device)
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=args.lr)
    
    # Train model
    print(f'Starting training with {args.model}...')
    model, train_losses, val_accuracies = train_model(
        model, train_loader, val_loader, criterion, optimizer, 
        num_epochs=args.epochs, device=device
    )
    
    # Save model
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_path = f'models/document_classifier_{args.model}_{timestamp}.pth'
    os.makedirs('models', exist_ok=True)
    
    torch.save({
        'model_state_dict': model.state_dict(),
        'model_architecture': args.model,
        'train_losses': train_losses,
        'val_accuracies': val_accuracies,
        'epochs': args.epochs,
        'batch_size': args.batch_size,
        'learning_rate': args.lr
    }, model_path)
    
    print(f'Model saved to {model_path}')
    
    # Save training metrics
    metrics = {
        'final_train_loss': train_losses[-1],
        'final_val_accuracy': val_accuracies[-1],
        'best_val_accuracy': max(val_accuracies),
        'training_timestamp': timestamp
    }
    
    metrics_path = f'models/training_metrics_{timestamp}.json'
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f'Training metrics saved to {metrics_path}')
    print('Training complete!')

if __name__ == '__main__':
    main()