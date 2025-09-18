# Subjects Review

This was a capstone project for COMP30022 created over a 12-week period

Subjects Review is a personal item registry tool that provides a platform not only for storage of University of Melbourne subject experiences and reviews, but for the sharing of them with other University of Melbourne students.

## The Project

This project develops a forensic tool to detect and analyse deepfake and synthetic media. The system supports both images and videos, providing automated preprocessing, anomaly detection, and metadata inspection. Results are presented with clear visualisations such as heatmaps and frame comparisons, along with detailed forensic reports. Designed for investigators and analysts, the tool offers a simple web interface, offline usability, and extensible architecture to support future integration of new models and methods.

## The Team

Baojun Liu : frontend lead

Ruidong Zhang : scrum master

YuchengWang : database

Yuzhao Ouyang :  backend

Xiyu Guan : Product owner

## Technologies

- Local ResNet50 Model
- FastAPI
- PyTorch
- OpenCV
- Ngrok
- Tailwind CSS
- daisyUI

## DeepForensics

Local deepfake detection using ResNet50 machine learning model for secure offline operation.

## Quick Start

1. Install dependencies:
```powershell
python -m venv .venv
pip install -r requirements.txt
.\.venv\Scripts\Activate.ps1
```

2. Test your model:
```bash
python test_model.py
```

3. Start server:
```bash
python start_local_model.py
```

### UI Development

For updating UI, remember to run:
```bash
npm run build
``` 
to compile the latest `app-compiled.css`

## Model Configuration

The system uses a local ResNet50 model for secure offline deepfake detection:

- **Model File**: `deepfake_resnet50.pth`
- **Architecture**: ResNet50 with 2-class output (authentic/fake)
- **Operation**: Completely offline, no internet connection required

## API Endpoints

- `GET /` - Web interface
- `POST /detect` - Upload and detect deepfakes
- `GET /health` - Health check
- `GET /docs` - API documentation
