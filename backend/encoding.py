"""
Video re-encoding utilities.

OpenCV's "mp4v" codec is not playable in most web browsers (an HTML5
<video> tag needs H.264). We write frames with mp4v to a raw temp file
first, then re-encode that file to H.264 here.
"""

import subprocess

import imageio_ffmpeg


def reencode_to_h264(raw_path: str, output_path: str) -> None:
    """Re-encode `raw_path` to H.264/yuv420p at `output_path` via ffmpeg."""
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run(
        [
            ffmpeg_exe, "-y", "-i", raw_path,
            "-vcodec", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            output_path,
        ],
        check=True, capture_output=True,
    )
