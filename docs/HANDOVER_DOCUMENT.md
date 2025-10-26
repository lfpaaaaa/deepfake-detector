# Project Handover Document

**Project**: Deepfake Detector  
**Version**: 3.0  
**Document Date**: October 26, 2025  
**Prepared By**: Xiyu Guan  
**Email**: xiyug@student.unimelb.edu.au

---

## Executive Summary

The Deepfake Detector is a production-ready web application for detecting manipulated images and videos using TruFor (image analysis) and DeepfakeBench (video analysis with 12 models). The system is fully documented, tested (109 tests, 93% pass rate), and containerized with Docker for easy deployment.

**Repository**: https://github.com/lfpaaaaa/deepfake-detector  
**Branch**: main (production-ready)

---

## 1. Quick Start

### For New Developers/Maintainers

**Essential Reading Order**:
1. **Start Here**: [README.md](../README.md) - System overview and quick start
2. **Setup**: [WEIGHTS_DOWNLOAD_GUIDE.md](../WEIGHTS_DOWNLOAD_GUIDE.md) - Download and setup model weights
3. **Architecture**: [V3 Domain Model](architecture/v3_domain_model_diagram.md) - System design
4. **Testing**: [Testing README](testing/README.md) - Testing strategy and results

**Quick Commands**:
```bash
# Clone and start
git clone https://github.com/lfpaaaaa/deepfake-detector.git
cd deepfake-detector

# Download weights (see WEIGHTS_DOWNLOAD_GUIDE.md)
# Then start with Docker:
docker compose up -d --build

# Access at: http://localhost:8000
```

---

## 2. Documentation Index

### 2.1 Getting Started
| Document | Purpose | Location |
|----------|---------|----------|
| Main README | System overview, features, quick start | [README.md](../README.md) |
| Weights Guide | Model weight download & setup | [WEIGHTS_DOWNLOAD_GUIDE.md](../WEIGHTS_DOWNLOAD_GUIDE.md) |
| Quick Reference | Common tasks & commands | [QUICK_REFERENCE_V2.md](../QUICK_REFERENCE_V2.md) |

### 2.2 Architecture & Design
| Document | Purpose | Location |
|----------|---------|----------|
| V3 Domain Model | Current system architecture | [v3_domain_model_diagram.md](architecture/v3_domain_model_diagram.md) |
| V3 Sequence Diagram | System interaction flows | [v3_sequence_diagram.md](architecture/v3_sequence_diagram.md) |
| Upgrade Summary | V1.0 → V2.0 changes | [UPGRADE_SUMMARY_V2.md](../UPGRADE_SUMMARY_V2.md) |

### 2.3 User Research & Requirements
| Document | Purpose | Location |
|----------|---------|----------|
| User Stories | User requirements | [usecases/](usecases/) |
| Personas | Target user profiles | [personas.md](usecases/personas.md) |
| Meeting Notes | Client meetings | [meetings/](meetings/) |

### 2.4 Technical Guides
| Document | Purpose | Location |
|----------|---------|----------|
| TruFor Guide | TruFor integration details | [TRUFOR_TECHNICAL_GUIDE.md](TRUFOR_TECHNICAL_GUIDE.md) |
| Model Setup | DeepfakeBench setup | [MODEL_SETUP.md](MODEL_SETUP.md) |
| Frame Inference | Video frame processing | [FRAME_INFERENCE_SETUP.md](../FRAME_INFERENCE_SETUP.md) |
| DeepfakeBench Quick Start | DeepfakeBench usage | [DeepfakeBench_QUICK_START.md](../DeepfakeBench_QUICK_START.md) |
| Batch Processing | Batch detection guide | [BATCH_PROCESSING_GUIDE.md](../BATCH_PROCESSING_GUIDE.md) |

### 2.5 Testing Documentation
| Document | Purpose | Location |
|----------|---------|----------|
| Testing Overview | Complete testing strategy | [testing/README.md](testing/README.md) |
| Test Cases | All 28 test scenarios | [TEST_CASES.md](testing/TEST_CASES.md) |
| Cycle 1 Report | Automated tests (67 tests) | [cycle_1_report.md](testing/test_reports/cycle_1_report.md) |
| Cycle 2 Report | Manual tests (42 tests) | [cycle_2_report.md](testing/test_reports/cycle_2_report.md) |
| Test Plans | Cycle-specific test plans | [test_plans/](testing/test_plans/) |

