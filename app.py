"""
Thin convenience wrapper so `streamlit run app.py` still works from the
project root. All real UI code lives in frontend/app.py; all detection
logic lives in the backend/ package.
"""

import runpy
import os

runpy.run_path(os.path.join(os.path.dirname(__file__), "frontend", "app.py"), run_name="__main__")
