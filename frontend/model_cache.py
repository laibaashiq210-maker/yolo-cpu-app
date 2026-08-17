"""
Streamlit-specific caching wrapper around backend.model.load_model.

Kept out of the backend package so the backend stays free of any
Streamlit dependency.
"""

import streamlit as st

from backend.model import load_model as _load_model


@st.cache_resource
def get_cached_model():
    """Load the YOLO model once per Streamlit session and reuse it."""
    return _load_model()
