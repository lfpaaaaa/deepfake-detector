# Deepfake Detection System

![CI Tests](https://github.com/lfpaaaaa/deepfake-detector/actions/workflows/ci.yml/badge.svg)
![Quick Tests](https://github.com/lfpaaaaa/deepfake-detector/actions/workflows/quick-test.yml/badge.svg)
![Version](https://img.shields.io/badge/version-3.1-blue)
![Test Coverage](https://img.shields.io/badge/test_coverage-100%25-success)
![Production](https://img.shields.io/badge/production-ready-brightgreen)

A comprehensive forensic tool for detecting and analyzing deepfake and synthetic media using state-of-the-art AI models.

> **Latest Update (Nov 4, 2025)**: V3.1 released with 9 bug fixes, enhanced security, and fully responsive mobile design. All tests passed with 100% coverage. Production ready! ✅

## The Project

This project develops a forensic tool to detect and analyse deepfake and synthetic media. The system supports both images and videos, providing automated preprocessing, anomaly detection, and metadata inspection. Results are presented with clear visualisations such as heatmaps and frame comparisons, along with detailed forensic reports. Designed for investigators and analysts, the tool offers a simple web interface, offline usability, and extensible architecture to support future integration of new models and methods.

### Key Features

#### 🔐 Security & User Management
- **User Authentication**: JWT token-based secure login system
- **Enhanced Password Policy**: Minimum 8 characters with uppercase, lowercase, and digits
- **User Registration**: Create personal accounts with easy access from login page
- **Session Management**: 24-hour token expiration with automatic validation
- **Protected Endpoints**: All detection features require authentication
- **Token Validation**: Automatic redirect to login on invalid/expired tokens

#### 🤖 AI Detection Models
- **TruFor Integration**: Advanced forensic framework with pixel-level localization
- **DeepfakeBench Integration**: 12 state-of-the-art frame-level detection models
- **Multi-Model Analysis**: Compare results across different detection algorithms
- **Ensemble Predictions**: Aggregate multiple model outputs for higher accuracy

#### 📊 Analysis & Visualization
- **Interactive Timeline**: Real-time threshold adjustment with visual feedback
- **Keyframe Screenshots**: Automatic extraction of suspicious frame segments
- **Heatmap Generation**: Visual localization of manipulated regions (optimized for large images)
- **Confidence Mapping**: Pixel-level confidence scores with proper error handling
- **Dynamic Analysis**: Adjust detection sensitivity on-the-fly
- **Large Image Support**: Backend downsampling prevents browser crashes on high-resolution images

#### 📜 History & Reports
- **Detection History**: Track all your detection jobs with persistent storage
- **Chronological Sorting**: Records sorted newest-first for easy access
- **PDF Reports**: Generate comprehensive analysis reports
- **ZIP Packages**: Download complete results including images and metadata
- **Status Tracking**: Monitor pending, processing, and completed jobs
- **Filter & Search**: Easily find specific detection results
- **Stable Layout**: F12 DevTools won't break table layouts

#### 🎨 Modern Interface
- **Interactive UI**: Modern web interface with unified navigation across all pages
- **Fully Responsive**: Optimized for desktop (1920px+), tablet (768px-1024px), and mobile (< 768px)
- **Adaptive Navigation**: Hamburger menu on devices < 1024px, horizontal menu on larger screens
- **Landscape Support**: Proper centering and menu display on mobile landscape mode
- **Card Layout**: Touch-friendly mobile interface for history viewing
- **Consistent Design**: Unified spacing and styling across all pages
- **Real-time Updates**: Live progress tracking during analysis

#### 🚀 Deployment & Operations
- **Offline Operation**: Complete local processing without internet dependency
- **Docker Support**: One-click deployment with Docker Compose
- **Batch Processing**: Multi-GPU parallel video processing
- **CI/CD Pipeline**: Automated testing and quality checks

## The Team

Baojun Liu : frontend

Ruidong Zhang : scrum master

YuchengWang : database

Yuzhao Ouyang :  backend

Xiyu Guan : Product owner

## Technologies

- **TruFor Model**: State-of-the-art forensic framework for image forgery detection
- **DeepfakeBench Framework**: 12 advanced frame-level detection models
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
- **Download**: [TruFor_weights.zip](https://drive.google.com/drive/folders/117IJoriB7kJB9vWQOuj7_S6lNRSOyZ_A?usp=sharing) (248.8 MB)
- **Official Repository**: [TruFor by GRIP-UNINA](https://github.com/grip-unina/TruFor)
- **Note**: Pre-trained weights provided by original authors, we only integrated the model

### DeepfakeBench Models (12 Frame-Level Detectors)
- **Current Models (V3.0)**: Xception, MesoNet-4, MesoNet-4 Inception, F3Net, EfficientNet-B4, Capsule Net, SRM, RECCE, SPSL, UCF, CNN-AUG, CORE
- **Note**: V2.0 had 13 models including FFD, which was removed in V3.0
- **Location**: `vendors/DeepfakeBench/training/weights/`
- **Download**: [vendors.zip](https://drive.google.com/drive/folders/117IJoriB7kJB9vWQOuj7_S6lNRSOyZ_A?usp=sharing) (1.1 GB - includes DeepfakeBench framework and weights)
- **Official Repository**: [DeepfakeBench by SCLBD](https://github.com/SCLBD/DeepfakeBench)
- **Note**: Pre-trained weights provided by DeepfakeBench project, we only integrated the framework
- **Features**: Frame-by-frame analysis, suspicious segment detection, multi-model comparison
- **Quick Start**: See [QUICK_START.md](QUICK_START.md) or [FRAME_INFERENCE_SETUP.md](FRAME_INFERENCE_SETUP.md)
- **Usage**: `python tools/predict_frames.py --input video.mp4 --model xception`

## Quick Start

### Prerequisites
- Docker Desktop installed ([Download here](https://www.docker.com/get-started/))
- At least 3GB free disk space

### Step-by-Step Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/lfpaaaaa/deepfake-detector.git
cd deepfake-detector
```

**Note**: The cloned repository does **NOT** include model weights (they are in `.gitignore`). You need to download them separately.

#### 2. Download Model Weights

Visit: [Google Drive - Model Weights](https://drive.google.com/drive/folders/117IJoriB7kJB9vWQOuj7_S6lNRSOyZ_A?usp=sharing)

Download these two files:
- `TruFor_weights.zip` (248.8 MB)
- `vendors.zip` (1.1 GB)

#### 3. Extract and Place Files

**Important**: Extract files **inside** the `deepfake-detector` directory.

##### For TruFor (Image Detection):
```bash
# Windows PowerShell:
Expand-Archive -Path "TruFor_weights.zip" -DestinationPath "."
# This creates: trufor.pth.tar in project root

# Linux/Mac:
unzip TruFor_weights.zip
# This creates: trufor.pth.tar in project root
```

##### For DeepfakeBench (Video Detection):
```bash
# Windows PowerShell:
Expand-Archive -Path "vendors.zip" -DestinationPath "."
# This creates: vendors/ folder in project root

# Linux/Mac:
unzip vendors.zip
# This creates: vendors/ folder in project root
```

**Expected Directory Structure After Extraction:**
```
deepfake-detector/
├── trufor.pth.tar              ← TruFor model (249 MB)
├── vendors/                    ← DeepfakeBench framework
│   └── DeepfakeBench/
│       └── training/
│           └── weights/
│               ├── xception_best.pth
│               ├── meso4_best.pth
│               ├── f3net_best.pth
│               └── ... (9 more .pth files)
├── app/
├── configs/
├── docker-compose.yml
├── Dockerfile
└── ...
```

**Verify Installation:**
```bash
# Check TruFor weight exists
ls -lh trufor.pth.tar
# Should show: ~249 MB

# Check DeepfakeBench weights exist (Windows)
dir vendors\DeepfakeBench\training\weights\*.pth
# Should show: 12 .pth files

# Check DeepfakeBench weights exist (Linux/Mac)
ls vendors/DeepfakeBench/training/weights/*.pth | wc -l
# Should show: 12
```

#### 4. Start Docker Container

```bash
# Build and start the container
docker compose up -d --build
```

**What this does:**
- Builds Docker image with all dependencies
- Copies model weights into the container
- Starts FastAPI server on port 8000
- Runs in background (`-d` flag)

**Wait for startup** (~30-60 seconds for first time):
```bash
# Check if container is running
docker compose ps

# View logs
docker compose logs -f

# Look for: "Application startup complete"
```

#### 5. Access the Application

Open your browser and visit:

**First-time users:**
1. 📝 **Register**: http://localhost:8000/web/register.html
   - Create your account
2. 🔐 **Login**: http://localhost:8000/web/login.html
   - Login with your credentials

**After login:**
- 🏠 **Main Page**: http://localhost:8000/web/index_main.html (Image detection)
- 🎬 **DeepfakeBench**: http://localhost:8000/web/deepfakebench.html (Video detection)
- 📜 **History**: http://localhost:8000/web/history.html (View past detections)

#### 6. Stop the Container

```bash
# Stop the container
docker compose down

# Stop and remove all data
docker compose down -v
```

### Troubleshooting

**Problem: "Model not found" error**
- ✅ Make sure `trufor.pth.tar` is in project root
- ✅ Make sure `vendors/` folder exists with 12 .pth files
- ✅ Rebuild Docker: `docker compose up -d --build`

**Problem: Port 8000 already in use**
```bash
# Windows: Find and kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/Mac: Find and kill process
lsof -ti:8000 | xargs kill -9
```

**Problem: Docker build fails**
- ✅ Make sure Docker Desktop is running
- ✅ Check disk space (need 3GB+)
- ✅ Try: `docker system prune` to free space

**See detailed guide**: [WEIGHTS_DOWNLOAD_GUIDE.md](WEIGHTS_DOWNLOAD_GUIDE.md)

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

See [MODEL_SETUP.md](docs/MODEL_SETUP.md) for detailed setup instructions and [TRUFOR_TECHNICAL_GUIDE.md](docs/TRUFOR_TECHNICAL_GUIDE.md) for technical implementation details.

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

### 📖 Getting Started
- **[QUICK_START.md](QUICK_START.md)** - Quick start guide
- **[FRAME_INFERENCE_SETUP.md](FRAME_INFERENCE_SETUP.md)** - Frame-level detection setup
- **[BATCH_PROCESSING_GUIDE.md](BATCH_PROCESSING_GUIDE.md)** - Batch processing guide

### 🏗️ Architecture
- **[V3 Domain Model](docs/architecture/v3_domain_model_diagram.md)** - V3 system architecture and components
- **[V3 Sequence Diagram](docs/architecture/v3_sequence_diagram.md)** - V3 interaction flows
- **[V2 Domain Model](docs/architecture/v2_domain_model_diagram.md)** - V2 architecture (legacy)
- **[V2 Sequence Diagram](docs/architecture/v2_sequence_diagram.md)** - V2 flows (legacy)

### 🤖 Models & Setup
- **[MODEL_SETUP.md](docs/MODEL_SETUP.md)** - Model setup instructions
- **[TRUFOR_TECHNICAL_GUIDE.md](docs/TRUFOR_TECHNICAL_GUIDE.md)** - TruFor technical details
- **[WEIGHTS_DOWNLOAD_GUIDE.md](WEIGHTS_DOWNLOAD_GUIDE.md)** - Model weights download guide

### 📱 Features & UI
- **[UI_FEATURES.md](UI_FEATURES.md)** - User interface features documentation
- **[UPGRADE_SUMMARY_V2.md](UPGRADE_SUMMARY_V2.md)** - V2.0 upgrade summary
- **[QUICK_REFERENCE_V2.md](QUICK_REFERENCE_V2.md)** - V2.0 quick reference

### 🔄 CI/CD & Testing
- **[CI_SETUP.md](CI_SETUP.md)** - Continuous integration setup guide
- **[tests/README.md](tests/README.md)** - Testing documentation
- **[Test Plans](docs/testing/test_plans/)** - Detailed test cycle plans
- **[Test Reports](docs/testing/test_reports/)** - Complete test execution reports

## Quality Assurance

### Test Coverage (Cycle 3 - Nov 4, 2025)
- ✅ **Bug Fix Verification**: 5/5 (100%)
- ✅ **Regression Testing**: 6/6 (100%)
- ✅ **Overall Pass Rate**: 12/12 (100%)
- ✅ **New Bugs Found**: 4 (all fixed during testing)
- ✅ **Production Status**: Ready for deployment

### Critical Bugs Fixed
1. **BUG-007** (🔴 Critical): Large image browser crashes - Fixed with backend downsampling
2. **BUG-009** (🟡 Medium): NaN% confidence display - Fixed with validation checks
3. **BUG-010** (🔴 Critical): Invalid token handling - Fixed with client-side validation
4. **BUG-011** (🟢 Low): F12 DevTools layout issues - Fixed with CSS adjustments
5. **BUG-012** (🟡 Medium): Missing registration link - Fixed with UX improvement
6. **BUG-013** (🟢 Low): Navigation spacing inconsistency - Fixed with unified CSS
7. **BUG-014** (🟡 Medium): History sorting disorder - Fixed with timestamp sorting
8. **BUG-015** (🟡 Medium): Responsive layout issues - Fixed with breakpoint adjustments

### Enhancement
- **ENHANCEMENT-005**: Enhanced password policy (min 8 chars, uppercase, lowercase, digit)

### Code Quality
- ✅ Removed 8 unused/redundant code items
- ✅ All imports optimized
- ✅ CSS duplicates eliminated
- ✅ Code reviewed and cleaned

**Test Documentation**:
- 📋 [Cycle 3 Test Plan](docs/testing/test_plans/cycle_3_bugfix_verification.md)
- 📊 [Cycle 3 Test Report](docs/testing/test_reports/cycle_3_report.md)

## Version History

| Version | Date | Key Features |
|---------|------|--------------|
| V1.0 | Initial | Basic ResNet detection |
| V2.0 | Oct 2025 | TruFor integration, Enhanced UI, Modal dialogs |
| V3.0 | Oct 2025 | Authentication, History, DeepfakeBench (12 models), Mobile UI, CI/CD |
| **V3.1** | **Nov 2025** | **Bug fixes, Enhanced security, Responsive design, 100% test coverage** |

### V3.0 Highlights (Oct 2025)
- 🔐 Complete JWT authentication system
- 📜 Detection history with PDF/ZIP reports
- 🎬 12 DeepfakeBench models for video analysis
- 📱 Mobile-responsive interface
- 🔄 CI/CD pipeline with automated testing

### V3.1 Highlights (Nov 2025) - Current Release
- 🐛 **Critical Bug Fixes**: Large image crashes, NaN displays, token validation
- 🔒 **Enhanced Security**: Stronger password policy (8+ chars, mixed case, digits)
- 📱 **Responsive Design**: Fixed mobile layout issues (portrait & landscape)
- 📊 **History Improvements**: Chronological sorting, registration link accessibility
- 🎨 **UI Consistency**: Unified navigation bar spacing across all pages
- ✅ **Quality Assurance**: 100% test coverage, all 9 bugs resolved
- 🧹 **Code Quality**: Removed 8 unused/redundant code items
- 📐 **Mobile Optimization**: Breakpoint adjusted to 1024px for better tablet/phone experience

**What's Fixed in V3.1**:
- ✅ Large images (>1MB) no longer crash the browser
- ✅ Corrupted files show proper error messages instead of "NaN%"
- ✅ Invalid tokens automatically redirect to login page
- ✅ History records sorted newest-first for better usability
- ✅ Mobile devices (landscape mode) display correct navigation menu
- ✅ All pages have consistent visual appearance

## License and Attribution

### Our Project
This project is for educational and research purposes.

### Integrated Models

**We integrated but did NOT train the following models:**

#### TruFor Model
- **Developed by**: GRIP-UNINA (University of Naples Federico II)
- **Repository**: https://github.com/grip-unina/TruFor
- **Paper**: [TruFor: Leveraging All-Round Clues for Trustworthy Image Forgery Detection](https://arxiv.org/abs/2212.10957)
- **License**: Check original repository
- **Our Role**: Integration only

#### DeepfakeBench Models
- **Developed by**: SCLBD (Shenzhen Campus of Learning and Big Data)
- **Repository**: https://github.com/SCLBD/DeepfakeBench
- **Paper**: [DeepfakeBench: A Comprehensive Benchmark](https://arxiv.org/abs/2307.01426)
- **License**: Check original repository
- **Our Role**: Integration only

**All model weights are provided by the original authors. We only integrated these models into our detection system.**

### Citations

If you use this system in research, please cite the original model papers:

**TruFor:**
```bibtex
@article{guillaro2023trufor,
  title={TruFor: Leveraging All-Round Clues for Trustworthy Image Forgery Detection and Localization},
  author={Guillaro, Fabrizio and Cozzolino, Davide and Sud, Avneesh and Dufour, Nicholas and Verdoliva, Luisa},
  journal={arXiv preprint arXiv:2212.10957},
  year={2023}
}
```

**DeepfakeBench:**
```bibtex
@article{yan2023deepfakebench,
  title={DeepfakeBench: A Comprehensive Benchmark of Deep Learning Methods for Deepfake Detection},
  author={Yan, Zhiyuan and Zhang, Yong and Fan, Yanbo and Wu, Baoyuan},
  journal={arXiv preprint arXiv:2307.01426},
  year={2023}
}
```

---

**Current Version**: 3.1 (Stable)  
**Last Updated**: November 4, 2025  
**Test Status**: ✅ All tests passed - Production ready  
**Maintained by**: [Xiyu Guan](mailto:xiyug@student.unimelb.edu.au)
