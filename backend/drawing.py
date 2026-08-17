"""
Frame annotation helpers (bounding boxes + on-screen HUD).
"""

import cv2

from backend.config import CLASS_COLORS, TARGET_CLASSES

HUD_ORDER = ["car", "bus", "truck", "motorcycle", "bicycle"]


def draw_detections(frame, boxes, class_ids, track_ids):
    """Draw a bounding box + label for every detection on `frame` (in place).

    Returns a dict of {class_name: count} for objects visible in this frame.
    """
    live_counts = {}
    for box, cls_id, track_id in zip(boxes, class_ids, track_ids):
        if cls_id not in TARGET_CLASSES:
            continue
        cname = TARGET_CLASSES[cls_id]
        live_counts[cname] = live_counts.get(cname, 0) + 1

        x1, y1, x2, y2 = map(int, box)
        color = CLASS_COLORS[cls_id]
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(
            frame, f"{cname} ID:{track_id}",
            (x1, max(y1 - 8, 0)), cv2.FONT_HERSHEY_SIMPLEX, 0.52, color, 2,
        )
    return live_counts


def draw_hud(frame, live_counts):
    """Draw the semi-transparent top banner with live per-class counts."""
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (frame.shape[1], 40), (20, 30, 45), -1)
    frame = cv2.addWeighted(overlay, 0.65, frame, 0.35, 0)

    parts = [f"Persons: {live_counts.get('person', 0)}"]
    for cname in HUD_ORDER:
        parts.append(f"{cname.capitalize()}: {live_counts.get(cname, 0)}")
    text = "   ".join(parts)

    cv2.putText(frame, text, (12, 27), cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 255, 255), 2)
    return frame
