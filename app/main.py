import logging
import os
import json
import subprocess
import asyncio
import hashlib
import time
from pathlib import Path
from contextlib import asynccontextmanager
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
try:
    # Try relative imports first (when run from app directory)
    from adapters.trufor_adapter import TruForAdapter
    from adapters.deepfakebench_adapter import DeepfakeBenchAdapter
except ImportError:
    # Fallback to absolute imports (when run from project root)
    from app.adapters.trufor_adapter import TruForAdapter
    from app.adapters.deepfakebench_adapter import DeepfakeBenchAdapter
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

# Thread pool for CPU-intensive tasks
executor = ThreadPoolExecutor(max_workers=2)

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
        # Initialize TruFor model
        model_path = os.getenv("MODEL_PATH", "trufor.pth.tar")
        if os.path.exists(model_path):
            detection_adapter = TruForAdapter(model_path=model_path)
            logger.info("TruFor adapter initialized successfully")
        else:
            logger.warning(f"TruFor model not found at {model_path}, adapter not initialized")
            detection_adapter = None
            
    except Exception as e:
        logger.error(f"Failed to initialize detection adapter: {e}")
        logger.warning("Server will start without TruFor model loaded")
        detection_adapter = None
    yield
    logger.info("Shutting down application")


app = FastAPI(
    title="Deepfake Detection API",
    version="1.0.0",
    description="Deepfake detection service supporting TruFor and DeepfakeBench models",
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


# =============================================================================
# DeepfakeBench API Endpoints
# =============================================================================

@app.get("/api/deepfakebench/models")
async def get_deepfakebench_models():
    """Get list of available DeepfakeBench models"""
    try:
        models = DeepfakeBenchAdapter.get_available_models()
        return JSONResponse(content={"models": models})
    except Exception as e:
        logger.error(f"Failed to get models: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/deepfakebench/analyze")
async def analyze_with_deepfakebench(
    file: UploadFile = File(...),
    model: str = Form("xception"),
    fps: float = Form(3.0),
    threshold: float = Form(0.5)
):
    """
    Analyze video using DeepfakeBench models
    
    Parameters:
    - file: Video file
    - model: Model key (e.g., 'xception', 'meso4', 'f3net')
    - fps: Frame sampling rate (default: 3.0)
    - threshold: Detection threshold (default: 0.5)
    """
    # Validate file type
    if file.content_type not in ALLOWED_VIDEO_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type: {file.content_type}. Allowed: {', '.join(ALLOWED_VIDEO_TYPES)}"
        )
    
    # Read file content
    content = await file.read()
    file_size_mb = len(content) / (1024 * 1024)
    logger.info(f"DeepfakeBench analysis request - File: {file.filename}, Size: {file_size_mb:.2f}MB, Model: {model}")
    
    # Validate size
    if len(content) > MAX_VIDEO_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large: {file_size_mb:.1f}MB. Maximum size: 500MB"
        )
    
    # Generate job ID
    timestamp = int(time.time())
    file_hash = hashlib.sha256(content).hexdigest()[:12]
    job_id = f"dfb_{file_hash}_{timestamp}"
    
    logger.info(f"Created DeepfakeBench job {job_id} for video {file.filename}")
    
    # Initialize job status FIRST (before saving file)
    jobs[job_id] = {
        "status": "processing",
        "job_id": job_id,
        "filename": file.filename,
        "model": model,
        "created_at": timestamp,
        "progress": 0,
        "stage": "Uploading...",
        "message": f"Preparing to analyze with {model}"
    }
    
    # Start analysis in background thread (to avoid blocking event loop)
    loop = asyncio.get_event_loop()
    loop.run_in_executor(
        executor,
        run_deepfakebench_analysis_sync,
        job_id, content, model, fps, threshold
    )
    
    # Return job_id IMMEDIATELY (before file is saved)
    return JSONResponse(content={"job_id": job_id, "model": model})


def run_deepfakebench_analysis_sync(job_id: str, content: bytes, model: str, fps: float, threshold: float):
    """Save video file and run DeepfakeBench analysis in background thread (synchronous for ThreadPoolExecutor)"""
    try:
        # Create job directory
        job_dir = DATA_DIR / job_id
        job_dir.mkdir(parents=True, exist_ok=True)
        
        # Update progress - saving file
        jobs[job_id].update({
            "progress": 5,
            "stage": "Saving file...",
            "message": "Writing video to disk"
        })
        
        # Save input video
        input_path = job_dir / "input.mp4"
        with open(input_path, "wb") as f:
            f.write(content)
        
        logger.info(f"Saved video file for job {job_id}, starting analysis")
        
        # Now run the analysis (synchronous call since we're already in a thread)
        run_deepfakebench_analysis(job_id, str(input_path), model, fps, threshold)
        
    except Exception as e:
        logger.error(f"Failed to save/analyze video for job {job_id}: {e}")
        jobs[job_id].update({
            "status": "error",
            "message": f"Failed to save video: {str(e)}"
        })


