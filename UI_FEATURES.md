# UI Features Documentation

## ✅ Update Complete

Your UI has been fully updated and now supports both **Image Detection** and **Video Analysis** modes!

---

## 🎨 New UI Features

### 1. Dual Mode Switching

**Image Detection Mode** 📷
- Drag & drop or click to upload images
- Real-time analysis progress
- Display detection results and confidence
- Supports JPG, PNG (max 10MB)

**Video Analysis Mode** 🎥
- Drag & drop or click to upload videos
- Real-time progress tracking
- Timeline visualization
- Segments and Keyframes display
- Supports MP4, MOV (max 50MB)

### 2. Video Analysis Features

#### 📊 Analysis Summary
Displays 4 key metrics:
- **Duration**: Total video length (seconds)
- **Clips Analyzed**: Number of analyzed frames
- **Threshold**: Current detection threshold
- **Suspicious**: Number of detected suspicious segments

#### ⏱️ Detection Timeline
- **Visualization Chart**: Red areas indicate suspicious segments
- **Interactive**: Hover to show detailed information
- **Time Labels**: Display specific time points of segments
- **Adjustment Slider**: Real-time threshold adjustment (0-100%)
  - Higher value = Stricter detection = Fewer segments
  - Lower value = Looser detection = More segments

#### 🚨 Suspicious Segments
Each segment displays:
- **Segment ID**: Segment number
- **Time Range**: Start time - End time (duration)
- **Peak Score**: Peak score (0-1, higher = more suspicious)
- **Peak Time**: Time when peak occurs

#### 🖼️ Key Frames
- **Thumbnail Display**: Keyframe images for each segment
- **Card Layout**: Responsive grid layout (2/3/4 columns)
- **Detailed Info**: Segment number, time point, score
- **Hover Effect**: Zoom in on mouse hover

---

## 🎮 Usage Guide

### Image Detection Workflow

1. **Open Page**: http://localhost:8000
2. **Select Mode**: Click "📷 Image Detection" (default)
3. **Upload Image**: 
   - Drag image to upload area
   - Or click "Choose Image" button to select file
4. **View Results**:
   - Original image preview
   - Detection result (real/fake)
   - Confidence score
5. **Continue Analysis**: Click "Analyze Another" to upload new image

### Video Analysis Workflow

1. **Open Page**: http://localhost:8000
2. **Switch Mode**: Click "🎥 Video Analysis"
3. **Upload Video**:
   - Drag video to upload area
   - Or click "Choose Video" button to select file
4. **Wait for Analysis**:
   - Real-time progress bar showing analysis progress
   - Stage hints (upload→extract→analyze→detect→complete)
   - Estimated time: ~30-60 seconds for 30-second video
5. **View Results**:
   - **Summary**: View overall statistics
   - **Timeline**: See suspicious areas on timeline
   - **Adjust Threshold**: Move slider to see different strictness results
   - **Segments**: View detailed info for each suspicious segment
   - **Keyframes**: Browse keyframe images
6. **Continue Analysis**: Click "Analyze Another Video" to upload new video

---

## 🎨 UI Design Features

### Responsive Design
- ✅ Desktop: Full layout (6-column width)
- ✅ Tablet: Adaptive layout (medium screen)
- ✅ Mobile: Single column layout (small screen)

### Visual Effects
- ✅ Smooth transition animations
- ✅ Hover interaction feedback
- ✅ DaisyUI theme styles
- ✅ Tailwind CSS responsive

### User Experience
- ✅ Drag & drop upload
- ✅ Real-time progress updates
- ✅ Interactive charts
- ✅ Clear visual feedback
- ✅ Error notifications

---

## 📊 Timeline Visualization

### Timeline Components

```
┌─────────────────────────────────────────────┐
│                                             │
│  ███     ██         ███                     │ ← Red areas = Suspicious segments
│                                             │
└─────────────────────────────────────────────┘
0:00                                      5:30
```

### Threshold Adjustment Effects

**High Threshold (80-100%)**:
- Shows only the most suspicious segments
- High precision, low recall
- Suitable for: Quick overview of obvious issues

**Medium Threshold (40-80%)**:
- Balanced precision and coverage
- Default recommended setting
- Suitable for: General analysis

**Low Threshold (0-40%)**:
- Shows all possible issues
- High recall, may have false positives
- Suitable for: Comprehensive inspection

