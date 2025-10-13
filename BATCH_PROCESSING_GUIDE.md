# 🚀 Batch Processing and Advanced Visualization Guide

## 📋 New Features Overview

This upgrade adds the following advanced features to the DeepfakeBench frame-level inference system:

### ✨ Enhanced Visualization
- **📊 Real-time Probability Bar**: Displays forgery probability at the bottom of the video for the current frame
- **📈 Sparkline Curve**: Shows probability fluctuation trends for the last 5 seconds
- **🎯 Threshold Indicator Line**: Clearly marks the detection threshold
- **⚠️ Suspicious Frame Highlighting**: Frames exceeding threshold are marked with red border
- **📊 Probability-Time Chart**: Complete analysis chart in PNG format
- **📝 SRT Subtitles**: Can display suspicious time segments in players

### 🔄 Batch Processing
- **⚡ Parallel Processing**: Multiple processes handle multiple videos simultaneously
- **🎮 Multi-GPU Support**: Poll-based GPU resource allocation
- **💾 Resume Support**: Automatically skip completed videos
- **📊 Progress Tracking**: Real-time display of processing progress

### 📈 Summary Reports
- **📋 CSV Summary**: All results aggregated into one table
- **📊 Statistical Analysis**: Automatically calculate various statistical indicators
- **🔍 Quick Screening**: Quickly locate suspicious videos

## 🎬 Output Files Description

After processing each video, the following files are generated:

```
runs/image_infer/<model>/<video_name>/
├── scores.csv          # Frame-by-frame scores (frame_idx, timestamp, prob_fake)
├── timeline.json       # Suspicious segment summary (with metadata)
├── plot.png           # 📊 Probability-time curve
├── segments.srt       # 📝 SRT subtitle file
├── vis.mp4           # 🎬 Visualization video (with probability bar and curve)
└── meta.txt          # 📄 Metadata (model, parameters, statistics)
```

### Detailed File Descriptions

#### 📊 `plot.png` - Probability Curve Chart
- X-axis: Time (seconds)
- Y-axis: Forgery probability (0-1)
- Red dashed line: Detection threshold
- Red shading: Suspicious time periods

#### 🎬 `vis.mp4` - Visualization Video
- **Main Screen**: Original video content (scaled to 960x540)
- **Bottom Probability Bar**:
  - Green→Red gradient: Represents probability from low to high
  - White vertical line: Threshold position
  - White curve: Probability sparkline for last 5 seconds
- **Top-left Text**: `p_fake=0.xxx  t=mm:ss`
- **Top-right Text**: Model name and threshold
- **Red Border**: Displayed when threshold is exceeded

#### 📝 `segments.srt` - Subtitle File
```srt
1
00:00:05,200 --> 00:00:12,800
SUSPECT

2
00:00:45,600 --> 00:00:58,300
SUSPECT
```

**Usage**: Place `segments.srt` in the same directory as the original video (with same name). Video players will automatically load subtitles and display "SUSPECT" during suspicious time periods.

#### 📄 `meta.txt` - Metadata
```
model=xception
ckpt=vendors/DeepfakeBench/training/weights/xception_best.pth
input_size=299
fps=3.0
threshold=0.6
frames=150
device=cuda
processing_time=45.23s
```

## 🚀 Usage

### 1️⃣ Single Video Inference (with Visualization)

```bash
python tools/predict_frames.py \
  --input video.mp4 \
  --model xception \
  --fps 3 \
  --threshold 0.6 \
  --save-vis
```

**Output**: Generates all 6 files (including `vis.mp4`)

### 2️⃣ Batch Processing (Multiple Videos)

```bash
# Basic usage: single GPU, 2 parallel processes
python tools/batch_predict.py \
  --input-dir /path/to/videos \
  --model xception \
  --fps 3 \
  --threshold 0.6 \
  --workers 2 \
  --save-vis

# Multi-GPU: Poll GPUs 0 and 1
python tools/batch_predict.py \
  --input-dir /path/to/videos \
  --model f3net \
  --gpus 0,1 \
  --workers 4 \
  --save-vis

# Resume (skip completed)
python tools/batch_predict.py \
  --input-dir /path/to/videos \
  --model xception \
  --workers 3

# Force reprocess all videos
python tools/batch_predict.py \
  --input-dir /path/to/videos \
  --model xception \
  --workers 3 \
  --overwrite

# Only process videos with specific characters in filename
python tools/batch_predict.py \
  --input-dir /path/to/videos \
  --model xception \
  --pattern "suspect" \
  --workers 2
```

