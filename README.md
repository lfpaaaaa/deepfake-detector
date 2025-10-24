# Deepfake Detection System

A comprehensive forensic tool for detecting and analyzing deepfake and synthetic media using state-of-the-art AI models.

## The Project

This project develops a forensic tool to detect and analyse deepfake and synthetic media. The system supports both images and videos, providing automated preprocessing, anomaly detection, and metadata inspection. Results are presented with clear visualisations such as heatmaps and frame comparisons, along with detailed forensic reports. Designed for investigators and analysts, the tool offers a simple web interface, offline usability, and extensible architecture to support future integration of new models and methods.

### Key Features

- **TruFor Integration**: Advanced forensic framework with pixel-level localization
- **DeepfakeBench Integration**: 13 state-of-the-art frame-level detection models
- **Interactive Timeline**: Real-time threshold adjustment with visual feedback
- **Keyframe Screenshots**: Automatic extraction of suspicious frame segments
- **Dynamic Analysis**: Adjust detection sensitivity on-the-fly
- **Interactive UI**: Modern web interface with navigation system
- **Offline Operation**: Complete local processing without internet dependency
- **Batch Processing**: Multi-GPU parallel video processing

## The Team

Baojun Liu : frontend

Ruidong Zhang : scrum master

YuchengWang : database

Yuzhao Ouyang :  backend

Xiyu Guan : Product owner

## Technologies

- **TruFor Model**: State-of-the-art forensic framework for image forgery detection
- **DeepfakeBench Framework**: 13 advanced frame-level detection models
- **FastAPI**: Modern Python web framework for APIs
- **PyTorch**: Deep learning framework for model inference
- **OpenCV**: Computer vision library for video processing
- **Tailwind CSS + daisyUI**: Modern UI framework

## Models

### TruFor Model
- **Architecture**: Transformer-based fusion with dual encoders
- **Features**: Pixel-level localization, confidence mapping, Noiseprint++ analysis
- **Output**: Anomaly maps, confidence maps, integrity scores
- **File**: `trufor.pth.tar`

### DeepfakeBench Models (13 Frame-Level Detectors)
- **Models**: Xception, MesoNet-4, F3Net, EfficientNet-B4, Capsule Net, SRM, RECCE, SPSL, FFD, UCF, CNN-AUG, CORE
- **Location**: `vendors/DeepfakeBench/training/weights/`
- **Features**: Frame-by-frame analysis, suspicious segment detection, multi-model comparison
- **Quick Start**: See [QUICK_START.md](QUICK_START.md) or [FRAME_INFERENCE_SETUP.md](FRAME_INFERENCE_SETUP.md)
- **Usage**: `python tools/predict_frames.py --input video.mp4 --model xception`

## Quick Start

<!-- 1. Install dependencies:
```powershell
python -m venv .venv
pip install -r configs/requirements.txt
.\.venv\Scripts\Activate.ps1
```

2. **Download model files** (Required):
```bash
# Download TruFor model
python models/download_models.py

# Or get from team members (see MODEL_SETUP.md)
```

3. Start the server:
```bash
# Start with TruFor model
python scripts/start_trufor.py

# Or start with all features
python app/main.py
``` -->

