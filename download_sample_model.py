"""
Download a sample model for document verification
This script creates a simple model for testing purposes
"""

import tensorflow as tf
from tensorflow.keras import layers, models
import os

def create_sample_model():
    """Create a simple CNN model for document verification"""
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])
    
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    
    return model

def save_sample_model(model_path="document_verifier.h5"):
    """Save a sample model to disk"""
    # Create the model
    model = create_sample_model()
    
    # Save the model
    model.save(model_path)
    print(f"Sample model saved to {model_path}")
    
    # Print model summary
    print("\nModel Architecture:")
    model.summary()
    
    return model_path

if __name__ == "__main__":
    # Create and save the sample model
    model_path = save_sample_model()
    print(f"\n✅ Sample model created and saved as '{model_path}'")
    print("You can now use this model for testing the verification pipeline.")