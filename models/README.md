# Model Weights Directory

This directory contains the AI model weights required for deepfake detection.

## 📥 Download Instructions

Model weights are **NOT** included in the repository due to their large size.

### Required Files

1. **TruFor Model** (~249 MB)
   - File: `trufor.pth.tar`
   - For: Image forgery detection

2. **DeepfakeBench Models** (~1.1 GB)
   - Directory: `vendors/DeepfakeBench/`
   - For: Video deepfake detection (12 models)

### How to Download

Please follow the detailed instructions in:
**[`docs/guides/WEIGHTS_DOWNLOAD_GUIDE.md`](../docs/guides/WEIGHTS_DOWNLOAD_GUIDE.md)**

Or use the quick link:
**Google Drive**: https://drive.google.com/drive/folders/117IJoriB7kJB9vWQOuj7_S6lNRSOyZ_A

### Expected Directory Structure

After downloading and extracting, your `models/` directory should look like this:

```
models/
├── trufor.pth.tar                          ← TruFor model (249 MB)
└── vendors/                                ← DeepfakeBench folder
    └── DeepfakeBench/
        ├── analysis/
        ├── preprocessing/
        ├── tools/
        └── training/
            └── weights/                    ← 12 model files here
                ├── xception_best.pth
                ├── meso4_best.pth
                ├── meso4Incep_best.pth
                ├── f3net_best.pth
                ├── effnb4_best.pth
                ├── capsule_best.pth
                ├── srm_best.pth
                ├── recce_best.pth
                ├── spsl_best.pth
                ├── ucf_best.pth
                ├── cnnaug_best.pth
                └── core_best.pth
```

## ✅ Verification

Run these commands to verify your setup:

### Windows (PowerShell)
```powershell
# Check TruFor
Get-Item models\trufor.pth.tar

# Count DeepfakeBench models
(Get-ChildItem models\vendors\DeepfakeBench\training\weights\*.pth).Count
# Should show: 12
```

### Linux/Mac
```bash
# Check TruFor
ls -lh models/trufor.pth.tar

# Count DeepfakeBench models
ls models/vendors/DeepfakeBench/training/weights/*.pth | wc -l
# Should show: 12
```

## 🚫 Note

Model files are automatically ignored by `.gitignore` and should **NOT** be committed to the repository.

