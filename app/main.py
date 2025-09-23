import logging
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
try:
    # Try relative imports first (when run from app directory)
    from adapters.local_resnet_adapter import LocalResNetAdapter
    from adapters.trufor_adapter import TruForAdapter
except ImportError:
    # Fallback to absolute imports (when run from project root)
    from app.adapters.local_resnet_adapter import LocalResNetAdapter
    from app.adapters.trufor_adapter import TruForAdapter
import uvicorn

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize adapter as global variable
detection_adapter = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize resources on startup"""
    global detection_adapter
    try:
        # Get model type from environment variable
        model_type = os.getenv("MODEL_TYPE", "resnet50").lower()
        
        if model_type == "trufor":
            # Initialize TruFor model
            model_path = os.getenv("MODEL_PATH", "trufor.pth.tar")
            detection_adapter = TruForAdapter(model_path=model_path)
            logger.info("TruFor adapter initialized successfully")
        else:
            # Initialize local ResNet50 model (default)
            model_path = os.getenv("MODEL_PATH", "deepfake_resnet50.pth")
            detection_adapter = LocalResNetAdapter(model_path=model_path)
            logger.info("Local ResNet50 adapter initialized successfully")
            
    except Exception as e:
        logger.error(f"Failed to initialize detection adapter: {e}")
        raise
    yield
    logger.info("Shutting down application")


app = FastAPI(
    title="Deepfake Detection API",
    version="1.0.0",
    description="Local deepfake detection service supporting ResNet50 and TruFor models",
    lifespan=lifespan
)

# Mount static files
app.mount("/web", StaticFiles(directory="app/web"), name="web")
app.mount("/static", StaticFiles(directory=".", html=True), name="static")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Constants
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_VIDEO_SIZE = 50 * 1024 * 1024  # 50MB
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png"}
ALLOWED_VIDEO_TYPES = {"video/mp4", "video/quicktime"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "deepfake-detection"}


@app.post("/detect")
async def detect_deepfake(file: UploadFile = File(...)):
    """
    Detect deepfakes in uploaded media files
    
    Accepts:
    - Images: JPEG, PNG (max 10MB)
    - Videos: MP4, MOV (max 50MB)
    
    Returns detection results including confidence score and verdict
    """
    # Validate MIME type
    mime_type = file.content_type
    if mime_type not in (ALLOWED_IMAGE_TYPES | ALLOWED_VIDEO_TYPES):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {mime_type}. Allowed: JPEG, PNG, MP4, MOV"
        )
    
    # Read file content
    content = await file.read()
    
    # Validate file size
    is_video = mime_type in ALLOWED_VIDEO_TYPES
    max_size = MAX_VIDEO_SIZE if is_video else MAX_IMAGE_SIZE
    if len(content) > max_size:
        size_limit_mb = max_size // (1024 * 1024)
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {size_limit_mb}MB"
        )
    
    # Log request (without content)
    media_type = "video" if is_video else "image"
    logger.info(f"Processing {media_type}: {file.filename} ({len(content)} bytes)")
    
    try:
        # Call detection adapter
        result = await detection_adapter.detect(
            file_bytes=content,
            filename=file.filename,
            mime_type=mime_type
        )
        
        logger.info(f"Detection complete for {file.filename}: {result['status']}")
        return JSONResponse(content=result)
        
    except TimeoutError:
        logger.error(f"Timeout processing {file.filename}")
        raise HTTPException(
            status_code=504,
            detail="Detection timeout - file may be too complex"
        )
    except Exception as e:
        logger.error(f"Detection failed for {file.filename}: {e}")
        # Check if it's a vendor service issue
        if "reality defender" in str(e).lower():
            raise HTTPException(
                status_code=503,
                detail="Detection service temporarily unavailable"
            )
        raise HTTPException(
            status_code=500,
            detail="Detection failed - please try again"
        )


@app.get("/", response_class=FileResponse)
async def root():
    """Serve the main HTML page"""
    return FileResponse('app/web/index.html')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)