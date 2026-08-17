"""
Static configuration: model, class mapping, colors, thresholds.

Keeping these in one place means the detection logic, the tracker config,
and any UI code can all import the same source of truth instead of
duplicating magic numbers.
"""

# YOLO model weights file (auto-downloaded by ultralytics on first use)
MODEL_WEIGHTS = "yolo11n.pt"

# COCO class-id -> friendly name, restricted to what this app cares about
TARGET_CLASSES = {
    0: "person",
    1: "bicycle",
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck",
}
CLASS_IDS = list(TARGET_CLASSES.keys())

# BGR colors (OpenCV) used to draw bounding boxes per class
CLASS_COLORS = {
    0: (0, 200, 80),    # person
    1: (255, 160, 0),   # bicycle
    2: (50, 120, 255),  # car
    3: (0, 180, 255),   # motorcycle
    5: (180, 0, 255),   # bus
    7: (220, 80, 0),    # truck
}

# Emoji icons for vehicle classes, used by the frontend for display only
VEHICLE_ICONS = {
    "car": "🚗",
    "bus": "🚌",
    "truck": "🚚",
    "motorcycle": "🏍️",
    "bicycle": "🚲",
}

CONFIDENCE_THRESHOLD = 0.5
IOU_THRESHOLD = 0.5

BYTETRACK_YAML_PATH = "custom_bytetrack.yaml"
BYTETRACK_YAML_CONTENT = """tracker_type: bytetrack
track_high_thresh: 0.5
track_low_thresh: 0.1
new_track_thresh: 0.7
track_buffer: 100
match_thresh: 0.7
fuse_score: True
"""
