"""
Test VideoMAE with Hugging Face model
Since DeepfakeBench doesn't provide pretrained VideoMAE weights,
we'll use Hugging Face's model instead
"""
import sys
import torch
from transformers import VideoMAEImageProcessor, VideoMAEForVideoClassification

print("\n" + "="*70)
print("🧪 Testing VideoMAE with Hugging Face")
print("="*70)
print()

# Check device
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"📊 Device: {device}")
print()

print("📥 Loading VideoMAE from Hugging Face...")
print("   Model: MCG-NJU/videomae-base")
print("   This will download ~350MB on first use")
print()

try:
    # Load processor
    print("   Loading image processor...")
    processor = VideoMAEImageProcessor.from_pretrained("MCG-NJU/videomae-base")
    print("   ✅ Processor loaded")
    
    # Load model
    print("   Loading model...")
    model = VideoMAEForVideoClassification.from_pretrained(
        "MCG-NJU/videomae-base",
        num_labels=2,  # Binary: real/fake
        ignore_mismatched_sizes=True
    )
    model.to(device)
    model.eval()
    print("   ✅ Model loaded")
    
    print()
    print("="*70)
    print("✅ VideoMAE is ready to use!")
    print("="*70)
    print()
    print("📝 Model Details:")
    print(f"   - Source: Hugging Face (MCG-NJU/videomae-base)")
    print(f"   - Device: {device}")
    print(f"   - Parameters: {sum(p.numel() for p in model.parameters()):,}")
    print(f"   - Trainable: {sum(p.numel() for p in model.parameters() if p.requires_grad):,}")
    print()
    print("⚠️  Note: This is a base model, not specifically trained for deepfake")
    print("   It will work but accuracy may be lower than a trained model")
    print()
    print("🚀 You can now test video analysis:")
    print("   1. Go to http://localhost:8000/docs")
    print("   2. Use POST /video/analyze")
    print("   3. Upload a video and test!")
    print()
    
except Exception as e:
    print()
    print("="*70)
    print("❌ Failed to load model")
    print("="*70)
    print(f"Error: {e}")
    print()
    print("Possible reasons:")
    print("1. No internet connection")
    print("2. Hugging Face is blocked")
    print("3. Missing dependencies")
    print()
    sys.exit(1)

