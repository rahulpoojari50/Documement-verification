import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms, models
from PIL import Image
import os
from sklearn.metrics import accuracy_score
import argparse

# Simple dataset class
class SimpleDataset(Dataset):
    def __init__(self, root_dir, transform=None, num_samples=100):
        self.root_dir = root_dir
        self.transform = transform
        self.images = []
        self.labels = []
        
        # Load a small number of images for quick testing
        count = 0
        for label, class_name in enumerate(['fake', 'original']):
            class_dir = os.path.join(root_dir, class_name)
            if os.path.exists(class_dir):
                for img_name in os.listdir(class_dir):
                    if img_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                        self.images.append(os.path.join(class_dir, img_name))
                        self.labels.append(label)
                        count += 1
                        if count >= num_samples:
                            break
                if count >= num_samples:
                    break
    
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

# Simple model
class SimpleClassifier(nn.Module):
    def __init__(self, num_classes=2):
        super(SimpleClassifier, self).__init__()
        self.backbone = models.mobilenet_v2(pretrained=True)
        # Freeze early layers
        for param in self.backbone.features[:-5].parameters():
            param.requires_grad = False
        num_features = self.backbone.classifier[1].in_features
        self.backbone.classifier[1] = nn.Linear(num_features, num_classes)
    
    def forward(self, x):
        return self.backbone(x)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--epochs', type=int, default=2)
    parser.add_argument('--batch-size', type=int, default=8)
    parser.add_argument('--lr', type=float, default=0.001)
    args = parser.parse_args()
    
    # Device
    device = torch.device('cpu')  # Use CPU for simplicity
    print(f'Using device: {device}')
    
    # Transforms
    transform = transforms.Compose([
        transforms.Resize((128, 128)),  # Smaller size for faster training
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Datasets
    train_dataset = SimpleDataset('data/processed/train', transform=transform, num_samples=50)
    val_dataset = SimpleDataset('data/processed/val', transform=transform, num_samples=20)
    
    print(f'Training samples: {len(train_dataset)}')
    print(f'Validation samples: {len(val_dataset)}')
    
    # Data loaders
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False)
    
    # Model
    model = SimpleClassifier(num_classes=2).to(device)
    
    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)
    
    # Training loop
    for epoch in range(args.epochs):
        # Training
        model.train()
        train_loss = 0.0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
        
        # Validation
        model.eval()
        val_predictions = []
        val_labels = []
        with torch.no_grad():
            for images, labels in val_loader:
                images, labels = images.to(device), labels.to(device)
                outputs = model(images)
                _, predicted = torch.max(outputs, 1)
                val_predictions.extend(predicted.cpu().numpy())
                val_labels.extend(labels.cpu().numpy())
        
        val_accuracy = accuracy_score(val_labels, val_predictions)
        avg_train_loss = train_loss / len(train_loader)
        
        print(f'Epoch [{epoch+1}/{args.epochs}], Loss: {avg_train_loss:.4f}, Val Acc: {val_accuracy:.4f}')
    
    # Save model
    os.makedirs('models', exist_ok=True)
    torch.save({
        'model_state_dict': model.state_dict(),
        'model_architecture': 'mobilenet_v2'
    }, 'models/simple_classifier.pth')
    
    print('Model saved to models/simple_classifier.pth')

if __name__ == '__main__':
    main()