### 2.6 UI Documentation
| Document | Purpose | Location |
|----------|---------|----------|
| UI Features | Frontend feature list | [UI_FEATURES.md](../UI_FEATURES.md) |

---

## 3. System Overview

### 3.1 Technology Stack
- **Backend**: Python 3.11, FastAPI
- **Frontend**: HTML/CSS/JavaScript (Vanilla)
- **ML Frameworks**: PyTorch 2.0+, OpenCV
- **Deployment**: Docker, Docker Compose
- **CI/CD**: GitHub Actions
- **Testing**: pytest (67 automated tests)

### 3.2 Key Components
```
├── app/                  ← FastAPI application
│   ├── adapters/         ← Model wrappers (TruFor, DeepfakeBench)
│   ├── auth/             ← JWT authentication
│   ├── history/          ← Detection history
│   ├── reports/          ← PDF/ZIP generation
│   ├── web/              ← Frontend (HTML/CSS/JS)
│   └── main.py           ← API endpoints
├── tests/                ← Automated tests (pytest)
├── tools/                ← Detection utilities
├── vendors/              ← DeepfakeBench (12 models)
├── TruFor-main/          ← TruFor framework
└── docs/                 ← Documentation
```

For detailed structure, see [README.md](../README.md) section "Project Structure".

### 3.3 Detection Models

**TruFor (Image Detection)**:
- Weight file: `trufor.pth.tar` (1.2GB)
- Official: https://grip-unina.github.io/TruFor/
- Features: Anomaly detection, confidence maps

**DeepfakeBench (Video Detection)**:
- 12 models: Xception, EfficientNet-B4, UCF, Capsule, RECCE, FWA, SBI, CORE, Xception-C23, Xception-C40, SPSL, F3Net
- Weight directory: `vendors/DeepfakeBench/training/weights/`
- Official: https://github.com/SCLBD/DeepfakeBench

