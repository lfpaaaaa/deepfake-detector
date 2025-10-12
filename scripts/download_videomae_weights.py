"""
Download VideoMAE weights for DeepfakeBench
Downloads from GitHub releases or Hugging Face
"""
import os
import sys
import urllib.request
from pathlib import Path
import hashlib

def download_file(url, dest_path, desc="Downloading"):
    """Download file with progress bar"""
    def reporthook(count, block_size, total_size):
        percent = int(count * block_size * 100 / total_size)
        sys.stdout.write(f"\r{desc}: {percent}% ")
        sys.stdout.flush()
    
    print(f"Downloading from: {url}")
    print(f"Saving to: {dest_path}")
    
    try:
        urllib.request.urlretrieve(url, dest_path, reporthook)
        print("\n✅ Download complete!")
        return True
    except Exception as e:
        print(f"\n❌ Download failed: {e}")
        return False

def main():
    # Target directory
    weights_dir = Path("vendors/DeepfakeBench/training/weights")
    weights_dir.mkdir(parents=True, exist_ok=True)
    
    # Target file
    weights_file = weights_dir / "videomae_pretrained.pth"
    
    # Check if already exists
    if weights_file.exists():
        size_mb = weights_file.stat().st_size / (1024 * 1024)
        print(f"⚠️  Weights file already exists: {weights_file}")
        print(f"   Size: {size_mb:.2f} MB")
        response = input("Do you want to re-download? (y/n): ")
        if response.lower() != 'y':
            print("Skipping download.")
            return
    
    print("\n" + "="*60)
    print("📥 VideoMAE Weights Download")
    print("="*60)
    print()
    print("⚠️  IMPORTANT: DeepfakeBench weights are hosted on GitHub Releases")
    print()
    print("Please follow these steps:")
    print()
    print("1. Open your browser and visit:")
    print("   🔗 https://github.com/SCLBD/DeepfakeBench/releases/tag/v1.0.1")
    print()
    print("2. Look for 'videomae_pretrained.pth' or similar VideoMAE weights")
    print()
    print("3. Download the file to:")
    print(f"   📁 {weights_file.absolute()}")
    print()
    print("4. The file should be approximately 350-400 MB")
    print()
    print("="*60)
    print()
    
    # Try direct download (may not work due to GitHub's download mechanism)
    print("Attempting direct download...")
    print("(Note: This may fail due to GitHub's download mechanism)")
    print()
    
    # Known direct download URLs (these might be outdated)
    possible_urls = [
        "https://github.com/SCLBD/DeepfakeBench/releases/download/v1.0.1/videomae_pretrained.pth",
        "https://github.com/SCLBD/DeepfakeBench/releases/download/v1.0.1/videomae_best.pth",
    ]
    
    for url in possible_urls:
        print(f"\nTrying: {url}")
        if download_file(url, str(weights_file), "Downloading VideoMAE weights"):
            # Verify file size
            size_mb = weights_file.stat().st_size / (1024 * 1024)
            print(f"✅ File downloaded successfully: {size_mb:.2f} MB")
            
            if size_mb < 10:
                print("⚠️  Warning: File size is suspiciously small.")
                print("   This might be an error page instead of the actual weights.")
                weights_file.unlink()
                continue
            else:
                print("\n" + "="*60)
                print("✅ VideoMAE Weights Ready!")
                print("="*60)
                print(f"📁 Location: {weights_file.absolute()}")
                print(f"📊 Size: {size_mb:.2f} MB")
                print()
                print("You can now test video analysis!")
                return
    
    print("\n" + "="*60)
    print("⚠️  Automatic download failed")
    print("="*60)
    print()
    print("Please download manually:")
    print("1. Visit: https://github.com/SCLBD/DeepfakeBench/releases")
    print("2. Find VideoMAE weights (usually in v1.0.1 or later)")
    print("3. Save as: " + str(weights_file.absolute()))
    print()

if __name__ == "__main__":
    main()

