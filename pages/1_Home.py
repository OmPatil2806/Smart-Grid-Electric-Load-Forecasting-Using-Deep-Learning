import streamlit as st
from datetime import datetime
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Home | Smart Grid", page_icon="🏠", layout="wide")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap');
  html, body, [data-testid="stAppViewContainer"] {
    background: #0a0e1a !important; color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif;
  }
  [data-testid="stSidebar"] { background: #0d1321 !important; border-right: 1px solid #1e3a5f !important; }
  #MainMenu, footer, header { visibility: hidden; }

  .hero {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1f3c 50%, #0a0e1a 100%);
    border: 1px solid #1e3a5f;
    border-radius: 20px;
    padding: 60px 40px;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 32px;
  }
  .hero::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(ellipse at 50% 0%, rgba(0,212,255,0.08) 0%, transparent 70%);
  }
  .hero-title {
    font-family: 'Orbitron', monospace;
    font-size: clamp(1.4rem, 4vw, 2.8rem);
    font-weight: 900;
    background: linear-gradient(135deg, #00d4ff, #0066cc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 12px 0 8px;
    letter-spacing: 2px;
  }
  .hero-sub {
    color: #94a3b8;
    font-size: clamp(0.85rem, 2vw, 1.1rem);
    font-weight: 300;
    letter-spacing: 1px;
  }
  .hero-icon { font-size: 56px; filter: drop-shadow(0 0 20px rgba(0,212,255,0.5)); }

  .time-badge {
    display: inline-block;
    background: #111827;
    border: 1px solid #1e3a5f;
    border-radius: 50px;
    padding: 8px 24px;
    font-family: 'Orbitron', monospace;
    font-size: 0.85rem;
    color: #00d4ff;
    margin-top: 20px;
    letter-spacing: 2px;
  }

  .nav-card {
    background: #111827;
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 28px 20px;
    text-align: center;
    transition: all 0.3s ease;
    cursor: pointer;
    height: 160px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 10px;
  }
  .nav-card:hover {
    border-color: #00d4ff;
    background: #131d2e;
    transform: translateY(-4px);
    box-shadow: 0 12px 30px rgba(0,212,255,0.15);
  }
  .nav-card .card-icon { font-size: 36px; }
  .nav-card .card-title {
    font-family: 'Orbitron', monospace;
    font-size: 0.75rem;
    font-weight: 700;
    color: #00d4ff;
    letter-spacing: 1px;
    text-transform: uppercase;
  }
  .nav-card .card-desc { font-size: 0.75rem; color: #64748b; }

  .stat-strip {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    margin: 24px 0;
  }
  .stat-item {
    flex: 1;
    min-width: 120px;
    background: #111827;
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 16px;
    text-align: center;
  }
  .stat-val { font-family: 'Orbitron', monospace; font-size: 1.4rem; color: #00d4ff; font-weight: 700; }
  .stat-lbl { font-size: 0.72rem; color: #64748b; margin-top: 4px; text-transform: uppercase; letter-spacing: 1px; }

  .section-label {
    font-size: 10px; font-weight: 600; letter-spacing: 3px;
    color: #475569; text-transform: uppercase; margin-bottom: 16px;
  }
  .stButton > button {
    background: transparent !important; border: none !important;
    padding: 0 !important; width: 100% !important;
  }
</style>
""", unsafe_allow_html=True)

# ── Live Time ─────────────────────────────────────────────────────────────────
now = datetime.now()
time_str = now.strftime("%A, %d %B %Y  |  %H:%M:%S")

# ── Hero Banner ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <div class="hero-icon">⚡</div>
  <div class="hero-title">Smart Grid Electric<br>Load Forecasting</div>
  <div class="hero-sub">Deep Learning Powered Energy Prediction System</div>
  <div class="time-badge">🕐 {time_str}</div>
</div>
""", unsafe_allow_html=True)

# ── Stats Strip ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="stat-strip">
  <div class="stat-item">
    <div class="stat-val">92%</div>
    <div class="stat-lbl">Model Accuracy</div>
  </div>
  <div class="stat-item">
    <div class="stat-val">45.23</div>
    <div class="stat-lbl">MAE (kW)</div>
  </div>
  <div class="stat-item">
    <div class="stat-val">61.84</div>
    <div class="stat-lbl">RMSE (kW)</div>
  </div>
  <div class="stat-item">
    <div class="stat-val">5 YR</div>
    <div class="stat-lbl">Dataset Span</div>
  </div>
  <div class="stat-item">
    <div class="stat-val">LSTM</div>
    <div class="stat-lbl">Model Type</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Navigation Cards ──────────────────────────────────────────────────────────
st.markdown('<div class="section-label">🧭 Navigate to a Page</div>', unsafe_allow_html=True)

cards = [
    ("🔮", "Single Prediction",  "Predict load for one time point",    "pages/2_Single_Prediction.py"),
    ("📅", "Batch Prediction",   "Upload CSV & predict all rows",       "pages/3_Batch_Prediction.py"),
    ("🗓️", "24hr Forecast",      "Forecast entire day hour by hour",    "pages/5_24hr_Forecast.py"),
    ("📊", "Visualizations",     "Explore hourly & temperature trends", "pages/4_Visualizations.py"),
    ("ℹ️", "About",              "Project info & model details",        "pages/6_About.py"),
]

cols = st.columns(len(cards))
for col, (icon, title, desc, _) in zip(cols, cards):
    with col:
        st.markdown(f"""
        <div class="nav-card">
          <div class="card-icon">{icon}</div>
          <div class="card-title">{title}</div>
          <div class="card-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; margin-top:40px; padding:20px;
            border-top:1px solid #1e3a5f; color:#475569; font-size:0.78rem;">
  Built by <span style="color:#00d4ff;">Om Patil</span> &nbsp;|&nbsp;
  MSc Data Science, AI and Digital Business &nbsp;|&nbsp;
  Module: M507C Methods of Prediction
</div>
""", unsafe_allow_html=True)