**Parameter Descriptions**:
- `--input-dir`: Directory containing videos (recursive search)
- `--model`: Model name or weight file
- `--workers`: Number of parallel processes (recommended 2-4)
- `--gpus`: GPU ID list (e.g., `0,1,2`)
- `--pattern`: Filename filter (only process matching videos)
- `--overwrite`: Force reprocess (default skips completed)
- `--save-vis`: Generate visualization video

### 3️⃣ Aggregate Results

```bash
# Generate summary CSV
python tools/aggregate_runs.py \
  --root runs/image_infer \
  --out runs/summary.csv

# Verbose mode (show processing progress)
python tools/aggregate_runs.py \
  --root runs/image_infer \
  --out runs/summary.csv \
  --verbose
```

**Output CSV Format**:
```csv
model,video,overall_score,average_score,segments,flagged_sec,total_frames,fps,threshold,dir
xception,video1,0.856234,0.423456,2,15.60,150,3.0,0.6,runs/image_infer/xception/video1
f3net,video1,0.789123,0.398765,1,8.20,150,3.0,0.6,runs/image_infer/f3net/video1
```

## 📊 Complete Workflow Examples

### Scenario 1: Quick Batch Screening

```bash
# Step 1: Batch process with fast model
python tools/batch_predict.py \
  --input-dir data/videos \
  --model meso4 \
  --fps 2 \
  --threshold 0.5 \
  --workers 4

# Step 2: Generate summary report
python tools/aggregate_runs.py \
  --root runs/image_infer \
  --out runs/quick_scan_summary.csv

# Step 3: View summary table, find high-scoring videos
# Open runs/quick_scan_summary.csv
# Filter for overall_score > 0.7

# Step 4: Re-analyze suspicious videos with powerful model
python tools/predict_frames.py \
  --input suspect_video.mp4 \
  --model xception \
  --fps 5 \
  --threshold 0.6 \
  --save-vis
```

### Scenario 2: Multi-Model Comparison Analysis

```bash
# Step 1: Process same batch of videos with multiple models
python tools/batch_predict.py --input-dir data/videos --model xception --workers 2 --save-vis
python tools/batch_predict.py --input-dir data/videos --model f3net --workers 2 --save-vis
python tools/batch_predict.py --input-dir data/videos --model recce --workers 2 --save-vis

# Step 2: Generate summary report
python tools/aggregate_runs.py --out runs/multi_model_summary.csv

# Step 3: Compare multi-model results for single video
python tools/quick_compare.py \
  --results_dir runs/image_infer \
  --video video_name

# Step 4: View visualization videos from each model
# runs/image_infer/xception/video_name/vis.mp4
# runs/image_infer/f3net/video_name/vis.mp4
# runs/image_infer/recce/video_name/vis.mp4
```

### Scenario 3: Efficient Multi-GPU Processing

```bash
# Use 4 GPUs, run 2 processes on each GPU (total 8 parallel tasks)
python tools/batch_predict.py \
  --input-dir data/large_dataset \
  --model xception \
  --gpus 0,1,2,3 \
  --workers 8 \
  --fps 3 \
  --save-vis

# Monitor progress in real-time (separate terminal)
watch -n 5 'find runs/image_infer -name "timeline.json" | wc -l'

# Aggregate after processing
python tools/aggregate_runs.py --out runs/large_dataset_summary.csv --verbose
```

## 🎯 Performance Optimization Recommendations

### CPU Mode
```bash
# Lightweight model + low FPS + multi-process
python tools/batch_predict.py \
  --input-dir videos \
  --model meso4 \
  --fps 2 \
  --workers 4 \
  --device cpu
```
**Expected Speed**: ~5-10 seconds/video (depending on CPU)

### Single GPU Mode
```bash
# Balanced model + medium FPS + moderate parallelism
python tools/batch_predict.py \
  --input-dir videos \
  --model f3net \
  --fps 3 \
  --workers 2
```
**Expected Speed**: ~3-5 seconds/video

### Multi-GPU Mode
```bash
# Powerful model + high FPS + high parallelism
python tools/batch_predict.py \
  --input-dir videos \
  --model xception \
  --fps 5 \
  --gpus 0,1 \
  --workers 4 \
  --save-vis
```
**Expected Speed**: ~2-3 seconds/video

## 📝 Subtitle Usage Instructions

### Using SRT in Players

1. **VLC Player**:
   - Place `segments.srt` in same directory as video
   - Rename to match video filename (e.g., `video.mp4` → `video.srt`)
   - Open video in VLC, subtitles will load automatically
   - Or: Subtitle → Add Subtitle File

