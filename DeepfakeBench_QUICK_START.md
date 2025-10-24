# 🚀 DeepfakeBench Frame-Level Inference - Quick Start

## ⚡ Get Started in 3 Steps

### 1️⃣ View Available Models

```bash
python tools/list_models.py
```

### 2️⃣ Run Your First Inference

```batch
# Windows
test_inference.bat

# Or run manually
python tools/predict_frames.py --input data/jobs/job_440557d4147f_1760275209/input.mp4 --model meso4 --fps 2
```

### 3️⃣ Check Results

Check the output directory:
- `runs/test_infer/meso4/input/scores.csv` - Frame-by-frame scores
- `runs/test_infer/meso4/input/timeline.json` - Suspicious time segments

## 📋 Common Commands

### Single Video Analysis
```bash
python tools/predict_frames.py \
  --input video.mp4 \
  --model xception \
  --fps 3 \
  --threshold 0.6
```

### Batch Processing
```bash
python tools/predict_frames.py \
  --input data/jobs/ \
  --model f3net \
  --fps 2
```

### Multi-Model Comparison
```batch
# Test 5 different models
test_all_models.bat

# Compare results
python tools/quick_compare.py --results_dir runs/model_comparison --video input
```

### Fuse with VideoMAE Scores
```bash
python tools/fuse_scores.py \
  --frame_csv runs/image_infer/xception/video/scores.csv \
  --videomae_csv runs/videomae/video/scores.csv \
  --alpha 0.6 \
  --out runs/fused/video
```

## 🎯 Recommended Model Selection

| Scenario | Model | FPS | Features |
|------|------|-----|------|
| Quick Screening | `meso4` | 2 | Lightweight and fast |
| Standard Detection | `f3net` | 3 | Balanced performance |
| High Accuracy | `xception` | 5 | Highest accuracy |
| Real-time Processing | `capsule_net` | 2 | Ultra-fast speed |

## 📊 Parameter Descriptions

| Parameter | Description | Default | Example |
|------|------|--------|------|
| `--input` | Video file or directory | Required | `video.mp4` |
| `--model` | Model name | Required | `xception` |
| `--fps` | Frame extraction rate | 3.0 | `2`, `5` |
| `--threshold` | Detection threshold | 0.5 | `0.6` |
| `--device` | Compute device | `cuda` | `cpu` |
| `--outdir` | Output directory | `runs/image_infer` | Custom path |

## 🔍 Output File Descriptions

### scores.csv
```csv
frame_idx,timestamp,prob_fake
0,0.000,0.234567
1,0.333,0.456789
```

### timeline.json
```json
{
  "overall_score": 0.8523,
  "suspicious_segments": [
    [5.2, 12.8],
    [45.6, 58.3]
  ]
}
```

## 📚 More Information

- **Complete Documentation**: `FRAME_INFERENCE_SETUP.md`
- **Detailed Tutorial**: `tools/README.md`
- **Supported Models**: 13 DeepfakeBench detectors

## 💡 Tips

1. First run will be slower (model loading)
2. GPU inference is approximately 10-20x faster than CPU
3. Higher FPS is more accurate but takes longer to process
4. Can run multiple models simultaneously for comparison

## 🐛 Issues?

See the troubleshooting section in `FRAME_INFERENCE_SETUP.md`
