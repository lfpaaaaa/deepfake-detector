import os
import asyncio
import logging
import tempfile
from typing import Dict, Any
from realitydefender import RealityDefender

logger = logging.getLogger(__name__)


class RealityDefenderAdapter:
    def __init__(self):
        api_key = os.getenv("REALITY_DEFENDER_API_KEY")
        if not api_key:
            raise ValueError("REALITY_DEFENDER_API_KEY not found in environment variables")
        self.client = RealityDefender(api_key=api_key)
        self.timeout = 15.0  # Reasonable timeout for production
        self.retry_count = 2
        self.retry_delays = [0.5, 1.5]
    
    async def detect(self, file_bytes: bytes, filename: str, mime_type: str) -> Dict[str, Any]:
        """
        Detect deepfake in media file
        
        Returns:
            {
                "request_id": str,
                "media_type": "image" | "video",
                "status": "AUTHENTIC" | "FAKE" | "UNCERTAIN",
                "score": float,
                "score_scale": str,
                "models": list[str] (optional),
                "reasons": list[str] (optional),
                "vendor_raw": dict
            }
        """
        media_type = "video" if mime_type.startswith("video/") else "image"
        
        # Save bytes to temporary file (SDK requires file path)
        with tempfile.NamedTemporaryFile(suffix=os.path.splitext(filename)[1] or '.tmp', delete=False) as tmp_file:
            tmp_file.write(file_bytes)
            tmp_path = tmp_file.name
        
        try:
            for attempt in range(self.retry_count + 1):
                try:
                    result = await self._call_api(tmp_path, media_type)
                    return self._format_response(result, media_type)
                except asyncio.TimeoutError:
                    if attempt < self.retry_count:
                        await asyncio.sleep(self.retry_delays[attempt])
                        continue
                    raise Exception("Reality Defender API timeout after retries")
                except Exception as e:
                    if attempt < self.retry_count and self._is_retryable(e):
                        await asyncio.sleep(self.retry_delays[attempt])
                        continue
                    raise
        finally:
            # Clean up temporary file
            try:
                os.unlink(tmp_path)
            except:
                pass
    
    async def _call_api(self, file_path: str, media_type: str) -> Dict:
        """Call Reality Defender API with timeout"""
        try:
            # Upload file and get request_id
            upload_response = await asyncio.wait_for(
                self.client.upload(file_path=file_path),
                timeout=self.timeout
            )
            
            if not upload_response or "request_id" not in upload_response:
                raise Exception(f"Failed to get request_id from upload. Response: {upload_response}")
            
            request_id = upload_response["request_id"]
            
            # Poll for results
            result = await asyncio.wait_for(
                self.client.get_result(request_id),
                timeout=self.timeout
            )
            
            return result
            
        except asyncio.TimeoutError:
            raise
        except Exception as e:
            logger.error(f"RD API error: {e}")
            raise
    
    def _format_response(self, result: Dict, media_type: str) -> Dict[str, Any]:
        """Format RD response to unified structure"""
        # Map RD verdict to our status (using 'status' field, not 'verdict')
        verdict = result.get("status", "").upper()
        status_map = {
            "AUTHENTIC": "AUTHENTIC",
            "REAL": "AUTHENTIC",
            "FAKE": "FAKE",
            "MANIPULATED": "FAKE",
            "SYNTHETIC": "FAKE",
            "UNCERTAIN": "UNCERTAIN",
            "UNKNOWN": "UNCERTAIN"
        }
        status = status_map.get(verdict, "UNCERTAIN")
        
        # Extract score (already in 0-1 scale from RD)
        score_value = result.get("score", 0.5)
        
        response = {
            "request_id": result.get("request_id", ""),
            "media_type": media_type,
            "status": status,
            "score": score_value,
            "score_scale": "0-1",
            "vendor_raw": result
        }
        
        # Add optional fields if available
        if "models" in result:
            response["models"] = result["models"]
        
        if "reasons" in result:
            response["reasons"] = result["reasons"]
        
        return response
    
    def _is_retryable(self, error: Exception) -> bool:
        """Check if error is worth retrying"""
        error_msg = str(error).lower()
        return any(x in error_msg for x in ["timeout", "connection", "503", "502", "504"])