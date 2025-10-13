# Deepfake Detection System

A comprehensive forensic tool for detecting and analyzing deepfake and synthetic media using state-of-the-art AI models.

## The Project

This project develops a forensic tool to detect and analyse deepfake and synthetic media. The system supports both images and videos, providing automated preprocessing, anomaly detection, and metadata inspection. Results are presented with clear visualisations such as heatmaps and frame comparisons, along with detailed forensic reports. Designed for investigators and analysts, the tool offers a simple web interface, offline usability, and extensible architecture to support future integration of new models and methods.

### Key Features

- **TruFor Integration**: Advanced forensic framework with pixel-level localization
- **Dual Model Support**: Both ResNet50 and TruFor models available
- **Real-time Analysis**: Fast processing with confidence-weighted pooling
- **Interactive UI**: Modern web interface with drag-and-drop support
- **Offline Operation**: Complete local processing without internet dependency

## The Team

Baojun Liu : frontend

Ruidong Zhang : scrum master

YuchengWang : database

Yuzhao Ouyang :  backend

Xiyu Guan : Product owner

## Technologies

- **TruFor Model**: State-of-the-art forensic framework for image forgery detection
- **ResNet50 Model**: Local deepfake detection for secure offline operation
- **FastAPI**: Modern Python web framework for APIs
- **PyTorch**: Deep learning framework
- **OpenCV**: Computer vision library
- **Tailwind CSS**: Utility-first CSS framework
- **daisyUI**: Component library for Tailwind CSS

## Models

### TruFor Model
- **Architecture**: Transformer-based fusion with dual encoders
- **Features**: Pixel-level localization, confidence mapping, Noiseprint++ analysis
- **Output**: Anomaly maps, confidence maps, integrity scores
- **File**: `trufor.pth.tar`

### ResNet50 Model
- **Architecture**: ResNet50 with 2-class output (authentic/fake)
- **Features**: Fast binary classification
- **Output**: Detection confidence scores
- **File**: `deepfake_resnet50.pth`

## Quick Start

1. Install dependencies:
```powershell
python -m venv .venv
pip install -r requirements.txt
.\.venv\Scripts\Activate.ps1
```

2. **Download model files** (Required):
```bash
# Automatic download (recommended)
python models\download_models.py

# Or get from team members (see MODEL_SETUP.md)
```

3. Test your model:
```bash
python scripts\test_model.py
```

4. Start server with TruFor model (recommended):
```bash
python scripts\start_trufor.py
```

Or start with ResNet50 model:
```bash
python scripts\start_local_model.py
```

### 📁 Model Files Required
- `trufor.pth.tar` (~500MB) - Primary TruFor model
- `deepfake_resnet50.pth` (~100MB) - ResNet50 alternative
- `deepfake_resnet18.pth` (~50MB) - ResNet18 lightweight

See [MODEL_SETUP.md](MODEL_SETUP.md) for detailed setup instructions and [TRUFOR_TECHNICAL_GUIDE.md](TRUFOR_TECHNICAL_GUIDE.md) for technical implementation details.

### UI Development

For updating UI, remember to run:
```bash
npm run build
``` 
to compile the latest `app-compiled.css`

## Model Configuration

The system supports two models for deepfake detection:

### TruFor Model (Default)
- **Model File**: `trufor.pth.tar`
- **Architecture**: Transformer-based fusion with dual encoders
- **Features**: Pixel-level localization, confidence mapping, Noiseprint++ analysis
- **Operation**: Completely offline, no internet connection required

### ResNet50 Model (Alternative)
- **Model File**: `deepfake_resnet50.pth`
- **Architecture**: ResNet50 with 2-class output (authentic/fake)
- **Features**: Fast binary classification
- **Operation**: Completely offline, no internet connection required

## API Endpoints

- `GET /` - Web interface
- `POST /detect` - Upload and detect deepfakes
- `GET /health` - Health check
- `GET /docs` - API documentation
