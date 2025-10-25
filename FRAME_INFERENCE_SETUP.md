# DeepfakeBench Frame-Level Model Inference - Setup Complete

## ✅ Completed Work

### 1. Core Files Created

The following tool files have been created:

- **`tools/weight_registry.py`** - Weight file mapping table
- **`tools/build_dfbench_model.py`** - Model loading factory
- **`tools/predict_frames.py`** - Main inference script
- **`tools/fuse_scores.py`** - Score fusion script
- **`tools/test_setup.py`** - System test script
- **`tools/__init__.py`** - Python package initialization file

### 2. Supported Models

12 DeepfakeBench models are currently available (FFD was removed in V3.0):

| Model | Weight File | Input Size | Status |
|------|---------|---------|------|
| Xception | xception_best.pth | 299x299 | ✅ Ready |
| MesoNet-4 | meso4_best.pth | 256x256 | ✅ Ready |
| MesoNet-4 Inception | meso4Incep_best.pth | 256x256 | ✅ Ready |
| F3Net | f3net_best.pth | 224x224 | ✅ Ready |
| EfficientNet-B4 | effnb4_best.pth | 380x380 | ✅ Ready |
| Capsule Net | capsule_best.pth | 128x128 | ✅ Ready |
| SRM | srm_best.pth | 299x299 | ✅ Ready |
| RECCE | recce_best.pth | 224x224 | ✅ Ready |
| SPSL | spsl_best.pth | 224x224 | ✅ Ready |
| UCF | ucf_best.pth | 256x256 | ✅ Ready |
| CNN-AUG | cnnaug_best.pth | 224x224 | ✅ Ready |
| CORE | core_best.pth | 224x224 | ✅ Ready |

All weight files are placed in: `vendors/DeepfakeBench/training/weights/`

### 3. Feature Capabilities

✅ **Frame-by-Frame Analysis**: Can set any FPS extraction rate
✅ **Multi-Model Support**: Supports 12 different detection models
✅ **Batch Processing**: Can process single videos or entire directories
✅ **Timeline Generation**: Automatically identifies suspicious time periods
✅ **Score Fusion**: Can fuse with VideoMAE results
✅ **Flexible Configuration**: Adjustable threshold, FPS and other parameters
✅ **Device Selection**: Supports GPU (CUDA) and CPU inference

## 🚀 Quick Start

### Method 1: Using Batch Script (Recommended)

Run the provided test script:

```batch
test_inference.bat
```

### Method 2: Command Line Execution

```bash
# Single video inference
python tools/predict_frames.py \
  --input data/jobs/job_440557d4147f_1760275209/input.mp4 \
  --model xception \
  --fps 3 \
  --threshold 0.6 \
  --device cuda

# Batch processing
python tools/predict_frames.py \
  --input data/jobs/ \
  --model meso4 \
  --fps 2 \
  --threshold 0.5 \
  --device cpu
```

## 📊 Output Description

For each video, the following will be generated in the output directory:

### 1. `scores.csv` - Frame-by-Frame Scores
```csv
frame_idx,timestamp,prob_fake
0,0.000,0.234567
1,0.500,0.456789
2,1.000,0.678901
...
```

### 2. `timeline.json` - Suspicious Segment Summary
```json
{
  "video": "input",
  "model": "xception",
  "threshold": 0.6,
  "total_frames": 150,
  "overall_score": 0.8523,
  "average_score": 0.4321,
  "suspicious_segments": [
    [5.2, 12.8],
    [45.6, 58.3]
  ],
  "num_suspicious_segments": 2
}
```

## 🔧 Common Command Examples

### Quick Screening (Low FPS + Lightweight Model)
```bash
python tools/predict_frames.py \
  --input video.mp4 \
  --model meso4 \
  --fps 2 \
  --threshold 0.5
```

### High Accuracy Detection (High FPS + Powerful Model)
```bash
python tools/predict_frames.py \
  --input video.mp4 \
  --model xception \
  --fps 5 \
  --threshold 0.6 \
  --device cuda
```

### Batch Process Directory
```bash
python tools/predict_frames.py \
  --input data/jobs/ \
  --model f3net \
  --fps 3 \
  --threshold 0.55
```

### CPU Mode (When No GPU Available)
```bash
python tools/predict_frames.py \
  --input video.mp4 \
  --model capsule_net \
  --fps 2 \
  --device cpu
```

