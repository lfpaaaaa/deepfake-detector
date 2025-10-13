# tools/build_dfbench_model.py
"""
Factory for building DeepfakeBench detector models.
Auto-discovers detector modules from vendors/DeepfakeBench/training/detectors/
"""

import sys
import os
import glob
import importlib
import torch
import yaml
from typing import Tuple, Optional, Callable

# Add DeepfakeBench to Python path
DFB_ROOT = os.path.join(os.path.dirname(__file__), "..", "vendors", "DeepfakeBench")
sys.path.insert(0, DFB_ROOT)


def _auto_import_detector(model_key: str):
    """
    Automatically import the detector module for given model_key.
    Searches through training/detectors/*_detector.py files.
    """
    # First try: exact match with model_key in filename
    search_pattern = os.path.join(DFB_ROOT, "training", "detectors", f"*{model_key}*detector.py")
    candidates = sorted(glob.glob(search_pattern, recursive=False))
    
    if not candidates:
        # Fallback: try all detector files
        search_pattern = os.path.join(DFB_ROOT, "training", "detectors", "*detector.py")
        candidates = sorted(glob.glob(search_pattern, recursive=False))
    
    # Try to import each candidate and find the builder function
    # First pass: look for exact matches
    for py_file in candidates:
        if "base_detector" in py_file:
            continue  # Skip base class
            
        # Convert file path to module path
        rel_path = os.path.relpath(py_file, DFB_ROOT)
        module_path = rel_path.replace(os.sep, ".")[:-3]  # Remove .py
        
        try:
            mod = importlib.import_module(module_path)
            
            # Look for exact match detector class (e.g., "xception" -> "XceptionDetector")
            expected_class_name = f"{model_key}Detector".lower()
            for attr_name in dir(mod):
                if attr_name.lower() == expected_class_name:
                    attr = getattr(mod, attr_name)
                    if callable(attr):
                        print(f"[INFO] Found detector class (exact match): {module_path}.{attr_name}")
                        return attr
        except Exception as e:
            continue
    
    # Second pass: look for partial matches
    for py_file in candidates:
        if "base_detector" in py_file:
            continue
            
        rel_path = os.path.relpath(py_file, DFB_ROOT)
        module_path = rel_path.replace(os.sep, ".")[:-3]
        
        try:
            mod = importlib.import_module(module_path)
            
            for attr_name in dir(mod):
                attr = getattr(mod, attr_name)
                
                # Check for build_xxx() function
                if attr_name.startswith("build_") and callable(attr):
                    if model_key.lower() in attr_name.lower():
                        print(f"[INFO] Found builder: {module_path}.{attr_name}")
                        return attr
                
                # Check for XXXDetector class (partial match)
                if attr_name.lower().endswith("detector") and callable(attr):
                    if model_key.lower() in attr_name.lower():
                        print(f"[INFO] Found detector class (partial match): {module_path}.{attr_name}")
                        return attr
                        
        except Exception as e:
            continue
    
    raise ImportError(f"Cannot locate detector builder for model_key='{model_key}'. "
                      f"Searched in {DFB_ROOT}/training/detectors/")


def _load_config(model_key: str) -> dict:
    """Load configuration from YAML file for the model."""
    config_path = os.path.join(DFB_ROOT, "training", "config", "detector", f"{model_key}.yaml")
    
    if not os.path.exists(config_path):
        print(f"[WARN] Config file not found: {config_path}, using minimal config")
        # Return minimal config
        return {
            "backbone_name": model_key,
            "backbone_config": {"num_classes": 2, "inc": 3},
            "loss_func": "cross_entropy",
            "pretrained": "None"
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
        
        # Force disable pretraining - we will load full trained weights later
        # This avoids the error when backbone pretrained weights are missing
        print(f"[INFO] Skipping backbone pretraining for {model_key} (will load full trained weights later)")
        config["pretrained"] = "None"
        
        return config
    except Exception as e:
        print(f"[WARN] Failed to load config: {e}, using minimal config")
        return {
            "backbone_name": model_key,
            "backbone_config": {"num_classes": 2, "inc": 3},
            "loss_func": "cross_entropy",
            "pretrained": "None"
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
    builder = _auto_import_detector(model_key)
    
    # Load configuration
    config = _load_config(model_key)
    
    # Override num_classes if provided
    if "backbone_config" in config:
        config["backbone_config"]["num_classes"] = num_classes
    
    # Try to instantiate the model
    try:
        # Some detectors are classes that need instantiation
        if isinstance(builder, type):
            # It's a class, instantiate it with config
            model = builder(config)
        else:
            # It's a function, call it
            result = builder(config)
            
            # Check if result is tuple (model, transform) or just model
            if isinstance(result, tuple) and len(result) == 2:
                return result[0], result[1]
            else:
                model = result
        
        return model, None
        
    except Exception as e:
        raise RuntimeError(f"Failed to build model for '{model_key}': {e}")