def run_deepfakebench_analysis(job_id: str, video_path: str, model: str, fps: float, threshold: float):
    """Run DeepfakeBench analysis in background (synchronous for ThreadPoolExecutor)"""
    try:
        logger.info(f"Starting DeepfakeBench analysis for job {job_id} with model {model}")
        
        # Get job directory for progress file
        job_dir = DATA_DIR / job_id
        
        jobs[job_id].update({
            "progress": 10,
            "stage": "Loading model...",
            "message": f"Initializing {model}"
        })
        
        # Initialize adapter
        adapter = DeepfakeBenchAdapter(model_key=model, device="cuda")
        
        # Progress callback - write to file like TruFor does
        def update_progress(progress, stage, message):
            jobs[job_id].update({
                "progress": progress,
                "stage": stage,
                "message": message
            })
            # Write to progress.json file for polling
            progress_file = job_dir / "progress.json"
            try:
                with open(progress_file, 'w') as f:
                    json.dump({
                        "progress": progress,
                        "stage": stage,
                        "message": message
                    }, f)
                logger.info(f"📊 Progress updated: {progress}% - {stage} - {message}")
            except Exception as e:
                logger.warning(f"Failed to write progress file: {e}")
        
        # Initial progress update
        update_progress(30, "Analyzing video...", "Starting frame analysis")
        
        # Run analysis with progress callback
        result = adapter.analyze_video(video_path, fps=fps, threshold=threshold, progress_callback=update_progress)
        
        if result["success"]:
            update_progress(95, "Generating report...", "Finalizing results")
            
            jobs[job_id].update({
                "status": "completed",
                "progress": 100,
                "stage": "Complete",
                "message": "Analysis finished",
                "result": result
            })
            update_progress(100, "Complete", "Analysis finished")
            logger.info(f"Job {job_id} completed successfully")
        else:
            jobs[job_id].update({
                "status": "error",
                "message": result.get("error", "Analysis failed")
            })
            
    except Exception as e:
        logger.error(f"DeepfakeBench analysis failed for job {job_id}: {e}")
        import traceback
        traceback.print_exc()
        jobs[job_id].update({
            "status": "error",
            "message": f"Analysis failed: {str(e)}"
        })


@app.get("/api/deepfakebench/jobs/{job_id}")
async def get_deepfakebench_job(job_id: str):
    """Get DeepfakeBench job status"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    # Check for progress updates from progress.json file (like TruFor does)
    job_dir = DATA_DIR / job_id
    progress_file = job_dir / "progress.json"
    
    if progress_file.exists():
        try:
            with open(progress_file, 'r') as f:
                progress_data = json.load(f)
                job.update({
                    "progress": progress_data.get("progress", job.get("progress", 0)),
                    "message": progress_data.get("message", job.get("message", "")),
                    "stage": progress_data.get("stage", job.get("stage", "processing"))
                })
                logger.info(f"📨 Sending progress to frontend: {job.get('progress')}% - {job.get('stage')} - {job.get('message')}")
        except Exception as e:
            logger.warning(f"Failed to read progress file: {e}")
    else:
        logger.debug(f"Progress file not found for job {job_id}")
    
    return JSONResponse(content=job)


@app.post("/api/deepfakebench/jobs/{job_id}/extract-keyframe")
async def extract_keyframe(job_id: str, timestamp: float = 0.0):
    """Extract a keyframe at the specified timestamp"""
    import cv2
    
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Get video path
    job_dir = DATA_DIR / job_id
    video_path = job_dir / "input.mp4"
    
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video file not found")
    
    try:
        # Open video
        cap = cv2.VideoCapture(str(video_path))
        
        if not cap.isOpened():
            raise HTTPException(status_code=500, detail="Failed to open video")
        
        # Get video properties
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_duration = total_frames / video_fps if video_fps > 0 else 0
        
        # AGGRESSIVE boundary handling: if timestamp is in last 40% of video, use middle region instead
        # This is because many videos have corrupted frames near the end
        if timestamp > video_duration * 0.6:
            # Map to safe middle region (30% of video duration)
            fallback_timestamp = video_duration * 0.35
            logger.warning(f"⚠️ Timestamp {timestamp:.2f}s is in potentially corrupted end region (>{video_duration*0.6:.2f}s), using fallback at {fallback_timestamp:.2f}s")
            timestamp = fallback_timestamp
        
        # Calculate frame number
        frame_number = int(timestamp * video_fps)
        
        # Ensure frame_number is within safe range (use only first 70% of frames to avoid corruption)
        safe_max_frame = max(0, int(total_frames * 0.7))
        if frame_number > safe_max_frame:
            frame_number = safe_max_frame
            logger.warning(f"⚠️ Frame {int(timestamp * video_fps)} exceeds safe range, capped to frame {safe_max_frame} (70% of video)")
        
        frame_number = max(0, frame_number)
        
        # Seek to frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        
        # Read frame with multiple retries
        ret, frame = cap.read()
        
        # If failed, try multiple previous frames (important for video end)
        retry_attempts = 15  # Try up to 15 frames back
        attempt = 0
        while not ret and attempt < retry_attempts and frame_number - attempt > 0:
            attempt += 1
            retry_frame = frame_number - attempt
            logger.warning(f"Failed to read frame {frame_number - attempt + 1}, trying frame {retry_frame}")
            cap.set(cv2.CAP_PROP_POS_FRAMES, retry_frame)
            ret, frame = cap.read()
        
        cap.release()
        
        if not ret:
            raise HTTPException(status_code=500, detail=f"Failed to extract frame at {timestamp:.2f}s (tried frames {frame_number} to {max(0, frame_number - retry_attempts)})")
        
        # Create keyframes directory
        keyframes_dir = job_dir / "keyframes"
        keyframes_dir.mkdir(exist_ok=True)
        
        # Generate filename based on timestamp
        keyframe_filename = f"keyframe_{timestamp:.2f}s.jpg"
        keyframe_path = keyframes_dir / keyframe_filename
        
        # Save keyframe
        cv2.imwrite(str(keyframe_path), frame)
        
        logger.info(f"Extracted keyframe for job {job_id} at {timestamp:.2f}s -> {keyframe_filename}")
        
        return JSONResponse(content={
            "success": True,
            "keyframe_path": f"keyframes/{keyframe_filename}",
            "timestamp": timestamp
        })
        
    except Exception as e:
        logger.error(f"Failed to extract keyframe: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to extract keyframe: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)