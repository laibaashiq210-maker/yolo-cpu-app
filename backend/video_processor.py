"""
Core detection + tracking pipeline.

`process_video` is UI-agnostic: instead of talking to Streamlit directly,
it reports progress through optional callback functions. This keeps the
backend reusable from a CLI, a test, or any other frontend.
"""

import os
import time
from typing import Callable, Optional

import cv2

from backend.config import (
    CLASS_IDS,
    CONFIDENCE_THRESHOLD,
    IOU_THRESHOLD,
    MODEL_WEIGHTS,
    TARGET_CLASSES,
)
from backend.drawing import draw_detections, draw_hud
from backend.encoding import reencode_to_h264
from backend.tracker import ensure_bytetrack_config
from ultralytics import YOLO

ProgressCallback = Callable[[int, int], None]  # (frame_idx, total_frames)
StatusCallback = Callable[[str], None]          # (message)


def process_video(
    input_path: str,
    output_path: str,
    progress_callback: Optional[ProgressCallback] = None,
    status_callback: Optional[StatusCallback] = None,
) -> dict:
    """Run detection + tracking on `input_path`, write annotated video to
    `output_path`, and return summary statistics.

    A fresh YOLO model instance is created per call so tracker IDs always
    restart from 1 for every new video.
    """
    tracker_yaml = ensure_bytetrack_config()
    fresh_model = YOLO(MODEL_WEIGHTS)

    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    raw_output_path = output_path.replace(".mp4", "_raw.mp4")
    out = cv2.VideoWriter(raw_output_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
    seen_ids = {cname: set() for cname in TARGET_CLASSES.values()}

    frame_idx = 0
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = fresh_model.track(
            frame, persist=True, conf=CONFIDENCE_THRESHOLD, iou=IOU_THRESHOLD,
            classes=CLASS_IDS, tracker=tracker_yaml, verbose=False, device="cpu",
        )[0]

        live_counts = {}
        if results.boxes.id is not None:
            ids = results.boxes.id.int().cpu().tolist()
            clss = results.boxes.cls.int().cpu().tolist()
            boxes = results.boxes.xyxy.cpu().numpy()

            live_counts = draw_detections(frame, boxes, clss, ids)
            for cls_id, track_id in zip(clss, ids):
                if cls_id in TARGET_CLASSES:
                    seen_ids[TARGET_CLASSES[cls_id]].add(track_id)

        frame = draw_hud(frame, live_counts)
        out.write(frame)
        frame_idx += 1

        if progress_callback is not None:
            progress_callback(frame_idx, total_frames)

    cap.release()
    out.release()

    if status_callback is not None:
        status_callback("Finalizing video for playback…")

    reencode_to_h264(raw_output_path, output_path)
    os.remove(raw_output_path)

    elapsed = time.time() - start_time
    counts = {cname: len(ids) for cname, ids in seen_ids.items()}

    return {
        "counts": counts,
        "total_pedestrians": counts.get("person", 0),
        "total_vehicles": sum(v for k, v in counts.items() if k != "person"),
        "elapsed_seconds": elapsed,
        "frames_processed": frame_idx,
    }
