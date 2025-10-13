#!/usr/bin/env python3
"""
Test script: Verify that ResNet50 model can be loaded correctly
"""

import os
import sys
import torch
import torchvision.models as models
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from app.adapters.local_resnet_adapter import LocalResNetAdapter


def test_model_loading():
    """Test model loading"""
    model_path = "deepfake_resnet50.pth"
    
    print(f"Checking model file: {model_path}")
    if not os.path.exists(model_path):
        print(f"❌ Model file not found: {model_path}")
        return False
    
    print(f"✅ Model file exists")
    
    try:
        print("Initializing model...")
        model = models.resnet50(pretrained=False)
        model.fc = torch.nn.Linear(model.fc.in_features, 2)
        
        print("Loading model weights...")
        checkpoint = torch.load(model_path, map_location='cpu')
        
        # Try different loading methods
        if isinstance(checkpoint, dict):
            if 'model_state_dict' in checkpoint:
                model.load_state_dict(checkpoint['model_state_dict'])
                print("✅ Successfully loaded using 'model_state_dict'")
            elif 'state_dict' in checkpoint:
                model.load_state_dict(checkpoint['state_dict'])
                print("✅ Successfully loaded using 'state_dict'")
            else:
                model.load_state_dict(checkpoint)
                print("✅ Successfully loaded dictionary directly")
        else:
            model.load_state_dict(checkpoint)
            print("✅ Successfully loaded weights directly")
        
        model.eval()
        print("✅ Model set to evaluation mode")
        
        # Test forward pass
        print("Testing forward pass...")
        dummy_input = torch.randn(1, 3, 224, 224)
        with torch.no_grad():
            output = model(dummy_input)
            print(f"✅ Output shape: {output.shape}")
            print(f"✅ Output value range: [{output.min().item():.4f}, {output.max().item():.4f}]")
        
        return True
        
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return False

def test_adapter():
    """Test adapter initialization"""
    try:
        print("\nTesting adapter initialization...")
        from app.adapters.local_resnet_adapter import LocalResNetAdapter
        
        adapter = LocalResNetAdapter(model_path="deepfake_resnet50.pth")
        print("✅ Adapter initialization successful")
        
        # Check device
        print(f"✅ Using device: {adapter.device}")
        
        return True
        
    except Exception as e:
        print(f"❌ Adapter initialization failed: {e}")
        return False

def main():
    """Main function"""
    print("🔍 Starting ResNet50 model test...")
    print("=" * 50)
    
    # Check PyTorch version
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA device count: {torch.cuda.device_count()}")
        print(f"Current CUDA device: {torch.cuda.current_device()}")
    
    print("=" * 50)
    
    # Test model loading
    model_ok = test_model_loading()
    
    if model_ok:
        # Test adapter
        adapter_ok = test_adapter()
        
        if adapter_ok:
            print("\n🎉 All tests passed! Model can be used normally.")
            print("\nTo start the service, run:")
            print("  python -m app.main")
            print("\nOr run with environment variable:")
            print("  USE_LOCAL_MODEL=true python -m app.main")
        else:
            print("\n❌ Adapter test failed")
            sys.exit(1)
    else:
        print("\n❌ Model loading test failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
