#!/usr/bin/env python3
"""
Training script for PAN card authenticity classifier
"""

import os
import sys
import cv2
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle
from pathlib import Path
import glob

def extract_features(image_path):
    """
    Extract features from PAN card image for classification
    
    Args:
        image_path (str): Path to the PAN card image
        
    Returns:
        np.array: Feature vector
    """
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        # Return zeros for failed image loading
        return np.zeros(20)  # Increased feature size
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Feature 1-3: Basic image statistics
    mean_intensity = np.mean(gray)
    std_intensity = np.std(gray)
    hist_entropy = -np.sum((np.histogram(gray, bins=256)[0] / gray.size) * 
                          np.log2(np.histogram(gray, bins=256)[0] / gray.size + 1e-10))
    
    # Feature 4-5: Edge detection statistics
    edges = cv2.Canny(gray, 50, 150)
    edge_density = np.sum(edges > 0) / edges.size
    edge_mean = np.mean(edges[edges > 0]) if np.any(edges > 0) else 0
    
    # Feature 6-7: Texture features (Local Binary Pattern approximation)
    # Simple texture measure using Laplacian variance
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    # Feature 8: Color histogram uniformity (for colored images)
    if len(image.shape) == 3:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hue_hist = cv2.calcHist([hsv], [0], None, [50], [0, 180])
        hue_uniformity = np.sum((hue_hist / np.sum(hue_hist)) ** 2)
    else:
        hue_uniformity = 0
    
    # Feature 9-10: Image dimensions
    height, width = gray.shape
    aspect_ratio = width / height
    
    # Additional features for better discrimination
    # Feature 11-12: Gradient features
    grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
    grad_magnitude = np.sqrt(grad_x**2 + grad_y**2)
    mean_gradient = np.mean(grad_magnitude)
    std_gradient = np.std(grad_magnitude)
    
    # Feature 13-14: Frequency domain features
    f = np.fft.fft2(gray)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20 * np.log(np.abs(fshift) + 1)
    freq_mean = np.mean(magnitude_spectrum)
    freq_std = np.std(magnitude_spectrum)
    
    # Feature 15-16: Corner detection features
    corners = cv2.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.01, minDistance=10)
    corner_count = len(corners) if corners is not None else 0
    corner_density = corner_count / (gray.shape[0] * gray.shape[1])
    
    # Feature 17-18: Blob detection features
    # Simple blob detection using contours
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blob_count = len(contours)
    avg_blob_area = np.mean([cv2.contourArea(cnt) for cnt in contours]) if contours else 0
    
    # Feature 19-20: Structural similarity features
    # Measure of structuredness in the image
    structuredness = np.mean(cv2.filter2D(gray, -1, np.array([[-1,-1,-1], [-1,8,-1], [-1,-1,-1]])))
    
    # Return feature vector
    features = np.array([
        mean_intensity,
        std_intensity,
        hist_entropy,
        edge_density,
        edge_mean,
        laplacian_var,
        hue_uniformity,
        width,
        height,
        aspect_ratio,
        mean_gradient,
        std_gradient,
        freq_mean,
        freq_std,
        corner_count,
        corner_density,
        blob_count,
        avg_blob_area,
        structuredness,
        laplacian_var / (std_intensity + 1e-10)  # Normalized texture measure
    ])
    
    return features

def prepare_dataset():
    """
    Prepare dataset for PAN card classification
    
    Returns:
        tuple: (features, labels) where features is np.array and labels is list
    """
    print("Preparing PAN card dataset...")
    
    # Paths to real and fake PAN card images
    real_pan_path = Path("data/raw/original_pan")
    fake_pan_path = Path("data/raw/fake_pan")
    
    features = []
    labels = []  # 1 for real, 0 for fake
    
    # Process real PAN cards
    real_images = list(real_pan_path.glob("*.jpg"))
    print(f"Processing {len(real_images)} real PAN card images...")
    
    for img_path in real_images:
        try:
            feat = extract_features(str(img_path))
            features.append(feat)
            labels.append(1)  # Real PAN
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
    
    # Process fake PAN cards
    fake_images = list(fake_pan_path.glob("*.jpg"))
    print(f"Processing {len(fake_images)} fake PAN card images...")
    
    for img_path in fake_images:
        try:
            feat = extract_features(str(img_path))
            features.append(feat)
            labels.append(0)  # Fake PAN
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
    
    if len(features) == 0:
        raise ValueError("No features extracted. Check image paths.")
    
    # Convert to numpy arrays
    features = np.array(features)
    labels = np.array(labels)
    
    print(f"Dataset prepared: {len(features)} samples, {len(features[0])} features each")
    print(f"Real PAN cards: {np.sum(labels)}, Fake PAN cards: {len(labels) - np.sum(labels)}")
    
    return features, labels