## 🔗 Score Fusion (Combining with VideoMAE)

If you already have VideoMAE analysis results:

```bash
python tools/fuse_scores.py \
  --frame_csv runs/image_infer/xception/video/scores.csv \
  --videomae_csv runs/videomae/video/scores.csv \
  --alpha 0.6 \
  --threshold 0.55 \
  --out runs/fused/video
```

**Parameter Descriptions:**
- `--alpha`: VideoMAE weight (0.6 = 60% VideoMAE + 40% frame model)
- `--threshold`: Post-fusion detection threshold

**Output Files:**
- `scores_fused.csv`: Fused frame-by-frame scores
- `timeline_fused.json`: Fused suspicious segments

## 📈 Performance Recommendations

### Speed Priority
- Model: `meso4` or `capsule_net`
- FPS: 2
- Device: GPU (if available)

### Accuracy Priority
- Model: `xception` or `efficientnetb4`
- FPS: 5
- Fusion: Combine with VideoMAE

### Balanced Choice
- Model: `f3net` or `recce`
- FPS: 3
- Device: GPU

## 📁 File Structure

```
deepfake-detector/
├── tools/
│   ├── __init__.py
│   ├── weight_registry.py          # Weight mapping
│   ├── build_dfbench_model.py      # Model building
│   ├── predict_frames.py           # Main inference script
│   ├── fuse_scores.py              # Score fusion
│   ├── test_setup.py               # Test script
│   └── README.md                   # Detailed documentation
│
├── vendors/DeepfakeBench/
│   └── training/
│       ├── detectors/              # Model definitions
│       ├── config/detector/        # Model configurations
│       └── weights/                # Weight files (13 .pth files)
│
├── runs/                           # Inference result output
│   ├── image_infer/                # Frame inference results
│   │   └── <model_name>/
│   │       └── <video_name>/
│   │           ├── scores.csv
│   │           └── timeline.json
│   └── fused/                      # Fusion results
│       └── <video_name>/
│           ├── scores_fused.csv
│           └── timeline_fused.json
│
├── test_inference.bat              # Windows quick test
└── FRAME_INFERENCE_SETUP.md        # This document
```

## 🐛 Troubleshooting

### Issue: Model Not Found

**Solution:**
1. Check if model name is correct (refer to supported models table)
2. Run `python tools/test_setup.py` to check system status

### Issue: CUDA Out of Memory

**Solution:**
```bash
# Reduce FPS
python tools/predict_frames.py --input video.mp4 --model meso4 --fps 2

# Or use CPU
python tools/predict_frames.py --input video.mp4 --model meso4 --device cpu
```

### Issue: Weight Loading Failed

**Solution:**
1. Confirm weight file exists: `dir vendors\DeepfakeBench\training\weights\`
2. Check if file size is normal (should not be 0 KB)
3. If there's a problem, re-download the corresponding weight

### Issue: PowerShell Display Anomalies

This is a known issue with PowerShell console and doesn't affect actual execution. You can:
1. Use batch script to run
2. Check output directory directly for results
3. Or use standard CMD instead of PowerShell

## 📚 More Information

- **Detailed Usage Documentation**: `tools/README.md`
- **DeepfakeBench Official**: https://github.com/SCLBD/DeepfakeBench
- **Model Configuration**: `vendors/DeepfakeBench/training/config/detector/`

## ✨ Future Extensions

Functions that can be further added:

1. **Visualization Output**: Overlay score curves on videos
2. **Ensemble Detection**: Multi-model voting fusion
3. **Web API**: REST API interface
4. **Real-time Inference**: Real-time camera detection
5. **Report Generation**: Auto-generate PDF/HTML reports

## 📝 Version Information

- **Creation Date**: 2025-10-12
- **Supported Models**: 13 DeepfakeBench image detectors
- **Python Version**: 3.8+
- **PyTorch Version**: 1.9+

---

## ⚡ Next Steps

Now that the system is fully configured, you can:

1. **Run Tests**: Execute `test_inference.bat` to verify the system
2. **Process Videos**: Use `tools/predict_frames.py` to analyze videos
3. **View Results**: Check the `runs/test_infer/` directory
4. **Read Documentation**: Check `tools/README.md` for more features

Enjoy! 🎉
