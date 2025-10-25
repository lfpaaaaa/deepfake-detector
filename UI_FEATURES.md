# UI Features Documentation

## ✅ V3.0 Update Complete

Your UI has been fully updated with **Authentication**, **History Management**, **Image Detection**, and **Video Analysis** features!

---

## 🎨 UI Features Overview

### 1. Authentication System 🔐

**Registration Page** (`/web/register.html`)
- Create new user account
- Username and password input
- Client-side validation
- Secure password requirements
- Redirect to login after successful registration

**Login Page** (`/web/login.html`)
- User authentication
- JWT token generation
- Remember me functionality (token stored in localStorage)
- Auto-redirect to main page after login
- Session expiration: 24 hours

**Session Management**
- Automatic token validation on protected pages
- Token expiration handling
- Auto-redirect to login when session expires
- Logout functionality (token revocation)
- "Please login first" prompts for unauthenticated access

### 2. Detection History 📜

**History Page** (`/web/history.html`)
- View all your detection jobs
- Filter by status: All, Pending, Processing, Completed, Failed
- Desktop view: Table layout with sortable columns
- Mobile view: Card-based layout (< 768px)
- Real-time status updates

**Features**:
- 📄 **Download PDF**: Generate comprehensive report
- 📦 **Download ZIP**: Get complete results package
- 🗑️ **Delete Job**: Remove detection record
- 🔍 **Job Details**: View detection metadata
- 📊 **Statistics**: Total jobs, completed, pending counts

**Mobile Responsive**:
- Automatic layout switch at 768px breakpoint
- Touch-friendly card interface
- Swipe-optimized interactions
- Compact statistics display

### 3. Dual Mode Detection Switching

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

## 🎉 V3.0 Feature Completion Status

✅ **All V3 Features Implemented**:
- [x] User authentication (JWT)
- [x] User registration and login
- [x] Detection history management
- [x] PDF/ZIP report generation
- [x] Mobile responsive design
- [x] Dual mode UI (Image/Video)
- [x] Image detection (TruFor)
- [x] Video analysis (DeepfakeBench 12 models)
- [x] Real-time progress tracking
- [x] Timeline visualization
- [x] Segments display
- [x] Keyframes gallery
- [x] Threshold adjustment
- [x] Error handling
- [x] CI/CD pipeline

---

## 🚀 V3.0 User Flow

### First Time Users
1. **Register**: Visit `http://localhost:8000/web/register.html`
   - Enter username and password
   - Click "Register"
2. **Login**: Redirect to login page automatically
   - Enter credentials
   - Session valid for 24 hours
3. **Main Page**: Start detecting after login!

### Returning Users
1. **Login**: Visit `http://localhost:8000/web/login.html`
   - Use existing credentials
   - Token stored in browser
2. **Access Features**:
   - Main Page: Image detection
   - DeepfakeBench: Video analysis
   - History: View past detections

### Typical Workflow
```
Register → Login → Upload Media → Detect → View Results → Check History → Download Reports
```

### Detection Flow
1. **Choose Detection Type**:
   - Image: Use main page or TruFor page
   - Video: Use DeepfakeBench page

2. **Upload & Analyze**:
   - Select file (drag & drop or click)
   - Wait for analysis (with progress bar)
   - View results with visualizations

3. **Access History**:
   - Go to History page
   - See all your detections
   - Download PDF/ZIP reports
   - Delete old records

### Mobile Usage
- Access any page on mobile browser
- History page automatically switches to card layout
- Touch-optimized buttons and interactions
- All features available on mobile

---

## 🔒 Security Notes

- **Session Duration**: 24 hours after login
- **Token Storage**: Secure localStorage
- **Auto Logout**: Expired sessions redirect to login
- **Protected Pages**: All detection features require authentication
- **User Isolation**: You can only see your own detection history

---

## 🛠️ Troubleshooting

### "Please login first" Error
- Session expired (>24 hours)
- Solution: Login again at `/web/login.html`

### Can't See History
- Not logged in
- Solution: Check authentication token in localStorage

### Reports Won't Download
- Job not completed yet
- Solution: Wait for "Completed" status

### Mobile Layout Not Showing
- Screen width > 768px
- Solution: Resize browser window or use actual mobile device

---

**Version**: 3.0  
**Last Updated**: October 25, 2025  
**Author**: Xiyu Guan

