"""
CSS for the Streamlit UI, kept separate from layout/component code.
"""

CUSTOM_CSS = """
<style>
/* ── Global ── */
body, [data-testid="stAppViewContainer"] { background: #f0f4f8; }

/* ── Header card ── */
.header-card {
    background: linear-gradient(135deg, #1e3a5f 0%, #2d6a9f 100%);
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 28px;
    color: white;
}
.header-card h1 { font-size: 2rem; font-weight: 800; margin: 0 0 6px 0; color: white; }
.header-card p  { font-size: 1rem; margin: 0; opacity: 0.85; }

/* ── Section cards ── */
.card {
    background: white;
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    border: 1px solid #e8edf2;
}
.card-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1e3a5f;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ── Metrics ── */
div[data-testid="stMetric"] {
    background: #f8fafc;
    border-radius: 12px;
    padding: 14px;
    border: 1px solid #e2e8f0;
}
div[data-testid="stMetricLabel"] { font-weight: 600; color: #475569; font-size: 0.8rem; }
div[data-testid="stMetricValue"] { font-weight: 800; color: #1e3a5f; font-size: 1.8rem; }

/* ── Vehicle badges ── */
.badge-row { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 12px; }
.badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: #f1f5f9; border: 1px solid #e2e8f0;
    border-radius: 20px; padding: 6px 14px;
    font-size: 0.85rem; font-weight: 600; color: #334155;
}
.badge-count {
    background: #1e3a5f; color: white;
    border-radius: 12px; padding: 2px 8px;
    font-size: 0.8rem; font-weight: 700;
}

/* ── Success banner ── */
.success-banner {
    background: linear-gradient(90deg, #d1fae5, #a7f3d0);
    border: 1px solid #6ee7b7;
    border-radius: 10px;
    padding: 12px 20px;
    color: #065f46;
    font-weight: 600;
    font-size: 0.95rem;
    margin-bottom: 16px;
}

/* ── Progress label ── */
.progress-label {
    font-size: 0.85rem; color: #64748b; text-align: center; margin-top: 4px;
}

/* ── Upload area ── */
[data-testid="stFileUploadDropzone"] {
    border: 2px dashed #94a3b8 !important;
    border-radius: 14px !important;
    background: #f8fafc !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
</style>
"""
