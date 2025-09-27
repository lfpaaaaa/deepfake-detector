#!/usr/bin/env python3
"""
Model Sharing Script for Team Members
Creates a compressed archive of model files for easy sharing
"""

import os
import zipfile
import tarfile
from pathlib import Path
from datetime import datetime

def create_model_archive():
    """Create a compressed archive of model files"""
    
    # Model files to include
    model_files = [
        "trufor.pth.tar",
        "deepfake_resnet50.pth", 
        "deepfake_resnet18.pth"
    ]
    
    # Check which files exist
    existing_files = []
    missing_files = []
    
    for file in model_files:
        if os.path.exists(file):
            existing_files.append(file)
            print(f"✅ Found: {file}")
        else:
            missing_files.append(file)
            print(f"❌ Missing: {file}")
    
    if not existing_files:
        print("❌ No model files found!")
        return False
    
    if missing_files:
        print(f"\n⚠️  Warning: {len(missing_files)} files are missing:")
        for file in missing_files:
            print(f"   - {file}")
        
        proceed = input("\nProceed with available files? (y/n): ").strip().lower()
        if proceed != 'y':
            print("❌ Archive creation cancelled.")
            return False
    
    # Create archive
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"deepfake_models_{timestamp}.zip"
    
    print(f"\n📦 Creating archive: {archive_name}")
    
    try:
        with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in existing_files:
                print(f"   Adding: {file}")
                zipf.write(file)
            
            # Add setup instructions
            zipf.writestr("README.txt", f"""
Deepfake Detection System - Model Files
======================================

This archive contains the model files for the Deepfake Detection System.

Files included:
{chr(10).join(f"- {file}" for file in existing_files)}

Setup Instructions:
1. Extract all files to the project root directory
2. Run: python start_trufor.py
3. Open: http://localhost:8000

For more information, see MODEL_SETUP.md in the project repository.

Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
""")
        
        # Get archive size
        archive_size = os.path.getsize(archive_name)
        size_mb = archive_size / (1024 * 1024)
        
        print(f"✅ Archive created successfully!")
        print(f"   File: {archive_name}")
        print(f"   Size: {size_mb:.1f} MB")
        print(f"   Files: {len(existing_files)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create archive: {e}")
        return False

def main():
    """Main function"""
    print("🤖 Deepfake Detection System - Model Sharing Tool")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("app") or not os.path.exists("requirements.txt"):
        print("❌ Please run this script from the project root directory!")
        return
    
    print("This script will create a compressed archive of model files")
    print("that can be easily shared with team members.")
    print()
    
    # Create the archive
    if create_model_archive():
        print("\n📤 Sharing Instructions:")
        print("1. Send the generated .zip file to your team members")
        print("2. Team members should extract it to their project root directory")
        print("3. They can then run: python start_trufor.py")
        print("\n💡 Tip: Use cloud storage (Google Drive, Dropbox) for large files")
    else:
        print("\n❌ Archive creation failed!")

if __name__ == "__main__":
    main()


