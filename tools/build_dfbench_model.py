# tools/build_dfbench_model.py
"""
Factory for building DeepfakeBench detector models.
Uses the DETECTOR registry from DeepfakeBench.
"""

import sys
import os
import torch
import yaml
from typing import Tuple, Optional, Callable

# Add DeepfakeBench to Python path
DFB_ROOT = os.path.join(os.path.dirname(__file__), "..", "models", "vendors", "DeepfakeBench")
sys.path.insert(0, DFB_ROOT)

# Also add the training directory so modules can import each other
TRAINING_ROOT = os.path.join(DFB_ROOT, "training")
sys.path.insert(0, TRAINING_ROOT)


def _get_detector_class(model_key: str):
    """
    Get the detector class from the DETECTOR registry.
    Returns the detector class for the given model_key.
    """
    from detectors import DETECTOR
    
    if model_key not in DETECTOR.data:
        available_models = list(DETECTOR.data.keys())
        raise ValueError(
            f"Model '{model_key}' not found in DETECTOR registry. "
            f"Available models: {available_models}"
        )
    
    detector_class = DETECTOR.data[model_key]
    print(f"[INFO] Found detector class for '{model_key}': {detector_class.__name__}")
    return detector_class


def _load_config(model_key: str) -> dict:
    """Load configuration from YAML file for the model."""
    config_path = os.path.join(DFB_ROOT, "training", "config", "detector", f"{model_key}.yaml")
    
    # Models that require ImageNet pretrained weights (will fail without them)
    REQUIRES_IMAGENET_PRETRAIN = {"f3net", "core", "spsl", "ucf", "srm", "capsule_net"}
    
    if not os.path.exists(config_path):
        print(f"[WARN] Config file not found: {config_path}, using minimal config")
        # Return minimal config
        return {
            "backbone_name": model_key,
            "backbone_config": {"num_classes": 2, "inc": 3},
            "loss_func": "cross_entropy",
            "pretrained": None  # Use None object, not string
        }
    
    try:
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        
        # Ensure required fields exist
        if "backbone_name" not in config:
            config["backbone_name"] = model_key
        if "backbone_config" not in config:
            config["backbone_config"] = {"num_classes": 2, "inc": 3}
        if "loss_func" not in config:
            config["loss_func"] = "cross_entropy"
        
        # Handle pretrained weights based on model requirements
        if model_key.lower() in REQUIRES_IMAGENET_PRETRAIN:
            # These models REQUIRE ImageNet pretrained weights for good performance
            pretrained_path = config.get("pretrained", "")
            if pretrained_path and pretrained_path != "None":
                # Convert relative path to absolute
                if not os.path.isabs(pretrained_path):
                    pretrained_path = os.path.join(DFB_ROOT, pretrained_path)
                
                # Check if file exists
                if os.path.exists(pretrained_path):
                    print(f"[INFO] Using ImageNet pretrained weights: {pretrained_path}")
                    config["pretrained"] = pretrained_path
                else:
                    raise FileNotFoundError(
                        f"Model '{model_key}' requires ImageNet pretrained weights, but file not found: {pretrained_path}\n"
                        f"Please download 'xception-b5690688.pth' from:\n"
                        f"https://download.pytorch.org/models/xception-b5690688.pth\n"
                        f"And place it in: models/vendors/DeepfakeBench/training/pretrained/"
                    )
            else:
                raise ValueError(
                    f"Model '{model_key}' requires ImageNet pretrained weights, but none specified in config.\n"
                    f"Please download 'xception-b5690688.pth' and update the config."
                )
        else:
            # For other models, disable pretraining - we will load full trained weights later
            print(f"[INFO] Skipping backbone pretraining for {model_key} (will load full trained weights later)")
            config["pretrained"] = None  # Use None object, not string "None"
        
        return config
    except FileNotFoundError:
        # Re-raise FileNotFoundError for missing pretrained weights
        raise
    except Exception as e:
        print(f"[WARN] Failed to load config: {e}, using minimal config")
        return {
            "backbone_name": model_key,
            "backbone_config": {"num_classes": 2, "inc": 3},
            "loss_func": "cross_entropy",
            "pretrained": None  # Use None object, not string
        }


def build_model_and_transforms(model_key: str, num_classes: int = 2) -> Tuple[torch.nn.Module, Optional[Callable]]:
    """
    Build a DeepfakeBench detector model and its transform function.
    
    Args:
        model_key: Model identifier (e.g., "xception", "meso4", etc.)
        num_classes: Number of output classes (default: 2 for binary classification)
    
    Returns:
        Tuple of (model, transform_function)
        - model: PyTorch model ready for inference
        - transform_function: Optional preprocessing function (None if using default)
    """
    detector_class = _get_detector_class(model_key)
    
    # Load configuration
    config = _load_config(model_key)
    
    # Override num_classes if provided
    if "backbone_config" in config:
        config["backbone_config"]["num_classes"] = num_classes
    
    # Instantiate the detector model
    try:
        # All detectors in the registry are classes, instantiate with config
        model = detector_class(config)
        return model, None
        
    except Exception as e:
        raise RuntimeError(f"Failed to build model for '{model_key}': {e}")

