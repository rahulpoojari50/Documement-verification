import os
import cv2
import numpy as np
import pandas as pd
import shutil
from sklearn.model_selection import train_test_split
from collections import defaultdict
import albumentations as A
import random
from PIL import Image
import argparse

# Set random seeds for reproducibility
random.seed(42)
np.random.seed(42)

def create_directories():
    """Create necessary directories for the project"""
    dirs = [
        'data/raw',
        'data/processed/train/original',
        'data/processed/train/fake',
        'data/processed/val/original',
        'data/processed/val/fake',
        'data/processed/test/original',
        'data/processed/test/fake',
        'models'
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        
    # Create subdirectories for different document types
    doc_types = ['aadhar', 'pan', 'dl']
    for doc_type in doc_types:
        os.makedirs(f'data/raw/fake_{doc_type}', exist_ok=True)
        os.makedirs(f'data/raw/original_{doc_type}', exist_ok=True)

def is_image_corrupted(image_path):
    """Check if an image is corrupted"""
    try:
        img = cv2.imread(image_path)
        if img is None:
            return True
        # Try to decode the image
        img_array = np.fromfile(image_path, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        if img is None:
            return True
        return False
    except Exception:
        return True

def get_dataset_stats(raw_data_path='data/raw'):
    """Get statistics about the dataset"""
    stats = defaultdict(int)
    corrupted = []
    
    print("Analyzing dataset...")
    
    for root, dirs, files in os.walk(raw_data_path):
        if files:
            class_name = os.path.basename(root)
            valid_images = 0
            
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    file_path = os.path.join(root, file)
                    if not is_image_corrupted(file_path):
                        valid_images += 1
                    else:
                        corrupted.append(file_path)
            
            stats[class_name] = valid_images
            print(f"{class_name}: {valid_images} valid images")
    
    print(f"\nTotal corrupted images found: {len(corrupted)}")
    if corrupted:
        print("Corrupted files:")
        for file in corrupted[:10]:  # Show first 10
            print(f"  {file}")
    
    return dict(stats), corrupted

def resize_and_save_image(src_path, dst_path, size=(512, 512)):
    """Resize image and save to destination"""
    try:
        img = cv2.imread(src_path)
        if img is None:
            return False
        
        # Resize image
        resized_img = cv2.resize(img, size)
        
        # Save resized image
        cv2.imwrite(dst_path, resized_img)
        return True
    except Exception as e:
        print(f"Error processing {src_path}: {str(e)}")
        return False

def augment_image(image_path, output_dir, num_augmentations=3):
    """Apply augmentations to an image"""
    try:
        # Read image
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Define augmentation pipeline
        transform = A.Compose([
            A.Rotate(limit=30, p=0.5),
            A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5),
            A.GaussNoise(var_limit=(10.0, 50.0), p=0.3),
            A.Blur(blur_limit=3, p=0.3),
            A.RandomCrop(height=480, width=480, p=0.4),
        ])
        
        # Apply augmentations
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        for i in range(num_augmentations):
            augmented = transform(image=image)
            aug_image = augmented['image']
            
            # Convert back to BGR for OpenCV
            aug_image = cv2.cvtColor(aug_image, cv2.COLOR_RGB2BGR)
            
            # Save augmented image
            aug_filename = f"{base_name}_aug_{i}.jpg"
            aug_path = os.path.join(output_dir, aug_filename)
            cv2.imwrite(aug_path, aug_image)
            
        return True
    except Exception as e:
        print(f"Error augmenting {image_path}: {str(e)}")
        return False

def prepare_dataset(train_split=0.7, val_split=0.15, test_split=0.15, augment=True):
    """Prepare the dataset with train/val/test splits"""
    print("Preparing dataset...")
    
    # Get all valid images
    image_paths = []
    labels = []
    
    raw_data_path = 'data/raw'
    for root, dirs, files in os.walk(raw_data_path):
        if files:
            class_type = 'fake' if 'fake_' in root else 'original'
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    file_path = os.path.join(root, file)
                    if not is_image_corrupted(file_path):
                        image_paths.append(file_path)
                        labels.append(class_type)
    
    # Create DataFrame
    df = pd.DataFrame({'image_path': image_paths, 'label': labels})
    
    # Split dataset
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        df['image_path'], df['label'], 
        test_size=test_split, 
        random_state=42, 
        stratify=df['label']
    )
    
    val_ratio = val_split / (train_split + val_split)
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val,
        test_size=val_ratio,
        random_state=42,
        stratify=y_train_val
    )
    
    # Process each split
    splits = [
        (X_train, y_train, 'train'),
        (X_val, y_val, 'val'),
        (X_test, y_test, 'test')
    ]
    
    # Process images for each split
    for X, y, split_name in splits:
        print(f"Processing {split_name} split...")
        
        for img_path, label in zip(X, y):
            # Destination path
            filename = os.path.basename(img_path)
            dst_dir = f'data/processed/{split_name}/{label}'
            dst_path = os.path.join(dst_dir, filename)
            
            # Resize and save original image
            resize_and_save_image(img_path, dst_path)
            
            # Apply augmentations for training set only
            if augment and split_name == 'train':
                augment_image(img_path, dst_dir, num_augmentations=3)
    
    # Print final statistics
    print("\nDataset preparation complete!")
    print_final_stats()

def print_final_stats():
    """Print statistics of the final processed dataset"""
    print("\nFinal Dataset Statistics:")
    splits = ['train', 'val', 'test']
    labels = ['original', 'fake']
    
    for split in splits:
        print(f"\n{split.capitalize()} Split:")
        total = 0
        for label in labels:
            path = f'data/processed/{split}/{label}'
            if os.path.exists(path):
                count = len([f for f in os.listdir(path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
                print(f"  {label}: {count}")
                total += count
        print(f"  Total: {total}")

def main():
    parser = argparse.ArgumentParser(description='Prepare dataset for document authenticity detection')
    parser.add_argument('--no-augment', action='store_true', help='Skip data augmentation')
    args = parser.parse_args()
    
    # Create directories
    create_directories()
    
    # Get initial dataset stats
    stats, corrupted = get_dataset_stats()
    
    # Prepare dataset with splits
    prepare_dataset(augment=not args.no_augment)
    
    print("\nData preparation complete!")
    print("Next steps:")
    print("1. Check the processed images in data/processed/")
    print("2. Run train.py to train the model")

if __name__ == "__main__":
    main()