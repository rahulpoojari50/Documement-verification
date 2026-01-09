# Data Preparation Script

This script prepares the dataset for training the document authenticity detection model.

## Features

1. Validates and analyzes dataset statistics
2. Removes corrupted images
3. Resizes images to a consistent size (512x512)
4. Applies data augmentation for the training set
5. Creates stratified train/validation/test splits (70/15/15)

## Usage

Run the data preparation script:

```bash
python scripts/data_prep.py
```

To skip data augmentation (faster processing):

```bash
python scripts/data_prep.py --no-augment
```

## Expected Directory Structure

The script expects the following directory structure:

```
data/
└── raw/
    ├── fake_aadhar/
    ├── original_aadhar/
    ├── fake_pan/
    ├── original_pan/
    ├── fake_dl/
    └── original_dl/
```

After running, the processed data will be organized as:

```
data/
└── processed/
    ├── train/
    │   ├── fake/
    │   └── original/
    ├── val/
    │   ├── fake/
    │   └── original/
    └── test/
        ├── fake/
        └── original/
```

## Output

The script will output:
1. Dataset statistics (number of valid images per class)
2. Number of corrupted images detected
3. Final dataset statistics after processing