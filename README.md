# Smart Traffic & Pedestrian Detector — CPU App

A simple, clean web app. Upload a video, get it back with pedestrians and
vehicles detected, tracked (unique IDs), and a live counter shown right on
the video itself.

## Project structure

```
yolo_cpu_app/
├── app.py                     # convenience wrapper: `streamlit run app.py`
├── requirements.txt
├── backend/                   # detection/tracking logic — no Streamlit here
│   ├── config.py               # classes, colors, thresholds, tracker settings
│   ├── model.py                 # YOLO model loading
│   ├── tracker.py               # ByteTrack config file generation
│   ├── drawing.py               # bounding-box + HUD drawing on frames
│   ├── encoding.py              # ffmpeg re-encode to browser-playable H.264
│   └── video_processor.py       # the end-to-end process_video() pipeline
└── frontend/                  # Streamlit UI only — calls into backend/
    ├── app.py                   # page setup + upload/process/results flow
    ├── styles.py                 # CSS
    ├── components.py             # header, upload card, results rendering
    └── model_cache.py            # st.cache_resource wrapper around backend.model
```

The `backend` package has no dependency on Streamlit, so the detection
pipeline can be reused from a CLI, a script, tests, or a different UI without
any changes.

## How to run it

1. Make sure Python 3.9+ is installed (`python --version` to check).

2. Open a terminal in this folder and install requirements:
   ```
   pip install -r requirements.txt
   ```

3. Start the app:
   ```
   streamlit run app.py
   ```
   (or equivalently `streamlit run frontend/app.py`)

4. Your browser opens at `http://localhost:8501`.

5. Upload one or more videos, click **Process this video** for each one.
   You'll see:
   - The live count of pedestrians and vehicles displayed on the video itself
   - Total unique pedestrians and vehicles counted
   - A download button for the processed video

## Notes

- Runs entirely on CPU — no GPU needed. This will be noticeably slower than
  the Colab (GPU) version, which is expected and is the point of this
  comparison.
- The first run downloads the YOLO11n model weights automatically (needs
  internet once).
- Uses ByteTrack for tracking, with the same tuned settings used in the
  Colab notebook.
