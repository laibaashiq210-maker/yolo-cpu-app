"""
ByteTrack tracker configuration.
"""

import os

from backend.config import BYTETRACK_YAML_PATH, BYTETRACK_YAML_CONTENT


def ensure_bytetrack_config(path: str = BYTETRACK_YAML_PATH) -> str:
    """Write the custom ByteTrack YAML config to disk if it doesn't exist yet.

    Returns the path to the config file, so callers can pass it straight to
    `model.track(..., tracker=path)`.
    """
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(BYTETRACK_YAML_CONTENT)
    return path