def train_classifier():
    """
    Train the PAN card authenticity classifier
    
    Returns:
        tuple: (classifier, accuracy, classification_report)
    """
    print("Training PAN card authenticity classifier...")
    
    # Prepare dataset
    try:
        features, labels = prepare_dataset()
    except Exception as e:
        print(f"Error preparing dataset: {e}")
        return None, 0, ""
    
    # Split dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        features, labels, test_size=0.2, random_state=42, stratify=labels
    )
    
    # Create and train classifier with improved parameters
    clf = RandomForestClassifier(
        n_estimators=200,  # Increased number of trees
        max_depth=15,      # Limit depth to prevent overfitting
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42
    )
    clf.fit(X_train, y_train)
    
    # Evaluate classifier
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=['Fake', 'Real'])
    
    print(f"Training completed!")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Classification Report:\n{report}")
    
    return clf, accuracy, report

def save_model(classifier, model_path="models/pan_authenticity_classifier.pkl"):
    """
    Save the trained classifier to disk
    
    Args:
        classifier: Trained classifier
        model_path (str): Path to save the model
    """
    # Create models directory if it doesn't exist
    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Save model
    with open(model_path, 'wb') as f:
        pickle.dump(classifier, f)
    
    print(f"Model saved to {model_path}")

def load_model(model_path="models/pan_authenticity_classifier.pkl"):
    """
    Load a trained classifier from disk
    
    Args:
        model_path (str): Path to the saved model
        
    Returns:
        classifier: Loaded classifier or None if failed
    """
    try:
        with open(model_path, 'rb') as f:
            classifier = pickle.load(f)
        print(f"Model loaded from {model_path}")
        return classifier
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def verify_pan_card(image_path, classifier=None):
    """
    Verify if a PAN card is real or fake using the trained classifier
    
    Args:
        image_path (str): Path to the PAN card image
        classifier: Trained classifier (loads default if None)
        
    Returns:
        dict: Verification result
    """
    # Load classifier if not provided
    if classifier is None:
        classifier = load_model()
        if classifier is None:
            return {"error": "Could not load classifier"}
    
    # Extract features
    try:
        features = extract_features(image_path)
        features = features.reshape(1, -1)  # Reshape for prediction
    except Exception as e:
        return {"error": f"Error extracting features: {e}"}
    
    # Make prediction
    try:
        prediction = classifier.predict(features)[0]
        probability = classifier.predict_proba(features)[0]
        
        result = {
            "is_authentic": bool(prediction),
            "confidence": float(max(probability)),
            "prediction": "Real" if prediction else "Fake",
            "probabilities": {
                "fake": float(probability[0]),
                "real": float(probability[1])
            }
        }
        
        return result
    except Exception as e:
        return {"error": f"Error during prediction: {e}"}

def main():
    """
    Main function to train and test the PAN card classifier
    """
    print("PAN Card Authenticity Classifier")
    print("=" * 40)
    
    # Train classifier
    classifier, accuracy, report = train_classifier()
    
    if classifier is None:
        print("Training failed!")
        return
    
    # Save model
    save_model(classifier)
    
    # Test with sample images
    print("\nTesting with sample images...")
    
    # Test with real PAN cards
    real_samples = glob.glob("data/raw/original_pan/*.jpg")[:3]
    fake_samples = glob.glob("data/raw/fake_pan/*.jpg")[:3]
    
    print("\nReal PAN Card Samples:")
    for sample in real_samples:
        result = verify_pan_card(sample, classifier)
        if "error" not in result:
            print(f"  {Path(sample).name}: {result['prediction']} (Confidence: {result['confidence']:.2f})")
        else:
            print(f"  {Path(sample).name}: Error - {result['error']}")
    
    print("\nFake PAN Card Samples:")
    for sample in fake_samples:
        result = verify_pan_card(sample, classifier)
        if "error" not in result:
            print(f"  {Path(sample).name}: {result['prediction']} (Confidence: {result['confidence']:.2f})")
        else:
            print(f"  {Path(sample).name}: Error - {result['error']}")
    
    print("\nClassifier training and testing completed!")

if __name__ == "__main__":
    main()