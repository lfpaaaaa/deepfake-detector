"""
DeepfakeBench Adapter for Web API
Provides unified interface for 13 DeepfakeBench models
"""

import os
import sys
import logging
import cv2
import json
import numpy as np
import torch
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import deque

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from tools.weight_registry import WEIGHT_REGISTRY
from tools.build_dfbench_model import build_model_and_transforms

logger = logging.getLogger(__name__)


class DeepfakeBenchAdapter:
    """Adapter for DeepfakeBench models with video analysis and visualization."""
    
    # Available models
    AVAILABLE_MODELS = {
        "xception": {"name": "Xception", "speed": "Medium", "accuracy": "High"},
        "meso4": {"name": "MesoNet-4", "speed": "Fast", "accuracy": "Medium"},
        "f3net": {"name": "F3Net", "speed": "Medium", "accuracy": "High"},
        "efficientnetb4": {"name": "EfficientNet-B4", "speed": "Medium", "accuracy": "High"},
        "capsule_net": {"name": "Capsule Net", "speed": "Very Fast", "accuracy": "Medium"},
        "recce": {"name": "RECCE", "speed": "Medium", "accuracy": "High"},
        "spsl": {"name": "SPSL", "speed": "Medium", "accuracy": "High"},
        "ffd": {"name": "FFD", "speed": "Medium", "accuracy": "High"},
        "ucf": {"name": "UCF", "speed": "Medium", "accuracy": "High"},
        "multi_attention": {"name": "CNN-AUG", "speed": "Medium", "accuracy": "High"},
        "core": {"name": "CORE", "speed": "Medium", "accuracy": "High"},
        "srm": {"name": "SRM", "speed": "Medium", "accuracy": "High"},
        "meso4Inception": {"name": "MesoNet-4 Inception", "speed": "Fast", "accuracy": "Medium"},
    }
    
    def __init__(self, model_key: str = "xception", device: str = "cuda"):
        """
        Initialize DeepfakeBench adapter.
        
        Args:
            model_key: Model identifier (e.g., 'xception', 'meso4')
            device: Device to use ('cuda' or 'cpu')
        """
        self.model_key = model_key
        self.device = device if torch.cuda.is_available() and device == "cuda" else "cpu"
        self.model = None
        self.transform_fn = None
        self.input_size = None
        self.weights_dir = "vendors/DeepfakeBench/training/weights"
        
        logger.info(f"Initializing DeepfakeBench adapter with model: {model_key}, device: {self.device}")
        self._load_model()
    
    def _load_model(self):
        """Load the specified DeepfakeBench model."""
        try:
            # Find weight file and input size
            weight_filename = None
            for wf, meta in WEIGHT_REGISTRY.items():
                if meta["model_key"] == self.model_key:
                    weight_filename = wf
                    self.input_size = meta["input_size"]
                    break
            
            if not weight_filename:
                raise ValueError(f"Unknown model key: {self.model_key}")
            
            weight_path = os.path.join(self.weights_dir, weight_filename)
            
            if not os.path.exists(weight_path):
                raise FileNotFoundError(f"Model weights not found: {weight_path}")
            
            # Build model
            logger.info(f"Building model: {self.model_key}")
            self.model, self.transform_fn = build_model_and_transforms(self.model_key)
            
            # Load weights
            logger.info(f"Loading weights from: {weight_path}")
            checkpoint = torch.load(weight_path, map_location="cpu")
            
            if isinstance(checkpoint, dict):
                state_dict = checkpoint.get("state_dict") or checkpoint.get("model") or checkpoint
            else:
                state_dict = checkpoint
            
            self.model.load_state_dict(state_dict, strict=False)
            
            # Move to device and set eval mode
            self.model.to(self.device)
            self.model.eval()
            
            logger.info(f"Model {self.model_key} loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def _preprocess_frame(self, frame: np.ndarray) -> torch.Tensor:
        """Preprocess a single frame for inference."""
        if self.transform_fn is not None:
            return self.transform_fn(frame)
        
        # Default preprocessing
        from torchvision import transforms
        
        transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((self.input_size, self.input_size)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        
        tensor = transform(frame)
        return tensor.unsqueeze(0)
    
    def _run_inference(self, frame_tensor: torch.Tensor) -> float:
        """Run inference on a single frame."""
        frame_tensor = frame_tensor.to(self.device)
        
        with torch.no_grad():
            data_dict = {"image": frame_tensor}
            
            try:
                output = self.model(data_dict, inference=True)
            except TypeError:
                try:
                    output = self.model(data_dict)
                except (TypeError, KeyError):
                    output = self.model(frame_tensor)
            
            # Handle different output formats
            if isinstance(output, dict):
                logits = output.get("prob") or output.get("cls") or output.get("logits") or output.get("pred")
                if logits is None:
                    for key, value in output.items():
                        if isinstance(value, torch.Tensor):
                            logits = value
                            break
            else:
                logits = output
            
            # Convert to probability
            if logits.dim() == 1:
                if len(logits) == 2:
                    prob = torch.softmax(logits, dim=0)[1].item()
                else:
                    prob = torch.sigmoid(logits[0]).item()
            elif logits.shape[-1] == 2:
                prob = torch.softmax(logits, dim=1)[0, 1].item()
            elif logits.shape[-1] == 1:
                prob = torch.sigmoid(logits[0, 0]).item()
            else:
                prob = torch.softmax(logits, dim=1)[0, -1].item()
            
            return prob
    
    def analyze_video(self, video_path: str, fps: float = 3.0, threshold: float = 0.5) -> Dict:
        """
        Analyze a video and return detection results.
        
        Args:
            video_path: Path to video file
            fps: Frame sampling rate
            threshold: Detection threshold
        
        Returns:
            Dictionary with analysis results
        """
        logger.info(f"Analyzing video: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise RuntimeError(f"Failed to open video: {video_path}")
        
        source_fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
        frame_step = max(int(round(source_fps / fps)), 1)
        
        scores = []
        frames_data = []  # Store frames for keyframe extraction
        frame_idx = 0
        output_idx = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_idx % frame_step == 0:
                timestamp = output_idx / fps
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Preprocess and run inference
                frame_tensor = self._preprocess_frame(rgb_frame)
                prob = self._run_inference(frame_tensor)
                
                scores.append({
                    "frame": output_idx,
                    "timestamp": timestamp,
                    "probability": prob
                })
                
                # Store frame data for keyframe extraction
                frames_data.append({
                    "frame_bgr": frame.copy(),
                    "timestamp": timestamp,
                    "probability": prob,
                    "frame_idx": output_idx
                })
                
                output_idx += 1
            
            frame_idx += 1
        
        cap.release()
        
        # Analyze results
        if not scores:
            return {
                "success": False,
                "error": "No frames processed"
            }
        
        # Calculate metrics
        probs = [s["probability"] for s in scores]
        overall_score = float(np.max(probs))
        average_score = float(np.mean(probs))
        
        # Smooth scores
        window = 5
        if len(probs) >= window:
            smoothed = np.convolve(probs, np.ones(window)/window, mode='same')
        else:
            smoothed = np.array(probs)
        
        # Find suspicious segments
        segments = []
        in_segment = False
        segment_start = 0
        
        for i, prob in enumerate(smoothed):
            if not in_segment and prob >= threshold:
                in_segment = True
                segment_start = i
            elif in_segment and prob < threshold:
                in_segment = False
                start_ts = scores[segment_start]["timestamp"]
                end_ts = scores[i-1]["timestamp"]
                if end_ts - start_ts >= 1.0:  # Minimum 1 second
                    # Find peak frame in this segment
                    segment_probs = [scores[j]["probability"] for j in range(segment_start, i)]
                    peak_idx = segment_start + int(np.argmax(segment_probs))
                    
                    segments.append({
                        "start": start_ts,
                        "end": end_ts,
                        "duration": end_ts - start_ts,
                        "peak_score": float(smoothed[peak_idx]),
                        "peak_time": scores[peak_idx]["timestamp"],
                        "keyframe_idx": peak_idx
                    })
        
        if in_segment:
            start_ts = scores[segment_start]["timestamp"]
            end_ts = scores[-1]["timestamp"]
            if end_ts - start_ts >= 1.0:
                segment_probs = [scores[j]["probability"] for j in range(segment_start, len(scores))]
                peak_idx = segment_start + int(np.argmax(segment_probs))
                
                segments.append({
                    "start": start_ts,
                    "end": end_ts,
                    "duration": end_ts - start_ts,
                    "peak_score": float(smoothed[peak_idx]),
                    "peak_time": scores[peak_idx]["timestamp"],
                    "keyframe_idx": peak_idx
                })
        
        # Save keyframes for suspicious segments
        keyframe_dir = os.path.join(os.path.dirname(video_path), "keyframes")
        os.makedirs(keyframe_dir, exist_ok=True)
        
        for i, segment in enumerate(segments):
            keyframe_idx = segment["keyframe_idx"]
            if keyframe_idx < len(frames_data):
                frame_bgr = frames_data[keyframe_idx]["frame_bgr"]
                keyframe_path = os.path.join(keyframe_dir, f"segment_{i+1}_keyframe.jpg")
                cv2.imwrite(keyframe_path, frame_bgr)
                segment["keyframe_path"] = f"keyframes/segment_{i+1}_keyframe.jpg"
                logger.info(f"Saved keyframe for segment {i+1} at {keyframe_path}")
        
        return {
            "success": True,
            "model": self.model_key,
            "model_name": self.AVAILABLE_MODELS.get(self.model_key, {}).get("name", self.model_key),
            "overall_score": overall_score,
            "average_score": average_score,
            "threshold": threshold,
            "total_frames": len(scores),
            "fps": fps,
            "suspicious_segments": segments,
            "frame_scores": scores,  # Return all scores for threshold adjustment
            "verdict": "FAKE" if overall_score >= threshold else "REAL",
            "confidence": overall_score
        }
    
    @classmethod
    def get_available_models(cls) -> List[Dict]:
        """Get list of available models with metadata."""
        models = []
        for key, info in cls.AVAILABLE_MODELS.items():
            # Check if weights exist
            weight_file = None
            for wf, meta in WEIGHT_REGISTRY.items():
                if meta["model_key"] == key:
                    weight_file = wf
                    break
            
            if weight_file:
                weight_path = os.path.join("vendors/DeepfakeBench/training/weights", weight_file)
                available = os.path.exists(weight_path)
            else:
                available = False
            
            models.append({
                "key": key,
                "name": info["name"],
                "speed": info["speed"],
                "accuracy": info["accuracy"],
                "available": available
            })
        
        return models