**Note**: Model weights not in git. Download from [Google Drive](https://drive.google.com/drive/folders/117IJoriB7kJB9vWQOuj7_S6lNRSOyZ_A).

---

## 4. Development & Maintenance

### 4.1 Running Tests
```bash
# All automated tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Specific test file
pytest tests/test_auth.py
```

See [testing/README.md](testing/README.md) for complete testing guide.

### 4.2 CI/CD Pipeline
- **Platform**: GitHub Actions
- **Workflow**: `.github/workflows/ci.yml`
- **Checks**: Code quality, security scan, unit tests, config validation
- **Trigger**: Push to main branch

### 4.3 Common Tasks

**Update Dependencies**:
```bash
pip install -r configs/requirements.txt --upgrade
docker compose up -d --build
```

**Backup User Data**:
```bash
tar -czf backup_$(date +%Y%m%d).tar.gz data/
```

**View Logs**:
```bash
docker compose logs -f
```

**Troubleshooting**: See [README.md](../README.md) section "Troubleshooting".

---

## 5. Known Issues

### 5.1 Active Bugs
4 bugs documented in [Cycle 2 Report](testing/test_reports/cycle_2_report.md):

| Bug ID | Severity | Description | Workaround |
|--------|----------|-------------|------------|
| BUG-007 | High | Browser crash with images >1MB | Use images <1MB |
| BUG-009 | Medium | NaN% for corrupted files | Manual validation |
| BUG-010 | High | Invalid token doesn't redirect | Clear localStorage |
| BUG-011 | Medium | UI breaks with F12 DevTools | Refresh page |

**Full Details**: [cycle_2_report.md](testing/test_reports/cycle_2_report.md) - Section 9

### 5.2 Limitations
- Single-user deployments only (no multi-tenancy)
- Model weights not in git (size/licensing)
- GPU recommended for large video processing
- No admin dashboard yet

---

## 6. Version History

| Version | Date | Key Changes | Documentation |
|---------|------|-------------|---------------|
| **V3.0** | Oct 2025 | Testing complete, CI/CD, mobile UI, 12 models | Current |
| V2.0 | Sep 2025 | TruFor + DeepfakeBench (13 models), auth, reports | [UPGRADE_SUMMARY_V2.md](../UPGRADE_SUMMARY_V2.md) |
| V1.0 | Initial | Basic detection | - |

**Note**: FFD model removed in V3.0 (12 models remain).

---

## 7. Testing Summary

### 7.1 Test Coverage
- **Cycle 1**: 67 automated tests, 100% pass rate, 70% code coverage
- **Cycle 2**: 42 manual/integration tests, 88% pass rate
- **Total**: 109 tests, 93% overall pass rate

### 7.2 Test Types
✅ Unit tests (auth, history, adapters)  
✅ Integration tests (API endpoints)  
✅ Performance tests (response times)  
✅ Security tests (SQL injection, token validation)  
✅ Edge cases (invalid files, special characters, large files)  
✅ UI tests (mobile responsive, navigation)  

**Complete Details**: [testing/README.md](testing/README.md)

---

## 8. Contact & Support

### 8.1 Current Maintainer
- **Name**: Xiyu Guan
- **Email**: xiyug@student.unimelb.edu.au
- **GitHub**: https://github.com/lfpaaaaa/deepfake-detector

### 8.2 Getting Help
1. Check documentation (this document + README)
2. Review [Known Issues](#51-active-bugs)
3. Check GitHub Issues
4. Contact maintainer via email

---

## 9. Handover Checklist

### 9.1 Knowledge Transfer
- [ ] Review this document with new maintainer
- [ ] Walk through [README.md](../README.md) and [WEIGHTS_DOWNLOAD_GUIDE.md](../WEIGHTS_DOWNLOAD_GUIDE.md)
- [ ] Demonstrate system setup (Docker)
- [ ] Show key features (detection workflows)
- [ ] Review [architecture diagrams](architecture/v3_domain_model_diagram.md)
- [ ] Explain [testing strategy](testing/README.md)
- [ ] Discuss [known issues](#51-active-bugs) and workarounds

### 9.2 Access & Credentials
- [ ] Provide GitHub repository access
- [ ] Share Google Drive link for model weights
- [ ] Verify new maintainer can build and run system
- [ ] Ensure new maintainer can run tests

### 9.3 Post-Handover
- [ ] Monitor for questions/issues (first 2 weeks)
- [ ] Update documentation based on feedback
- [ ] Provide additional support as needed

---

## 10. Future Recommendations

### High Priority
1. **Fix BUG-007**: Implement image resizing/compression for large files
2. **Fix BUG-010**: Add token validation on page load
3. **Improve error handling**: Better messages for corrupted files

### Medium Priority
4. Admin dashboard for user management
5. API rate limiting and key authentication
6. Model version updates (TruFor, DeepfakeBench)

### Low Priority
7. Batch processing web interface
8. Export history to JSON/CSV
9. Multi-language support (i18n)

**Full List**: See [Cycle 2 Report - Section 11](testing/test_reports/cycle_2_report.md#11-recommendations)

---

## Appendix: Quick Reference

### Essential Commands
```bash
# Start system
docker compose up -d

# Stop system
docker compose down

# Rebuild after changes
docker compose up -d --build

# View logs
docker compose logs -f

# Run tests
pytest

# Run tests with coverage
pytest --cov=app

# Backup data
tar -czf backup.tar.gz data/
```

### Key File Locations
| Item | Location |
|------|----------|
| User accounts | `data/users.json` |
| Detection results | `data/jobs/` |
| TruFor weights | `trufor.pth.tar` |
| DeepfakeBench weights | `vendors/DeepfakeBench/training/weights/` |
| Configuration | `configs/config.yaml` |
| Frontend | `app/web/` |
| Tests | `tests/` |
| Documentation | `docs/` |

### Important Links
- **Repository**: https://github.com/lfpaaaaa/deepfake-detector
- **TruFor**: https://grip-unina.github.io/TruFor/
- **DeepfakeBench**: https://github.com/SCLBD/DeepfakeBench
- **Model Weights**: https://drive.google.com/drive/folders/117IJoriB7kJB9vWQOuj7_S6lNRSOyZ_A

---

**Document Version**: 2.0 (Streamlined)  
**Last Updated**: October 26, 2025  
**Status**: ✅ Ready for Handover

---

*This document serves as a navigation hub. For detailed information, please refer to the linked documents above.*
