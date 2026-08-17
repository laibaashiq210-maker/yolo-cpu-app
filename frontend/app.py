"""
Smart Traffic & Pedestrian Detector — CPU Web App

Streamlit entry point. This file only handles page setup and the
upload -> process -> show results flow; all detection/tracking logic
lives in the `backend` package.

Run with:  streamlit run frontend/app.py
(from the project root, so the `backend` package is importable)
"""

import os
import sys
import tempfile

import streamlit as st

# Make sure the project root (parent of frontend/ and backend/) is on the
# path, so `import backend...` works regardless of the working directory
# `streamlit run` was invoked from.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend.components import (
    render_header,
    render_results,
    render_upload_card,
    run_processing_with_progress,
)
from frontend.model_cache import get_cached_model
from frontend.styles import CUSTOM_CSS

st.set_page_config(page_title="Smart Traffic Detector", page_icon="🚦", layout="wide")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

render_header()

# Warm the model cache once per session (also surfaces load errors early).
get_cached_model()

uploaded_files = render_upload_card()

if uploaded_files:
    if "results_cache" not in st.session_state:
        st.session_state.results_cache = {}

    for i, uploaded_file in enumerate(uploaded_files):
        st.markdown("---")
        file_key = f"{uploaded_file.name}_{uploaded_file.size}_{i}"

        tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        tfile.write(uploaded_file.read())
        input_path = tfile.name

        already_done = file_key in st.session_state.results_cache

        st.markdown(f'<div class="card"><div class="card-title">🎬 {uploaded_file.name}</div>', unsafe_allow_html=True)
        col_orig, col_out = st.columns(2)
        with col_orig:
            st.caption("📹 Original Video")
            st.video(input_path)
        st.markdown('</div>', unsafe_allow_html=True)

        processing_key = f"processing_{file_key}"

        if not already_done and not st.session_state.get(processing_key, False):
            if st.button("▶️ Process this Video", key=f"process_{i}", use_container_width=True):
                st.session_state[processing_key] = True
                st.rerun()

        if st.session_state.get(processing_key, False) and not already_done:
            output_path = os.path.join(tempfile.gettempdir(), f"output_{i}.mp4")
            results = run_processing_with_progress(input_path, output_path)
            st.session_state.results_cache[file_key] = (results, output_path)
            st.session_state[processing_key] = False
            st.rerun()

        if already_done:
            results, output_path = st.session_state.results_cache[file_key]
            render_results(results, output_path, col_out)

            with open(output_path, "rb") as f:
                st.download_button(
                    "⬇️ Download Processed Video", f,
                    file_name=f"processed_{uploaded_file.name}",
                    key=f"download_{i}",
                    use_container_width=True,
                )

            if st.button("🔄 Re-process this Video", key=f"reprocess_{i}", use_container_width=True):
                del st.session_state.results_cache[file_key]
                st.rerun()
