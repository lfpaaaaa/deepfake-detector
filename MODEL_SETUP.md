# Model Setup Guide

This guide explains how to obtain and configure the required model files for the Deepfake Detection System.

## Required Model Files

The system requires the following model files to function:

### 1. TruFor Model (Primary - Recommended)
- **File**: `trufor.pth.tar`
- **Size**: ~500MB
- **Source**: [TruFor Official Repository](https://github.com/grip-unina/TruFor)
- **Features**: Pixel-level localization, confidence maps, Noiseprint++ analysis
- **Download**: Run `python download_models.py` and select option 2

### 2. ResNet50 Model (Alternative)
- **File**: `deepfake_resnet50.pth`
- **Size**: ~100MB
- **Source**: Local training or provided by team
- **Features**: Fast binary classification
- **Download**: Run `python download_models.py` and select option 3

### 3. ResNet18 Model (Lightweight)
- **File**: `deepfake_resnet18.pth`
- **Size**: ~50MB
- **Source**: Local training or provided by team
- **Features**: Lightweight binary classification
- **Download**: Run `python download_models.py` and select option 3

## Setup Methods

### Method 1: Automatic Download (Recommended)
```bash
# Install required packages
pip install requests tqdm

# Run the download script
python download_models.py
```

### Method 2: Manual Download
1. Download the model files from the sources above
2. Place them in the project root directory
3. Ensure the files are named exactly as specified

### Method 3: Team Sharing
If you have access to the model files from team members:

1. **Via Cloud Storage** (Google Drive, Dropbox, etc.):
   - Download the model files
   - Place them in the project root directory

2. **Via Git LFS** (if enabled):
   ```bash
   git lfs pull
   ```

3. **Via USB/External Drive**:
   - Copy the model files to the project root directory

## File Structure
After setup, your project should look like this:
```
deepfake-detector/
├── trufor.pth.tar          # TruFor model weights
├── deepfake_resnet50.pth   # ResNet50 model weights
├── deepfake_resnet18.pth   # ResNet18 model weights
├── app/
├── requirements.txt
└── ...
```

## Verification
To verify that the models are correctly set up:

```bash
# Test the models
python test_model.py

# Start the server
python start_trufor.py
```

## Troubleshooting

### Issue: Model file not found
**Solution**: Ensure the model files are in the project root directory with the exact names specified.

### Issue: Download fails
**Solution**: 
1. Check your internet connection
2. Try downloading manually from the source
3. Contact team members for the files

### Issue: Model loading errors
**Solution**:
1. Verify the file integrity
2. Check that the file is not corrupted
3. Ensure you have the correct model version

## File Sizes
- `trufor.pth.tar`: ~500MB
- `deepfake_resnet50.pth`: ~100MB
- `deepfake_resnet18.pth`: ~50MB

**Total**: ~650MB for all models

## Notes
- Model files are large and may take time to download
- Ensure you have sufficient disk space
- The TruFor model is the primary model and is recommended for best results
- ResNet models are alternatives for faster processing or limited resources