1. Install docker desktop
[Download here](https://www.docker.com/get-started/)

2. Prepare model files *(optional but recommended)*
- Place `trufor.pth.tar` in the project root.
- Put DeepfakeBench weights under `vendors/DeepfakeBench/training/weights/`.

3. One-click deployment
```bash
docker compose up -d --build
```

4. Access the web interface:
- Main page: `http://localhost:8000/web/index_main.html`
- TruFor Detection: `http://localhost:8000/web/index.html`
- DeepfakeBench: `http://localhost:8000/web/deepfakebench.html`

5. **Frame-by-frame analysis** with DeepfakeBench models:
```bash
# Single video analysis with visualization
python tools/predict_frames.py --input video.mp4 --model xception --fps 10 --save-vis

# Batch processing multiple videos
python tools/batch_predict.py --input-dir data/videos --model xception --workers 4 --gpus 0,1

# List available models
python tools/list_models.py

# Aggregate results
python tools/aggregate_runs.py --root runs/image_infer --out summary.csv
```
### Common Commands
- **View logs:** `docker-compose logs -f`
- **Stop services:** `docker-compose down`
- **Restart services:** `docker-compose restart`

**Full documentation:** `DOCKER_README.md`

### 📁 Model Files Required
- `trufor.pth.tar` (~500MB) - Primary TruFor model for image/video forensics
- DeepfakeBench weights (13 files, ~50-200MB each) - Frame-level detectors
  - Location: `vendors/DeepfakeBench/training/weights/`
  - Models: `xception_best.pth`, `meso4_best.pth`, `f3net_best.pth`, etc.

See [MODEL_SETUP.md](MODEL_SETUP.md) for detailed setup instructions and [TRUFOR_TECHNICAL_GUIDE.md](TRUFOR_TECHNICAL_GUIDE.md) for technical implementation details.

For DeepfakeBench frame-level detection:
- **Quick Start**: [QUICK_START.md](QUICK_START.md)
- **Full Documentation**: [FRAME_INFERENCE_SETUP.md](FRAME_INFERENCE_SETUP.md)
- **Batch Processing**: [BATCH_PROCESSING_GUIDE.md](BATCH_PROCESSING_GUIDE.md) 
- **Tool Documentation**: [tools/README.md](tools/README.md)

### UI Development

For updating UI, remember to run:
```bash
npm run build
``` 
to compile the latest `app-compiled.css`

## Detection Methods

### 1. TruFor Detection (Image & Video Forensics)
- **Model**: `trufor.pth.tar`
- **Architecture**: Transformer-based fusion with dual encoders
- **Features**: 
  - Pixel-level localization with heatmaps
  - Confidence mapping
  - Noiseprint++ analysis
  - Both image and video support
- **Use Case**: Detailed forensic analysis with visual evidence

### 2. DeepfakeBench Detection (Video Frame Analysis)
- **Models**: 13 specialized detectors (Xception, F3Net, EfficientNet-B4, etc.)
- **Features**:
  - Frame-by-frame deepfake detection
  - Interactive timeline with threshold slider
  - Automatic keyframe extraction
  - Suspicious segment identification
  - Real-time threshold adjustment
  - Dynamic keyframe generation
- **Use Case**: Video-specific deepfake detection with detailed temporal analysis

Both methods operate completely offline with no internet connection required.

## Web Interface Navigation

The system provides three main interfaces accessible through a unified navigation bar:

1. **Home** (`/web/index_main.html`) - Landing page with method selection
2. **TruFor Detection** (`/web/index.html`) - Image and video forensic analysis
3. **DeepfakeBench** (`/web/deepfakebench.html`) - Frame-level video analysis

### Key Features
- **Unified Navigation**: Easy switching between detection methods
- **Drag & Drop Upload**: Intuitive file upload interface
- **Real-time Progress**: Live analysis progress indicators
- **Interactive Results**: 
  - Timeline visualization with adjustable threshold
  - Keyframe screenshots of suspicious segments
  - Detailed segment analysis
  - Downloadable results

## API Endpoints

### TruFor API
- `POST /detect` - Upload and analyze media
- `GET /health` - Health check

### DeepfakeBench API
- `GET /api/deepfakebench/models` - List available models
- `POST /api/deepfakebench/analyze` - Start video analysis
- `GET /api/deepfakebench/jobs/{job_id}` - Get analysis status
- `POST /api/deepfakebench/jobs/{job_id}/extract-keyframe` - Extract frame at timestamp
- `GET /video/jobs/{job_id}/keyframes/{filename}` - Serve keyframe images

## Project Structure

```
deepfake-detector/
├── app/
│   ├── adapters/           # Model adapters
│   │   ├── trufor_adapter.py
│   │   └── deepfakebench_adapter.py
│   ├── web/                # Web interfaces
│   │   ├── index_main.html      # Landing page
│   │   ├── index.html           # TruFor interface
│   │   └── deepfakebench.html   # DeepfakeBench interface
│   └── main.py             # FastAPI application
├── tools/                  # CLI tools
│   ├── predict_frames.py   # Frame-level inference
│   ├── batch_predict.py    # Batch processing
│   └── aggregate_runs.py   # Result aggregation
├── models/                 # Model weights
│   └── trufor.pth.tar
├── vendors/DeepfakeBench/  # DeepfakeBench framework
│   └── training/weights/   # DeepfakeBench model weights
├── data/jobs/              # Analysis results
└── docs/                   # Documentation
```

## LAN Access Guide

To access the web interface from other devices on your local network (e.g., mobile phones, tablets):

### 1. Find Your Computer's IPv4 Address

**Windows (PowerShell):**
```powershell
ipconfig
# Look for "IPv4 Address" under your active network adapter (e.g., 192.168.1.100)
```

**macOS/Linux:**
```bash
ifconfig
# Look for "inet" address under your active network interface (e.g., en0 or wlan0)
```

### 2. Configure Firewall

**Windows:**
```powershell
# Allow inbound connections on port 8000
New-NetFirewallRule -DisplayName "Deepfake Detector" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow
```

**macOS:**
- System Preferences → Security & Privacy → Firewall → Firewall Options
- Add Python and allow incoming connections

**Linux (ufw):**
```bash
sudo ufw allow 8000/tcp
```

### 3. Start the Server

The server is already configured to accept LAN connections (`host="0.0.0.0"`):

```bash
python scripts/start_trufor.py
```

### 4. Access from Other Devices

On your mobile phone or other device **connected to the same Wi-Fi network**, open your browser and navigate to:

```
http://YOUR_IPV4_ADDRESS:8000/web/index_main.html
```

For example, if your IPv4 is `192.168.1.100`:
```
http://192.168.1.100:8000/web/index_main.html
```

### Available Pages:
- Main page: `http://YOUR_IP:8000/web/index_main.html`
- TruFor Detection: `http://YOUR_IP:8000/web/index.html`
- DeepfakeBench: `http://YOUR_IP:8000/web/deepfakebench.html`

### Troubleshooting:
- ✅ Ensure both devices are on the **same Wi-Fi network**
- ✅ Verify firewall rules allow port 8000
- ✅ Check if the server is running: `http://YOUR_IP:8000/health`
- ✅ Try disabling VPN if enabled

## Documentation

- **[QUICK_START.md](QUICK_START.md)** - Quick start guide
- **[FRAME_INFERENCE_SETUP.md](FRAME_INFERENCE_SETUP.md)** - Frame-level detection setup
- **[BATCH_PROCESSING_GUIDE.md](BATCH_PROCESSING_GUIDE.md)** - Batch processing guide
- **[UPGRADE_SUMMARY_V2.md](UPGRADE_SUMMARY_V2.md)** - V2.0 upgrade summary
- **[MODEL_SETUP.md](docs/MODEL_SETUP.md)** - Model setup instructions
- **[TRUFOR_TECHNICAL_GUIDE.md](docs/TRUFOR_TECHNICAL_GUIDE.md)** - TruFor technical details

## License

This project is for educational and research purposes.
