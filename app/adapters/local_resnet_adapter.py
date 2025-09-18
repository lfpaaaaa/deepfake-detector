import os
import logging
import tempfile
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import cv2
import numpy as np
from typing import Dict, Any, List
import torchvision.models as models
import io

logger = logging.getLogger(__name__)


# Direct use of torchvision ResNet50 model


class LocalResNetAdapter:
    """Adapter for local ResNet50 deepfake detection model"""
    
    def __init__(self, model_path: str = "deepfake_resnet50.pth"):
        self.model_path = model_path
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = None
        self.transform = None
        self._load_model()
        self._setup_transforms()
    
    def _load_model(self):
        """Load the trained ResNet50 model"""
        try:
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Model file not found: {self.model_path}")
            
            # Initialize ResNet50 model
            self.model = models.resnet50(pretrained=False)
            # Modify the final layer for binary classification
            self.model.fc = nn.Linear(self.model.fc.in_features, 2)
            
            # Load state dict
            checkpoint = torch.load(self.model_path, map_location=self.device)
            
            # Handle different checkpoint formats
            if isinstance(checkpoint, dict):
                if 'model_state_dict' in checkpoint:
                    self.model.load_state_dict(checkpoint['model_state_dict'])
                elif 'state_dict' in checkpoint:
                    self.model.load_state_dict(checkpoint['state_dict'])
                else:
                    self.model.load_state_dict(checkpoint)
            else:
                self.model.load_state_dict(checkpoint)
            
            self.model.to(self.device)
            self.model.eval()
            
            logger.info(f"Model loaded successfully from {self.model_path}")
            logger.info(f"Using device: {self.device}")
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def _setup_transforms(self):
        """Setup image preprocessing transforms"""
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                               std=[0.229, 0.224, 0.225])
        ])
    
    async def detect(self, file_bytes: bytes, filename: str, mime_type: str) -> Dict[str, Any]:
        """
        Detect deepfake in media file using local ResNet50 model
        
        Returns:
            {
                "request_id": str,
                "media_type": "image" | "video",
                "status": "AUTHENTIC" | "FAKE" | "UNCERTAIN",
                "score": float,
                "score_scale": "0-1",
                "models": ["ResNet50"],
                "reasons": list[str] (optional),
                "vendor_raw": dict
            }
        """
        media_type = "video" if mime_type.startswith("video/") else "image"
        
        try:
            if media_type == "image":
                result = await self._detect_image(file_bytes, filename)
            else:
                result = await self._detect_video(file_bytes, filename)
            
            return self._format_response(result, media_type, filename)
            
        except Exception as e:
            logger.error(f"Detection failed for {filename}: {e}")
            raise
    
    async def _detect_image(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        """Detect deepfake in image"""
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(file_bytes)).convert('RGB')
            
            # Preprocess image
            input_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # Run inference
            with torch.no_grad():
                outputs = self.model(input_tensor)
                probabilities = torch.softmax(outputs, dim=1)
                fake_prob = probabilities[0][1].item()  # Probability of being fake
                authentic_prob = probabilities[0][0].item()  # Probability of being authentic
            
            return {
                "fake_probability": fake_prob,
                "authentic_probability": authentic_prob,
                "prediction": 1 if fake_prob > 0.5 else 0,
                "confidence": max(fake_prob, authentic_prob)
            }
            
        except Exception as e:
            logger.error(f"Image detection failed: {e}")
            raise
    
    async def _detect_video(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        """Detect deepfake in video by sampling frames"""
        try:
            # Save video to temporary file
            with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as tmp_file:
                tmp_file.write(file_bytes)
                tmp_path = tmp_file.name
            
            try:
                # Open video
                cap = cv2.VideoCapture(tmp_path)
                frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                fps = cap.get(cv2.CAP_PROP_FPS)
                
                # Sample frames (every 30 frames or at least 5 frames)
                sample_interval = max(1, frame_count // 5)
                frame_predictions = []
                frame_confidences = []
                
                frame_idx = 0
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    if frame_idx % sample_interval == 0:
                        # Convert BGR to RGB
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        frame_pil = Image.fromarray(frame_rgb)
                        
                        # Preprocess and predict
                        input_tensor = self.transform(frame_pil).unsqueeze(0).to(self.device)
                        
                        with torch.no_grad():
                            outputs = self.model(input_tensor)
                            probabilities = torch.softmax(outputs, dim=1)
                            fake_prob = probabilities[0][1].item()
                            authentic_prob = probabilities[0][0].item()
                        
                        frame_predictions.append(1 if fake_prob > 0.5 else 0)
                        frame_confidences.append(max(fake_prob, authentic_prob))
                    
                    frame_idx += 1
                
                cap.release()
                
                # Aggregate frame predictions
                avg_fake_prob = np.mean([1 - p for p in frame_predictions])  # Convert to fake probability
                avg_authentic_prob = np.mean(frame_predictions)  # Convert to authentic probability
                overall_prediction = 1 if avg_fake_prob > 0.5 else 0
                avg_confidence = np.mean(frame_confidences)
                
                return {
                    "fake_probability": avg_fake_prob,
                    "authentic_probability": avg_authentic_prob,
                    "prediction": overall_prediction,
                    "confidence": avg_confidence,
                    "frames_analyzed": len(frame_predictions),
                    "total_frames": frame_count
                }
                
            finally:
                # Clean up temporary file
                try:
                    os.unlink(tmp_path)
                except:
                    pass
                    
        except Exception as e:
            logger.error(f"Video detection failed: {e}")
            raise
    
    def _format_response(self, result: Dict, media_type: str, filename: str) -> Dict[str, Any]:
        """Format detection result to unified structure"""
        fake_prob = result["fake_probability"]
        authentic_prob = result["authentic_probability"]
        prediction = result["prediction"]
        confidence = result["confidence"]
        
        # Determine status based on prediction and confidence
        if confidence < 0.6:  # Low confidence threshold
            status = "UNCERTAIN"
        elif prediction == 1:  # Predicted as fake
            status = "FAKE"
        else:  # Predicted as authentic
            status = "AUTHENTIC"
        
        response = {
            "request_id": f"local_{filename}_{hash(filename)}",
            "media_type": media_type,
            "status": status,
            "score": fake_prob,  # Use fake probability as score
            "score_scale": "0-1",
            "models": ["ResNet50"],
            "vendor_raw": {
                "model_type": "ResNet50",
                "fake_probability": fake_prob,
                "authentic_probability": authentic_prob,
                "prediction": prediction,
                "confidence": confidence,
                "device": str(self.device)
            }
        }
        
        # Add video-specific information
        if media_type == "video" and "frames_analyzed" in result:
            response["vendor_raw"]["frames_analyzed"] = result["frames_analyzed"]
            response["vendor_raw"]["total_frames"] = result["total_frames"]
        
        # Add reasons based on confidence and prediction
        reasons = []
        if confidence < 0.6:
            reasons.append("Low confidence in prediction")
        if fake_prob > 0.7:
            reasons.append("High probability of manipulation detected")
        elif authentic_prob > 0.7:
            reasons.append("High probability of authentic content")
        
        if reasons:
            response["reasons"] = reasons
        
        return response
