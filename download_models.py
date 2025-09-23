#!/usr/bin/env python3
"""
Model Download Script for Deepfake Detection System
Downloads required model files for team members
"""

import os
import requests
import hashlib
from pathlib import Path
from tqdm import tqdm

# Model configurations
MODELS = {
    "trufor.pth.tar": {
        "url": "https://github.com/grip-unina/TruFor/releases/download/v1.0/trufor.pth.tar",
        "size": "~500MB",
        "description": "TruFor model weights"
    },
    "deepfake_resnet50.pth": {
        "url": "https://example.com/deepfake_resnet50.pth",  # Replace with actual URL
        "size": "~100MB", 
        "description": "ResNet50 model weights"
    },
    "deepfake_resnet18.pth": {
        "url": "https://example.com/deepfake_resnet18.pth",  # Replace with actual URL
        "size": "~50MB",
        "description": "ResNet18 model weights"
    }
}

def download_file(url: str, filename: str, description: str) -> bool:
    """Download a file with progress bar"""
    try:
        print(f"Downloading {description}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(filename, 'wb') as file, tqdm(
            desc=filename,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for chunk in response.iter_content(chunk_size=8192):
                size = file.write(chunk)
                pbar.update(size)
        
        print(f"✅ {description} downloaded successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to download {description}: {e}")
        return False

def main():
    """Main download function"""
    print("🤖 Deepfake Detection System - Model Downloader")
    print("=" * 50)
    
    # Create models directory if it doesn't exist
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    
    print("Available models:")
    for i, (filename, info) in enumerate(MODELS.items(), 1):
        print(f"{i}. {filename} ({info['size']}) - {info['description']}")
    
    print("\nSelect models to download:")
    print("1. Download all models")
    print("2. Download TruFor only")
    print("3. Download ResNet models only")
    print("4. Download specific model")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        # Download all models
        for filename, info in MODELS.items():
            if not os.path.exists(filename):
                download_file(info["url"], filename, info["description"])
            else:
                print(f"⏭️  {filename} already exists, skipping...")
    
    elif choice == "2":
        # Download TruFor only
        filename = "trufor.pth.tar"
        info = MODELS[filename]
        if not os.path.exists(filename):
            download_file(info["url"], filename, info["description"])
        else:
            print(f"⏭️  {filename} already exists, skipping...")
    
    elif choice == "3":
        # Download ResNet models only
        for filename in ["deepfake_resnet50.pth", "deepfake_resnet18.pth"]:
            if filename in MODELS:
                info = MODELS[filename]
                if not os.path.exists(filename):
                    download_file(info["url"], filename, info["description"])
                else:
                    print(f"⏭️  {filename} already exists, skipping...")
    
    elif choice == "4":
        # Download specific model
        print("\nAvailable models:")
        for i, (filename, info) in enumerate(MODELS.items(), 1):
            print(f"{i}. {filename} ({info['size']})")
        
        model_choice = input("Enter model number: ").strip()
        try:
            model_index = int(model_choice) - 1
            filename = list(MODELS.keys())[model_index]
            info = MODELS[filename]
            
            if not os.path.exists(filename):
                download_file(info["url"], filename, info["description"])
            else:
                print(f"⏭️  {filename} already exists, skipping...")
        except (ValueError, IndexError):
            print("❌ Invalid choice!")
    
    else:
        print("❌ Invalid choice!")
    
    print("\n🎉 Model download process completed!")
    print("\nNext steps:")
    print("1. Run: python start_trufor.py")
    print("2. Open: http://localhost:8000")

if __name__ == "__main__":
    main()


