#!/usr/bin/env python3
"""
Start the deepfake detection service with TruFor model
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set environment variables for TruFor
os.environ["MODEL_TYPE"] = "trufor"
os.environ["MODEL_PATH"] = "trufor.pth.tar"

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

if __name__ == "__main__":
    import uvicorn
    from main import app
    
    print("Starting Deepfake Detection Service with TruFor model...")
    print("Model: TruFor")
    print("Model Path: trufor.pth.tar")
    print("Server will be available at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)


