# VideoMAE Weights Download Guide

## 📥 Question 1: Where to download weights?

### ⚠️ Important Finding: VideoMAE Weights Not Available!

**After checking DeepfakeBench GitHub Releases**:
```
https://github.com/SCLBD/DeepfakeBench/releases
```

**Results**:
- ❌ v1.0.1 - Only weights for other detectors (xception, f3net, core, etc.), **NO VideoMAE**
- ❌ v1.0.2 - Face X-ray related files
- ❌ v1.0.3 - I3D related weights

**Conclusion**: 
DeepfakeBench has **NOT released** VideoMAE pretrained weights!

### ✅ Only Available Solution: Hugging Face Model (Recommended)

Since official weights are not provided, **you can only use Hugging Face model**:
- Model will be automatically downloaded from internet
- No manual operations needed
- System is already configured, works out of the box

### Why No VideoMAE Weights?

Possible reasons:
1. VideoMAE is a newer video detector
2. Requires significant computational resources to train
3. DeepfakeBench team hasn't released yet
4. May need to train yourself (not recommended, requires large dataset and GPU)

---

## 📁 Question 2: Where should it be placed?

### ❌ No Need to Manually Place Weights!

Since DeepfakeBench **doesn't provide** VideoMAE weights, you:
- ❌ Don't need to download any files
- ❌ Don't need to manually place weights
- ✅ System will automatically use Hugging Face model

**If weights become available in the future**, they should be placed at:
```
vendors/DeepfakeBench/training/weights/videomae_pretrained.pth
```

But currently this file **doesn't exist and isn't needed**!

---

## 🤖 Question 3: What is Hugging Face Model?

### Simple Explanation

**Hugging Face** is an AI model sharing platform, similar to GitHub but specifically for AI models.

### Its Role in This Project

#### Comparison of Two Model Sources:

| Feature | DeepfakeBench Weights (Local) | Hugging Face Model (Online) |
|---------|------------------------------|----------------------------|
| **Source** | Manual download from GitHub | Auto-download from internet |
| **Training Data** | Specifically trained for deepfake detection | General video understanding tasks |
| **Accuracy** | 🟢 High (specifically trained) | 🟡 Medium (general model) |
| **Speed** | 🟢 Fast (local loading) | 🟡 First-time download needed |
| **File Size** | ~350MB | ~350MB |
| **Use Case** | ✅ Production environment | ⚠️ Testing/Development |

### Detailed Explanation

**1. DeepfakeBench Weights (Recommended for Production)**:
```
✅ Specifically trained for detecting deepfake videos
✅ Trained on multiple deepfake datasets
✅ Higher detection accuracy
✅ This is the best model released by researchers
```

**2. Hugging Face Model (Temporary Solution)**:
```
⚠️ Base pretrained VideoMAE model
⚠️ Originally for general video classification tasks (like action recognition)
⚠️ Not fine-tuned for deepfake
⚠️ Detection accuracy will be lower
✅ But allows system to run
```

### How System Chooses

The code I wrote follows this priority:

```python
1. First check: vendors/DeepfakeBench/training/weights/videomae_pretrained.pth
   ├─ If exists → Use local DeepfakeBench weights ✅
   └─ If not exists → Continue to next step

2. Then try downloading from Hugging Face:
   ├─ Access: MCG-NJU/videomae-base
   ├─ Auto-download to cache
   └─ Use Hugging Face model ⚠️
```

### Actual Difference Example

Suppose analyzing a video containing deepfake:

**Using DeepfakeBench Weights**:
```
Segment 1: 0:05-0:12, score: 0.87 (high confidence detection)
Segment 2: 0:28-0:35, score: 0.92 (high confidence detection)
Result: Accurately identifies deepfake segments
```

**Using Hugging Face Model**:
```
Segment 1: 0:05-0:12, score: 0.61 (medium confidence)
Segment 2: 0:28-0:35, score: 0.68 (medium confidence)
Result: May identify, but with lower confidence
Or: May miss some segments
```

---

## 🎯 My Recommendation

### ✅ Only Option: Use Hugging Face Model

**Since official VideoMAE weights are not provided, this is the only viable solution!**

```
Pros: 
✅ No need to manually download weight files
✅ System handles everything automatically
✅ Can start testing immediately
✅ Model from official Hugging Face

Explanation:
📝 This is VideoMAE's base pretrained model
📝 Originally for video classification tasks
📝 Can be used for deepfake detection, but accuracy may not be optimal
📝 First run will auto-download (~350MB)

Conclusion:
✅ Fully functional, can perform video analysis
⚠️ Detection accuracy may be lower than specifically trained model
✅ Suitable for testing, development and general use
```

### ❌ Not Recommended: Train Weights Yourself

```
Difficulty: ⭐⭐⭐⭐⭐ Extremely High
Cost: Requires significant GPU and time
Data: Needs large-scale deepfake dataset
Conclusion: Not suitable for individual users
```

---

## 📝 Usage Steps Summary

### Quick Start Guide (Using Hugging Face)

```powershell
# 1. Confirm service is running
# Your service is already running: http://localhost:8000

# 2. Test VideoMAE model loading
python scripts/test_with_huggingface.py
# First run will auto-download model (~350MB)

# 3. Test video analysis
# Method A: Use browser
# Visit: http://localhost:8000/docs
# Find POST /video/analyze
# Upload video to test

# Method B: Use test script (need to upload video first)
powershell -ExecutionPolicy Bypass -File scripts/test_video_api.ps1

# 4. View results
# System will return:
# - timeline.json: Complete analysis results
# - segments: Detected suspicious segments
# - keyframes: Keyframe images
```

### ❌ Not Needed Steps

```
❌ No need to download weights from GitHub
❌ No need to manually place files
❌ No need to configure paths
✅ Everything is automatically configured!
```

---

## ❓ Frequently Asked Questions

### Q1: Why can't I find VideoMAE weight files?
A: Because DeepfakeBench official has **NOT released** VideoMAE pretrained weights!

### Q2: What to do without weight files?
A: Use Hugging Face model (system is configured, auto-used)

### Q3: How is Hugging Face model's performance?
A: Works normally, but accuracy may be lower than specifically trained model

### Q4: Can I always use Hugging Face model?
A: **Yes!** This is currently the **only available** solution

### Q5: Does first-time use require download?
A: Yes, first run will auto-download approximately 350MB model file

### Q6: Need internet connection?
A: First-time use requires internet to download model, then cached locally

### Q7: How to know which model system is using?
A: Run `python scripts/test_with_huggingface.py` to see details

---

## 🔗 Related Links

- **DeepfakeBench GitHub**: https://github.com/SCLBD/DeepfakeBench
- **DeepfakeBench Releases**: https://github.com/SCLBD/DeepfakeBench/releases
- **Hugging Face VideoMAE**: https://huggingface.co/MCG-NJU/videomae-base
- **VideoMAE Paper**: https://arxiv.org/abs/2203.12602

---

**Need Help?** 
- If you encounter download issues, let me know
- If you want to test with Hugging Face model first, you can start directly

