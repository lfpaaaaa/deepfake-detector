#!/usr/bin/env python3
"""
Startup script: Launch deepfake detection service using local ResNet50 model
"""

import os
import sys
import uvicorn
from pathlib import Path

def main():
    """Start local model service"""
    
    # Set model path (optional, defaults to deepfake_resnet50.pth)
    os.environ["MODEL_PATH"] = "deepfake_resnet50.pth"
    
    # Check if model file exists
    model_path = Path("deepfake_resnet50.pth")
    if not model_path.exists():
        print("❌ Error: Model file 'deepfake_resnet50.pth' not found")
        print("Please ensure the model file is in the current directory")
        sys.exit(1)
    
    print("🚀 Starting Deepfake Detection Service (using local ResNet50 model)")
    print("=" * 60)
    print(f"📁 Model file: {model_path.absolute()}")
    print(f"🌐 Service URL: http://localhost:8000")
    print(f"📖 API docs: http://localhost:8000/docs")
    print(f"🖥️  Web interface: http://localhost:8000/")
    print("=" * 60)
    print("Press Ctrl+C to stop the service")
    print()
    
    try:
        # Start service
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=False,  # Recommended to set False for production
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Service stopped")
    except Exception as e:
        print(f"❌ Startup failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
