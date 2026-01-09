import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms
from PIL import Image
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_curve, auc
import json
import argparse
from scripts.train import DocumentDataset, DocumentClassifier

def evaluate_model(model, test_loader, device='cpu'):
    """Evaluate the model on test data"""
    model.eval()
    
    all_predictions = []
    all_probabilities = []
    all_labels = []
    
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            
            outputs = model(inputs)
            probabilities = torch.softmax(outputs, dim=1)
            _, predictions = torch.max(outputs, 1)
            
            all_predictions.extend(predictions.cpu().numpy())
            all_probabilities.extend(probabilities.cpu().numpy()[:, 1])  # Probability of positive class
            all_labels.extend(labels.cpu().numpy())
    
    # Calculate metrics
    accuracy = accuracy_score(all_labels, all_predictions)
    precision = precision_score(all_labels, all_predictions, zero_division=0)
    recall = recall_score(all_labels, all_predictions, zero_division=0)
    f1 = f1_score(all_labels, all_predictions, zero_division=0)
    
    # Confusion matrix
    cm = confusion_matrix(all_labels, all_predictions)
    
    # ROC curve and AUC
    fpr, tpr, _ = roc_curve(all_labels, all_probabilities)
    roc_auc = auc(fpr, tpr)
    
    metrics = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': cm.tolist(),
        'roc_auc': roc_auc
    }
    
    return metrics, all_predictions, all_probabilities, all_labels, fpr, tpr

def plot_confusion_matrix(cm, classes=['Fake', 'Original'], save_path='confusion_matrix.png'):
    """Plot and save confusion matrix"""
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_roc_curve(fpr, tpr, roc_auc, save_path='roc_curve.png'):
    """Plot and save ROC curve"""
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (AUC = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def find_misclassified_samples(test_dataset, predictions, labels, num_samples=5):
    """Find and save misclassified samples"""
    misclassified_indices = [i for i, (pred, label) in enumerate(zip(predictions, labels)) if pred != label]
    
    # Limit to num_samples
    misclassified_indices = misclassified_indices[:num_samples]
    
    misclassified_samples = []
    for idx in misclassified_indices:
        img_path = test_dataset.images[idx]
        true_label = 'Original' if labels[idx] == 1 else 'Fake'
        pred_label = 'Original' if predictions[idx] == 1 else 'Fake'
        
        misclassified_samples.append({
            'image_path': img_path,
            'true_label': true_label,
            'predicted_label': pred_label
        })
    
    return misclassified_samples

def main():
    parser = argparse.ArgumentParser(description='Evaluate document authenticity detection model')
    parser.add_argument('--model-path', type=str, required=True, help='Path to trained model')
    parser.add_argument('--data-path', type=str, default='data/processed/test', help='Path to test data')
    parser.add_argument('--batch-size', type=int, default=32, help='Batch size')
    
    args = parser.parse_args()
    
    # Set device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f'Using device: {device}')
    
    # Load model
    checkpoint = torch.load(args.model_path, map_location=device)
    model_architecture = checkpoint.get('model_architecture', 'efficientnet')
    
    model = DocumentClassifier(num_classes=2, model_name=model_architecture).to(device)
    model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    
    print(f'Loaded model: {model_architecture}')
    
    # Data transforms
    test_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    # Create dataset and dataloader
    test_dataset = DocumentDataset(root_dir=args.data_path, transform=test_transform)
    test_loader = DataLoader(test_dataset, batch_size=args.batch_size, shuffle=False)
    
    print(f'Test samples: {len(test_dataset)}')
    
    # Evaluate model
    print('Evaluating model...')
    metrics, predictions, probabilities, labels, fpr, tpr = evaluate_model(model, test_loader, device)
    
    # Print metrics
    print('\n=== Evaluation Metrics ===')
    print(f'Accuracy:  {metrics["accuracy"]:.4f}')
    print(f'Precision: {metrics["precision"]:.4f}')
    print(f'Recall:    {metrics["recall"]:.4f}')
    print(f'F1-Score:  {metrics["f1_score"]:.4f}')
    print(f'ROC AUC:   {metrics["roc_auc"]:.4f}')
    
    print('\nConfusion Matrix:')
    print(np.array(metrics["confusion_matrix"]))
    
    # Plot and save visualizations
    os.makedirs('results', exist_ok=True)
    
    plot_confusion_matrix(
        np.array(metrics["confusion_matrix"]), 
        save_path='results/confusion_matrix.png'
    )
    
    plot_roc_curve(
        fpr, tpr, metrics["roc_auc"],
        save_path='results/roc_curve.png'
    )
    
    # Find misclassified samples
    misclassified = find_misclassified_samples(test_dataset, predictions, labels)
    print(f'\nMisclassified samples: {len(misclassified)}')
    for sample in misclassified[:3]:  # Show first 3
        print(f"  True: {sample['true_label']}, Predicted: {sample['predicted_label']}")
        print(f"  Path: {sample['image_path']}")
    
    # Save metrics
    metrics_path = 'results/evaluation_metrics.json'
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f'\nMetrics saved to {metrics_path}')
    print(f'Confusion matrix saved to results/confusion_matrix.png')
    print(f'ROC curve saved to results/roc_curve.png')

if __name__ == '__main__':
    main()