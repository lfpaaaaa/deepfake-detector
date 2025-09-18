
# Local ResNet50 Model for Deepfake Detection

## Configuration

This system uses only local ResNet50 model for secure offline deepfake detection. No internet connection required.

### 1. Install Dependencies

First install the required Python packages:

```bash
pip install -r requirements.txt
```

### 2. Model Configuration

The system automatically uses the local ResNet50 model. Optionally, you can set the model path:

```env
# Model file path (optional, defaults to deepfake_resnet50.pth)
MODEL_PATH=deepfake_resnet50.pth
```

### 3. Start Service

```bash
python -m app.main
```

Or using uvicorn:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Features

### Image Detection
- Supports JPEG and PNG formats
- Automatic image preprocessing (resize, normalization)
- Returns authentic/fake probability and confidence

### Video Detection
- Supports MP4 and MOV formats
- Smart frame sampling (every 30 frames or at least 5 frames)
- Aggregates multi-frame prediction results

### Response Format

```json
{
    "request_id": "local_filename_hash",
    "media_type": "image",
    "status": "FAKE|AUTHENTIC|UNCERTAIN",
    "score": 0.85,
    "score_scale": "0-1",
    "models": ["ResNet50"],
    "reasons": ["High probability of manipulation detected"],
    "vendor_raw": {
        "model_type": "ResNet50",
        "fake_probability": 0.85,
        "authentic_probability": 0.15,
        "prediction": 1,
        "confidence": 0.85,
        "device": "cuda:0"
    }
}
```

## Model Requirements

- Model file should be in PyTorch format (.pth)
- Model architecture should be based on ResNet50
- Output layer should be a 2-class classifier (authentic/fake)
- Model should be trained and have saved weights

## Performance Optimization

- Automatically detects and uses GPU (if available)
- Smart sampling for video processing to reduce computation
- Supports batch processing of multiple files

## Troubleshooting

1. **Model loading failed**: Check model file path and format
2. **CUDA errors**: Ensure correct PyTorch and CUDA versions are installed
3. **Out of memory**: Try using CPU mode or processing smaller files
4. **Dependency issues**: Ensure all packages in requirements.txt are properly installed
