import logging
import os
import json
import subprocess
import asyncio
import hashlib
import time
from pathlib import Path
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

# Job storage
jobs = {}

# Constants for video analysis
DATA_DIR = Path("data/jobs")
DATA_DIR.mkdir(parents=True, exist_ok=True)


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
MAX_VIDEO_SIZE = 500 * 1024 * 1024  # 500MB
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png"}
ALLOWED_VIDEO_TYPES = {
    "video/mp4", 
    "video/quicktime", 
    "video/x-msvideo",  # AVI
    "video/mpeg",
    "video/webm",
    "video/x-matroska",  # MKV
    "application/octet-stream"  # Generic binary, for some MP4 files
}


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


@app.post("/video/analyze")
async def analyze_video(file: UploadFile = File(...)):
    """
    Analyze video for deepfake detection and generate timeline
    Returns job_id for tracking progress
    """
    logger.info(f"Received video upload: filename={file.filename}, content_type={file.content_type}")
    
    # Validate file type
    if file.content_type not in ALLOWED_VIDEO_TYPES:
        logger.error(f"Unsupported file type: {file.content_type}")
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Allowed types: MP4, MOV, AVI, MPEG, WebM, MKV"
        )
    
    # Read file content
    content = await file.read()
    file_size_mb = len(content) / (1024 * 1024)
    logger.info(f"File size: {file_size_mb:.2f}MB")
    
    # Validate size
    if len(content) > MAX_VIDEO_SIZE:
        logger.error(f"File too large: {file_size_mb:.2f}MB > {MAX_VIDEO_SIZE/(1024*1024)}MB")
        raise HTTPException(
            status_code=400,
            detail=f"File too large: {file_size_mb:.1f}MB. Maximum size: 500MB"
        )
    
    # Generate job ID
    timestamp = int(time.time())
    file_hash = hashlib.sha256(content).hexdigest()[:12]
    job_id = f"job_{file_hash}_{timestamp}"
    
    # Create job directory
    job_dir = DATA_DIR / job_id
    job_dir.mkdir(parents=True, exist_ok=True)
    
    # Save input video
    input_path = job_dir / "input.mp4"
    with open(input_path, "wb") as f:
        f.write(content)
    
    logger.info(f"Created job {job_id} for video {file.filename} ({len(content)} bytes)")
    
    # Initialize job status
    jobs[job_id] = {
        "status": "processing",
        "job_id": job_id,
        "filename": file.filename,
        "created_at": timestamp,
        "progress": 0,
        "message": "Starting analysis..."
    }
    
    # Start analysis in background
    asyncio.create_task(run_video_analysis(job_id, str(input_path), str(job_dir)))
    
    return JSONResponse(content={"job_id": job_id})


async def run_video_analysis(job_id: str, input_path: str, output_dir: str):
    """Run video analysis in background"""
    try:
        logger.info(f"Starting OFFICIAL DeepfakeBench video analysis for job {job_id}")
        
        # Path to inference script
        inference_script = "vendors/DeepfakeBench/tools/video_inference.py"
        weights_path = "vendors/DeepfakeBench/training/weights/videomae_pretrained.pth"
        
        # Check if weights exist
        if not os.path.exists(weights_path):
            logger.warning(f"VideoMAE weights not found at {weights_path}")
            logger.warning("Please download official weights from: https://github.com/SCLBD/DeepfakeBench/releases")
        
        # Build command
        cmd = [
            "python",
            inference_script,
            "--input", input_path,
            "--out", output_dir,
            "--weights", weights_path,
            "--threshold-percentile", "85"
        ]
        
        logger.info(f"Running command: {' '.join(cmd)}")
        
        # Run subprocess
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Wait for completion
        stdout, stderr = await process.communicate()
        
        if process.returncode == 0:
            # Load timeline results
            timeline_path = Path(output_dir) / "timeline.json"
            if timeline_path.exists():
                with open(timeline_path, 'r') as f:
                    timeline = json.load(f)
                
                jobs[job_id].update({
                    "status": "completed",
                    "progress": 100,
                    "message": "Analysis complete",
                    "result": timeline
                })
                logger.info(f"Job {job_id} completed successfully using OFFICIAL pipeline")
            else:
                jobs[job_id].update({
                    "status": "error",
                    "message": "Timeline file not found"
                })
        else:
            error_msg = stderr.decode() if stderr else "Unknown error"
            logger.error(f"Job {job_id} failed: {error_msg}")
            jobs[job_id].update({
                "status": "error",
                "message": f"Analysis failed: {error_msg[:200]}"
            })
            
    except Exception as e:
        logger.error(f"Job {job_id} error: {e}")
        jobs[job_id].update({
            "status": "error",
            "message": str(e)
        })


@app.get("/video/jobs/{job_id}/status")
async def get_job_status(job_id: str):
    """Get job status and progress"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    # Check for progress updates from inference script
    job_dir = DATA_DIR / job_id
    progress_file = job_dir / "progress.json"
    
    if progress_file.exists():
        try:
            with open(progress_file, 'r') as f:
                progress_data = json.load(f)
                job.update({
                    "progress": progress_data.get("progress", job.get("progress", 0)),
                    "message": progress_data.get("message", job.get("message", "")),
                    "stage": progress_data.get("stage", "processing")
                })
        except Exception as e:
            logger.warning(f"Failed to read progress file: {e}")
    
    return JSONResponse(content=job)


@app.get("/video/jobs/{job_id}/result")
async def get_job_result(job_id: str):
    """Get complete analysis results"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    if job["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Job not completed. Current status: {job['status']}"
        )
    
    return JSONResponse(content=job.get("result", {}))


@app.get("/video/jobs/{job_id}/keyframes/{filename}")
async def get_keyframe(job_id: str, filename: str):
    """Serve keyframe images"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    keyframe_path = DATA_DIR / job_id / "keyframes" / filename
    
    if not keyframe_path.exists():
        raise HTTPException(status_code=404, detail="Keyframe not found")
    
    return FileResponse(keyframe_path)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)