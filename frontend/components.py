"""
Small, reusable pieces of the Streamlit UI.
"""

import streamlit as st

from backend.config import VEHICLE_ICONS
from backend.video_processor import process_video


def render_header():
    st.markdown("""
    <div class="header-card">
      <h1>🚦 Smart Traffic & Pedestrian Detector</h1>
      <p>Upload a traffic video — YOLO11 + ByteTrack will detect, track, and count every person and vehicle automatically.</p>
    </div>
    """, unsafe_allow_html=True)


def render_upload_card():
    st.markdown('<div class="card"><div class="card-title">📂 Upload Video</div>', unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "Supported formats: MP4, AVI, MOV",
        type=["mp4", "avi", "mov"],
        accept_multiple_files=True,
        label_visibility="visible",
    )
    st.markdown('</div>', unsafe_allow_html=True)
    return uploaded_files


def run_processing_with_progress(input_path: str, output_path: str) -> dict:
    """Call the backend's process_video, wiring its callbacks up to
    Streamlit progress widgets."""
    progress_bar = st.progress(0)
    status_text = st.empty()

    def on_progress(frame_idx: int, total_frames: int):
        if total_frames > 0:
            progress_bar.progress(min(frame_idx / total_frames, 1.0))
        pct = int(100 * frame_idx / total_frames) if total_frames > 0 else 0
        status_text.markdown(
            f'<p class="progress-label">Processing frame {frame_idx} / {total_frames} &nbsp;·&nbsp; {pct}%</p>',
            unsafe_allow_html=True,
        )

    def on_status(message: str):
        status_text.markdown(f'<p class="progress-label">{message}</p>', unsafe_allow_html=True)

    results = process_video(
        input_path, output_path,
        progress_callback=on_progress,
        status_callback=on_status,
    )

    status_text.empty()
    progress_bar.empty()
    return results


def render_results(results: dict, output_path: str, col_out):
    st.markdown('<div class="success-banner">✅ Video processing is done</div>', unsafe_allow_html=True)

    m1, m2 = st.columns(2)
    m1.metric("👥 Total Pedestrians", results["total_pedestrians"])
    m2.metric("🚗 Total Vehicles", results["total_vehicles"])

    vehicle_counts = {k: v for k, v in results["counts"].items() if k != "person" and v > 0}
    if vehicle_counts:
        badges_html = '<div class="badge-row">'
        for cname, cnt in vehicle_counts.items():
            icon = VEHICLE_ICONS.get(cname, "🚙")
            badges_html += f'<div class="badge">{icon} {cname.capitalize()} <span class="badge-count">{cnt}</span></div>'
        badges_html += '</div>'
        st.markdown(badges_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with col_out:
        st.caption("🎯 Processed Video")
        st.video(output_path)
