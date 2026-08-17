"""
YOLO model loading.

Deliberately framework-agnostic: no `st.cache_resource` here. The frontend
is responsible for caching model instances across reruns if it wants to
(see frontend/model_cache.py).
"""

from ultralytics import YOLO

from backend.config import MODEL_WEIGHTS


def load_model() -> YOLO:
    """Load (or download, on first run) the YOLO model weights."""
    return YOLO(MODEL_WEIGHTS)
