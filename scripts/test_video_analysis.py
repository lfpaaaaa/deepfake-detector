"""
Test video analysis with VideoMAE detector
Can use either local weights or Hugging Face model
"""
import sys
import os
from pathlib import Path
import torch
from transformers import VideoMAEImageProcessor, VideoMAEForVideoClassification

def test_videomae_model():
    """Test if VideoMAE model can be loaded"""
    print("\n" + "="*60)
    print("🧪 Testing VideoMAE Model")
    print("="*60)
    
    weights_path = Path("vendors/DeepfakeBench/training/weights/videomae_pretrained.pth")
    
    print(f"\n📊 Device: {'CUDA' if torch.cuda.is_available() else 'CPU'}")
    
    # Check for local weights
    if weights_path.exists():
        size_mb = weights_path.stat().st_size / (1024 * 1024)
        print(f"\n✅ Local weights found: {weights_path}")
        print(f"   Size: {size_mb:.2f} MB")
        print("   Will use local weights for analysis")
    else:
        print(f"\n⚠️  Local weights not found: {weights_path}")
        print("\n📥 Testing Hugging Face VideoMAE model...")
        
        try:
            # Try to load from Hugging Face
            print("   Loading VideoMAE from Hugging Face (MCG-NJU/videomae-base)...")
            print("   This will download the model (~350MB) on first use...")
            
            processor = VideoMAEImageProcessor.from_pretrained("MCG-NJU/videomae-base")
            model = VideoMAEForVideoClassification.from_pretrained(
                "MCG-NJU/videomae-base",
                num_labels=2,  # Binary classification: real/fake
                ignore_mismatched_sizes=True
            )
            
            print("   ✅ Model loaded successfully from Hugging Face!")
            print("   Note: This model needs fine-tuning for deepfake detection")
            print("   For best results, download DeepfakeBench trained weights")
            
            return True, "huggingface"
            
        except Exception as e:
            print(f"   ❌ Failed to load Hugging Face model: {e}")
            return False, None
    
    return True, "local"

def find_test_video():
    """Find a test video in the data directory"""
    data_dir = Path("data/jobs")
    
    if not data_dir.exists():
        print("\n⚠️  No test videos found in data/jobs/")
        return None
    
    # Look for any .mp4 file
    for job_dir in data_dir.iterdir():
        if job_dir.is_dir():
            input_video = job_dir / "input.mp4"
            if input_video.exists():
                return input_video
    
    print("\n⚠️  No test videos found")
    print("   Please upload a video through the web interface first")
    return None

def check_inference_script():
    """Check if inference script exists"""
    script_path = Path("vendors/DeepfakeBench/tools/video_inference.py")
    
    if not script_path.exists():
        print(f"\n❌ Inference script not found: {script_path}")
        return False
    
    print(f"\n✅ Inference script found: {script_path}")
    return True

def main():
    print("\n" + "="*70)
    print("🎥 VideoMAE Video Analysis Test")
    print("="*70)
    
    # 1. Check inference script
    if not check_inference_script():
        print("\n❌ Test failed: Missing inference script")
        return
    
    # 2. Test model loading
    model_ok, model_type = test_videomae_model()
    
    if not model_ok:
        print("\n" + "="*70)
        print("❌ Test Failed: Cannot load VideoMAE model")
        print("="*70)
        print("\n📋 To fix this:")
        print("1. Download VideoMAE weights manually from:")
        print("   https://github.com/SCLBD/DeepfakeBench/releases")
        print("2. Or ensure you have internet connection for Hugging Face")
        return
    
    # 3. Check for test video
    test_video = find_test_video()
    
    print("\n" + "="*70)
    print("✅ VideoMAE Setup Complete!")
    print("="*70)
    print(f"\n📊 Model source: {model_type}")
    print(f"📁 Inference script: vendors/DeepfakeBench/tools/video_inference.py")
    
    if test_video:
        print(f"🎬 Test video found: {test_video}")
        print("\n💡 You can now test video analysis:")
        print(f"   python vendors/DeepfakeBench/tools/video_inference.py \\")
        print(f"     --input {test_video} \\")
        print(f"     --out test_output \\")
        print(f"     --weights vendors/DeepfakeBench/training/weights/videomae_pretrained.pth \\")
        print(f"     --threshold-percentile 85")
    else:
        print("\n🌐 Service is running at: http://localhost:8000")
        print("   Upload a video through the web interface to test analysis")
    
    print("\n" + "="*70)
    print()
    
    # Show weights download instructions
    weights_path = Path("vendors/DeepfakeBench/training/weights/videomae_pretrained.pth")
    if not weights_path.exists():
        print("⚠️  For better performance, download trained weights:")
        print()
        print("Option 1: Manual Download")
        print("   1. Visit: https://github.com/SCLBD/DeepfakeBench/releases")
        print("   2. Look for VideoMAE weights (check all releases)")
        print("   3. Save to: vendors/DeepfakeBench/training/weights/videomae_pretrained.pth")
        print()
        print("Option 2: Use Hugging Face (current)")
        print("   The system will use Hugging Face's base model")
        print("   This works but may have lower accuracy")
        print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

