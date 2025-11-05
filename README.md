# 🎭 Deepfake Detector

[![Version](https://img.shields.io/badge/version-3.1-blue.svg)](https://github.com/lfpaaaaa/deepfake-detector)
[![Python](https://img.shields.io/badge/python-3.11+-green.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)
[![Tests](https://img.shields.io/badge/tests-passing-success.svg)](docs/testing/test_reports/cycle_3_report.md)
[![License](https://img.shields.io/badge/license-Educational-orange.svg)](LICENSE)

A production-ready web application for detecting deepfakes in images and videos using state-of-the-art AI models (TruFor + DeepfakeBench).

**🎯 Project Status**: ✅ Production Ready (V3.1 - Nov 4, 2025)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Quick Start](#quick-start)
- [Technologies](#technologies)
- [AI Models](#ai-models)
- [Documentation](#documentation)
- [Version History](#version-history)
- [License](#license-and-attribution)

---

## Overview

The **Deepfake Detector** provides forensic analysts and researchers with powerful tools to identify manipulated media through:

- **TruFor**: Advanced image forgery detection with pixel-level localization
- **DeepfakeBench**: Ensemble of 12 video deepfake detection models

### The Team

- **Baojun Liu** - Frontend Development
- **Ruidong Zhang** - Scrum Master
- **Yucheng Wang** - Database Management
- **Yuzhao Ouyang** - Backend Development
- **Xiyu Guan** - Product Owner, System Architecture, Full-Stack Development

**GitHub**: https://github.com/lfpaaaaa/deepfake-detector  
**Contact**: xiyug@student.unimelb.edu.au

---

## Key Features

### 🔐 Security & User Management
- JWT-based authentication with 24-hour sessions
- Role-based access control (Admin/Analyst)
- Enhanced password policy (8+ chars, uppercase, lowercase, digit)
- Secure token validation and automatic redirects

### 🤖 AI Detection Models
- **TruFor** - Image forgery detection with confidence mapping
- **DeepfakeBench** - 12 specialized video detection models
- Pixel-level anomaly localization
- Multi-model ensemble predictions

### 📊 Analysis & Visualization
- Real-time detection progress indicators
- Confidence heatmaps and score visualizations
- Frame-by-frame video analysis
- Suspicious segment identification

### 📜 History & Reports
- Complete detection history with chronological sorting
- Professional PDF reports with forensic details
- ZIP archives with all analysis artifacts
- Admin can view all users' history

### 🎨 Modern Interface
- Responsive design (desktop, tablet, mobile)
- Drag-and-drop file upload
- Unified navigation across all pages
- Dark/light theme support

### 🚀 Deployment & Operations
- Docker containerization for easy deployment
- Volume mounting for development hot-reload
- CI/CD with GitHub Actions
- Comprehensive test coverage (100% pass rate)

---

## Quick Start

### Prerequisites
- **Docker Desktop** installed ([Download here](https://www.docker.com/get-started/))
- At least **3GB** free disk space
- Internet connection for downloading model weights

### Installation (5 Steps)

#### 1. Clone Repository
```bash
git clone https://github.com/lfpaaaaa/deepfake-detector.git
cd deepfake-detector
```

#### 2. Download Model Weights

**📥 Download from Google Drive**: [Model Weights Folder](https://drive.google.com/drive/folders/117IJoriB7kJB9vWQOuj7_S6lNRSOyZ_A)

Download these two files:
- `TruFor_weights.zip` (248.8 MB) - TruFor model weights
- `vendors.zip` (1.1 GB) - **DeepfakeBench framework + 12 model weights (all included)**

#### 3. Extract Files

**Windows PowerShell**:
```powershell
# Extract to models/ directory
Expand-Archive -Path "TruFor_weights.zip" -DestinationPath "models" -Force
Expand-Archive -Path "vendors.zip" -DestinationPath "models" -Force
```

**Linux/Mac**:
```bash
# Create models directory and extract
mkdir -p models
unzip TruFor_weights.zip -d models
unzip vendors.zip -d models
```

**Verify**:
```bash
# Should exist: models/trufor.pth.tar (~249 MB) and models/vendors/ directory
ls -lh models/trufor.pth.tar

# Should have 12 .pth files
ls models/vendors/DeepfakeBench/training/weights/*.pth | wc -l
```

#### 4. Start Docker
```bash
docker compose up -d --build
```

Wait ~30-60 seconds for first-time startup. Check logs:
```bash
docker compose logs -f
# Look for: "Application startup complete"
```

#### 5. Access Application

Open your browser: **http://localhost:8000/web/index_main.html**

**First-time setup**:
1. Click "Register" to create an account
2. Password must meet policy (8+ chars, uppercase, lowercase, digit)
3. Login and start detecting!

### Stop Docker
```bash
docker compose down
```

### Need Help?

- **Complete Setup Guide**: [docs/guides/WEIGHTS_DOWNLOAD_GUIDE.md](docs/guides/WEIGHTS_DOWNLOAD_GUIDE.md)
- **Troubleshooting**: See guide above or [docs/handover/HANDOVER_DOCUMENT.md](docs/handover/HANDOVER_DOCUMENT.md)

---

## Technologies

| Layer | Stack |
|-------|-------|
| **Backend** | Python 3.11, FastAPI, Uvicorn |
| **Frontend** | HTML5, CSS3, JavaScript (Vanilla), DaisyUI, TailwindCSS |
| **AI/ML** | PyTorch 2.0+, TruFor, DeepfakeBench (12 models) |
| **Auth** | JWT (jose), bcrypt, passlib |
| **Database** | JSON file storage (users, sessions, jobs) |
| **Deployment** | Docker, Docker Compose |
| **CI/CD** | GitHub Actions |
| **Testing** | pytest, FastAPI TestClient |

---

## AI Models

### TruFor (Image Detection)
- **File**: `models/trufor.pth.tar` (~249 MB)
- **Features**: Pixel-level forgery localization, confidence maps, Noiseprint++ analysis
- **Official**: https://github.com/grip-unina/TruFor
- **Paper**: [TruFor: Leveraging All-Round Clues for Trustworthy Image Forgery Detection](https://arxiv.org/abs/2212.10957)

### DeepfakeBench (Video Detection)
- **12 Models**: Xception, EfficientNet-B4, F3Net, MesoNet-4, Capsule, SRM, RECCE, SPSL, UCF, CNN-AUG, CORE, MesoNet-4 Inception
- **Total Size**: ~780 MB
- **Official**: https://github.com/SCLBD/DeepfakeBench
- **Paper**: [DeepfakeBench: A Comprehensive Benchmark](https://arxiv.org/abs/2307.01426)

**Download Link**: https://drive.google.com/drive/folders/117IJoriB7kJB9vWQOuj7_S6lNRSOyZ_A

**⚠️ Important**: We **only integrated** these models. We did **NOT** train them. All credit goes to original authors.

---

## Documentation

### 📖 Getting Started
- **[WEIGHTS_DOWNLOAD_GUIDE.md](docs/guides/WEIGHTS_DOWNLOAD_GUIDE.md)** - Complete model setup guide
- **[HANDOVER_DOCUMENT.md](docs/handover/HANDOVER_DOCUMENT.md)** - Comprehensive project handover

### 🤖 Model Guides
- **[TruFor Technical Guide](docs/guides/TRUFOR_TECHNICAL_GUIDE.md)** - TruFor integration details
- **[Quick Reference V2](docs/guides/QUICK_REFERENCE_V2.md)** - Command cheat sheet

### 🏗️ Architecture & Design
- **[V3 Domain Model](docs/architecture/v3_domain_model_diagram.md)** - System architecture
- **[V3 Sequence Diagram](docs/architecture/v3_sequence_diagram.md)** - Interaction flows
- **[Upgrade Summary V2](docs/guides/UPGRADE_SUMMARY_V2.md)** - V1 → V2 migration

### 🧪 Testing & Quality
- **[Testing README](docs/testing/README.md)** - Testing strategy
- **[Cycle 3 Test Report](docs/testing/test_reports/cycle_3_report.md)** - Latest results (100% pass)
- **[Test Cases](docs/testing/TEST_CASES.md)** - All 28 test scenarios

### 📱 UI Documentation
- **[UI Features](docs/ui/UI_FEATURES.md)** - Frontend features guide
- **[UI Screenshots](docs/ui/)** - 32 screenshots (16 desktop + 16 mobile)

### 🔧 Operations
- **[CI Setup Guide](docs/testing/CI_SETUP.md)** - GitHub Actions configuration
- **[Changelog](docs/handover/CHANGELOG.md)** - Version history details

---

## Version History

| Version | Date | Highlights |
|---------|------|------------|
| **V3.1** 🎉 | **Nov 4, 2025** | **9 bugs fixed, enhanced security, 100% test pass, responsive design** |
| V3.0 | Oct 26, 2025 | Complete testing (109 tests), mobile UI, 12 models, CI/CD |
| V2.0 | Sep 2025 | TruFor + DeepfakeBench integration, JWT auth, PDF reports |
| V1.0 | Initial | Basic detection system |

### V3.1 Highlights (Current Release)

**🐛 Critical Bugs Fixed**:
- ✅ **BUG-007**: Large image crashes (backend downsampling)
- ✅ **BUG-009**: NaN% confidence display (validation checks)
- ✅ **BUG-010**: Invalid token handling (client-side validation)
- ✅ **BUG-011**: F12 DevTools layout issues (CSS fixes)
- ✅ **BUG-012**: Missing registration link (UX improvement)
- ✅ **BUG-013**: Navigation spacing inconsistency (unified CSS)
- ✅ **BUG-014**: History sorting disorder (timestamp sorting)
- ✅ **BUG-015**: Responsive layout issues (breakpoint adjustments)

**🔒 Enhancements**:
- Enhanced password policy (min 8 chars, uppercase, lowercase, digit)

**✅ Quality Assurance**:
- **Test Pass Rate**: 100% (Cycle 3)
- **Tests Run**: 121 (67 automated + 42 manual + 12 verification)
- **Code Quality**: Removed 8 unused items, optimized imports
- **Production Status**: ✅ Ready for deployment

**📋 Full Details**: [Cycle 3 Test Report](docs/testing/test_reports/cycle_3_report.md)

---

## Project Structure

```
deepfake-detector/
├── app/                          # FastAPI application
│   ├── adapters/                 # Model wrappers (TruFor, DeepfakeBench)
│   ├── auth/                     # JWT authentication
│   ├── history/                  # Detection history management
│   ├── reports/                  # PDF/ZIP generation
│   ├── web/                      # Frontend (HTML/CSS/JS)
│   └── main.py                   # API endpoints (1288 lines)
├── docs/                         # Documentation
│   ├── guides/                   # User guides
│   │   ├── WEIGHTS_DOWNLOAD_GUIDE.md
│   │   └── QUICK_REFERENCE_V2.md
│   ├── architecture/             # System design diagrams
│   ├── testing/                  # Test plans and reports
│   ├── ui/                       # UI screenshots and docs
│   ├── guides/                   # User guides & tech docs
│   │   ├── WEIGHTS_DOWNLOAD_GUIDE.md
│   │   ├── TRUFOR_TECHNICAL_GUIDE.md
│   │   ├── UPGRADE_SUMMARY_V2.md
│   │   └── QUICK_REFERENCE_V2.md
│   ├── handover/                 # Project handover
│   │   ├── HANDOVER_DOCUMENT.md
│   │   └── CHANGELOG.md
│   ├── testing/                  # Testing docs
│   │   ├── CI_SETUP.md
│   │   └── ...
├── tests/                        # Automated tests (pytest)
├── tools/                        # CLI detection tools
├── models/                       # Model weights directory (user must download)
│   ├── trufor.pth.tar           # TruFor model weights
│   └── vendors/                 # DeepfakeBench models
│       └── DeepfakeBench/       # 12 detection models
├── docker-compose.yml            # Docker configuration
├── Dockerfile                    # Docker image definition
└── README.md                     # This file
```

---

## API Endpoints

### Authentication
- `POST /register` - Create new user account
- `POST /token` - Login and get JWT token
- `GET /api/auth/me` - Get current user info

### Detection
- `POST /detect` - Analyze image (TruFor)
- `POST /api/deepfakebench/analyze` - Analyze video (DeepfakeBench)
- `GET /api/deepfakebench/jobs/{job_id}` - Check analysis status

### History & Reports
- `GET /api/history` - Get detection history
- `GET /api/history/{job_id}` - Get specific job details
- `GET /api/history/{job_id}/pdf` - Download PDF report
- `GET /api/history/{job_id}/zip` - Download ZIP archive

### Models
- `GET /api/models/status` - Check model availability
- `GET /api/deepfakebench/models` - List all 12 models

**Full API Documentation**: http://localhost:8000/docs (Swagger UI)

---

## Web Interface

### Pages
1. **Home** (`/web/index_main.html`) - Landing page with method selection
2. **Register** (`/web/register.html`) - Create new account
3. **Login** (`/web/login.html`) - User authentication
4. **TruFor Detection** (`/web/index.html`) - Image analysis
5. **DeepfakeBench** (`/web/deepfakebench.html`) - Video analysis
6. **History** (`/web/history.html`) - View past detections

### Key Features
- **Unified Navigation**: Consistent navbar across all pages
- **Drag & Drop Upload**: Intuitive file upload
- **Real-time Progress**: Live detection status
- **Interactive Results**: Adjustable thresholds, keyframe extraction
- **Responsive Design**: Works on desktop, tablet, and mobile

---

## Common Commands

### Docker
```bash
# Start services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down

# Rebuild after code changes
docker compose up -d --build

# Clean up
docker system prune -a
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

### Development
```bash
# Local development (requires Python 3.11+)
python -m uvicorn app.main:app --reload

# Or use startup scripts
bash scripts/start.sh      # Linux/Mac
scripts\start.bat          # Windows
```

---

## License and Attribution

### Our Project
This project is for **educational and research purposes**.

### Integrated Models

**We only integrated these models - we did NOT train them.**

#### TruFor Model
- **Developed by**: GRIP-UNINA (University of Naples Federico II)
- **Repository**: https://github.com/grip-unina/TruFor
- **License**: Check official repository
- **Citation**:
```bibtex
@article{guillaro2023trufor,
  title={TruFor: Leveraging All-Round Clues for Trustworthy Image Forgery Detection and Localization},
  author={Guillaro, Fabrizio and Cozzolino, Davide and Sud, Avneesh and Dufour, Nicholas and Verdoliva, Luisa},
  journal={arXiv preprint arXiv:2212.10957},
  year={2023}
}
```

#### DeepfakeBench Models
- **Developed by**: SCLBD (Shenzhen Campus of Learning and Big Data)
- **Repository**: https://github.com/SCLBD/DeepfakeBench
- **License**: Check official repository
- **Citation**:
```bibtex
@article{yan2023deepfakebench,
  title={DeepfakeBench: A Comprehensive Benchmark of Deep Learning Methods for Deepfake Detection},
  author={Yan, Zhiyuan and Zhang, Yong and Fan, Yanbo and Wu, Baoyuan},
  journal={arXiv preprint arXiv:2307.01426},
  year={2023}
}
```

**All credit for the models goes to the original authors and research teams.**

---

## Support & Contact

**Project Maintainer**: Xiyu Guan  
**Email**: xiyug@student.unimelb.edu.au  
**GitHub**: https://github.com/lfpaaaaa/deepfake-detector

**For Help**:
1. Check [documentation](#documentation) section above
2. Read [HANDOVER_DOCUMENT.md](docs/handover/HANDOVER_DOCUMENT.md)
3. Review [test reports](docs/testing/test_reports/cycle_3_report.md)
4. Contact maintainer via email

**For Model Issues**:
- TruFor: https://github.com/grip-unina/TruFor/issues
- DeepfakeBench: https://github.com/SCLBD/DeepfakeBench/issues

---

**Last Updated**: November 4, 2025  
**Version**: 3.1  
**Status**: ✅ Production Ready

---

**⭐ Star this repo if you find it useful!**