---

## 🔧 Technical Implementation

### Frontend Tech Stack
- **HTML5**: Modern semantic markup
- **Tailwind CSS**: Utility-first CSS framework
- **DaisyUI**: Tailwind component library
- **Vanilla JavaScript**: Native JS, no dependencies

### API Integration
- `POST /detect`: Image detection
- `POST /video/analyze`: Video analysis (returns job_id)
- `GET /video/jobs/{job_id}/status`: Query analysis progress
- `GET /video/jobs/{job_id}/result`: Get complete results
- `GET /video/jobs/{job_id}/keyframes/{filename}`: Get keyframe images

### Real-time Update Mechanism
- **Polling**: Query job status every 1 second
- **Progress Display**: Real-time progress bar update (0-100%)
- **Stage Hints**: Show current processing stage
- **Auto Complete**: Automatically load results when analysis completes

---

## 🎯 Use Cases

### Case 1: Quick Detection
```
1. Open page
2. Click "Video Analysis"
3. Drag & drop video
4. Wait 30 seconds
5. View Timeline - spot problem areas at a glance
```

### Case 2: Detailed Analysis
```
1. Upload video and complete analysis
2. Adjust threshold slider to different positions
3. Compare detection results at different thresholds
4. Review Segments detailed information
5. Check Keyframes images
6. Identify suspicious areas
```

### Case 3: Batch Detection
```
1. Analyze first video
2. Record results
3. Click "Analyze Another Video"
4. Repeat steps 1-3
```

---

## 🐛 Troubleshooting

### Issue 1: Page has no styling
**Symptom**: Page displays plain text, no colors or layout
**Cause**: CDN loading failed
**Solution**: 
- Check network connection
- Refresh page (Ctrl+F5)
- Wait for CDN to recover

### Issue 2: No response after video upload
**Symptom**: Progress bar doesn't move after clicking upload
**Cause**: 
- File too large (>50MB)
- Format not supported
- Service not started
**Solution**:
- Check file size and format
- Confirm service is running: http://localhost:8000/health
- Check browser console for error messages

### Issue 3: Keyframe images won't display
**Symptom**: Keyframe area shows broken image icon
**Cause**: 
- Analysis not fully completed
- File path error
**Solution**:
- Wait for analysis to fully complete
- Refresh page to reload
- Check if job directory contains keyframes folder

### Issue 4: No red areas on Timeline
**Symptom**: Timeline is blank
**Cause**: 
- No suspicious segments detected in video
- Threshold set too high
**Solution**:
- Lower threshold slider (move to left)
- Try different test videos

---

## 🌟 Best Practices

### Upload Recommendations
- ✅ Use MP4 format (best compatibility)
- ✅ File size < 30MB (faster processing)
- ✅ Video duration < 2 minutes (reasonable time)
- ✅ Videos with faces (better detection)

### Threshold Settings
- **First analysis**: Use default value (50%)
- **Suspected issues**: Lower to 30-40% to see more details
- **Confirm issues**: Raise to 70-80% to see only obvious problems

### Result Interpretation
- **Multiple Segments**: Video may have multiple problem areas
- **High Peak Score (>0.8)**: Segment is very suspicious
- **Long Duration**: Problem persists for extended time
- **No Segments**: Video may be authentic (or lower threshold to check again)

---

## 📸 UI Screenshots Description

### Main Interface
- Top: Title and subtitle
- Middle: Mode switch buttons (image/video)
- Bottom: Upload area (changes based on mode)

### Video Analysis Results Page
1. **Summary Card**: 4 statistical numbers
2. **Timeline Card**: Timeline chart + threshold slider
3. **Segments Card**: Warning list
4. **Keyframes Card**: Image grid

---

## 🎉 Completion Status

✅ **All Features Implemented**:
- [x] Dual mode UI
- [x] Image detection
- [x] Video upload
- [x] Real-time progress
- [x] Timeline visualization
- [x] Segments display
- [x] Keyframes gallery
- [x] Threshold adjustment
- [x] Responsive design
- [x] Error handling

---

## 🚀 Start Testing Now!

1. Open browser
2. Visit http://localhost:8000
3. Click "🎥 Video Analysis"
4. Upload test video
5. Enjoy the new video analysis experience!

**Happy Testing!** 🎊