2. **MPV Player**:
   ```bash
   mpv video.mp4 --sub-file=segments.srt
   ```

3. **Browser (HTML5 Video)**:
   ```html
   <video controls>
     <source src="video.mp4" type="video/mp4">
     <track src="segments.srt" kind="subtitles" srclang="en" label="Suspect Segments">
   </video>
   ```

### Customize Subtitle Styles

SRT files can be manually edited to add styles:
```srt
1
00:00:05,200 --> 00:00:12,800
<font color="red"><b>⚠️ SUSPECT</b></font>
```

## 🔧 Troubleshooting

### Issue: Visualization Video Cannot Be Generated

**Symptoms**: Other files are generated, but no `vis.mp4`

**Solutions**:
1. Confirm using `--save-vis` parameter
2. Check if OpenCV is correctly installed:
   ```bash
   python -c "import cv2; print(cv2.__version__)"
   ```
3. Try different encoder (modify fourcc in code)

### Issue: Batch Processing Stuck

**Symptoms**: Processes start then no response for long time

**Solutions**:
1. Reduce `--workers` count
2. Check if GPU memory is sufficient: `nvidia-smi`
3. Remove `--save-vis` to save resources
4. Use a lighter model

### Issue: Summary Report is Empty

**Symptoms**: `summary.csv` only has headers

**Solutions**:
1. Confirm inference is complete (exists `timeline.json`)
2. Check if path is correct
3. Use `--verbose` to see detailed information

### Issue: Plot Charts Cannot Be Generated

**Symptoms**: Warning "Failed to generate plot"

**Solution**:
```bash
pip install matplotlib
```

## 📚 Dependency Requirements

New features require the following additional dependencies:

```bash
pip install matplotlib  # For generating charts
```

Existing dependencies:
- torch
- torchvision  
- opencv-python
- numpy
- pyyaml

## 🎓 Advanced Tips

### 1. Automatically Process New Videos

Create monitoring script (Linux/Mac):
```bash
#!/bin/bash
# watch_and_process.sh

INPUT_DIR="data/incoming"
MODEL="xception"

while true; do
    python tools/batch_predict.py \
        --input-dir "$INPUT_DIR" \
        --model "$MODEL" \
        --workers 2 \
        --save-vis
    
    python tools/aggregate_runs.py \
        --out runs/latest_summary.csv
    
    sleep 300  # Check every 5 minutes
done
```

### 2. Combine with VideoMAE Scores

```bash
# 1. Frame inference
python tools/predict_frames.py --input video.mp4 --model xception --fps 3

# 2. VideoMAE inference (if available)
# ...

# 3. Fusion
python tools/fuse_scores.py \
  --frame_csv runs/image_infer/xception/video/scores.csv \
  --videomae_csv runs/videomae/video/scores.csv \
  --alpha 0.6 \
  --out runs/fused/video
```

### 3. Export as Report

```bash
# After generating summary, convert to HTML report with Python
python -c "
import pandas as pd
df = pd.read_csv('runs/summary.csv')
df.to_html('runs/report.html', index=False)
"
```

## 📊 Output Examples

### Timeline JSON
```json
{
  "video": "test_video",
  "model": "xception",
  "threshold": 0.6,
  "total_frames": 150,
  "fps": 3.0,
  "overall_score": 0.8523,
  "average_score": 0.4321,
  "suspicious_segments": [
    [5.2, 12.8],
    [45.6, 58.3]
  ],
  "num_suspicious_segments": 2
}
```

### Meta TXT
```
model=xception
ckpt=vendors/DeepfakeBench/training/weights/xception_best.pth
input_size=299
fps=3.0
threshold=0.6
frames=150
device=cuda
processing_time=45.23s
```

### Summary CSV (Partial)
```
model,video,overall_score,average_score,segments,flagged_sec,total_frames,fps,threshold
xception,video1,0.856234,0.423456,2,15.60,150,3.0,0.6
xception,video2,0.234567,0.123456,0,0.00,180,3.0,0.6
f3net,video1,0.789123,0.398765,1,8.20,150,3.0,0.6
```

---

## 🎉 Summary

The new batch processing and visualization features greatly improve the system's usability and efficiency:

- ✅ **More Intuitive**: Visualization videos and charts make results clear at a glance
- ✅ **More Efficient**: Batch processing and multi-GPU support significantly increase processing speed
- ✅ **More Flexible**: Resume support and auto-aggregation save time
- ✅ **More Professional**: SRT subtitles and metadata meet professional needs

Get started! 🚀
