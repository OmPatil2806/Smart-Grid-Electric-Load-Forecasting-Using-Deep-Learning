import streamlit as st

st.set_page_config(
    page_title="Smart Grid Load Forecasting",
    page_icon="🔌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap');

  :root {
    --navy:      #0a0e1a;
    --card:      #111827;
    --border:    #1e3a5f;
    --blue:      #00d4ff;
    --green:     #22c55e;
    --orange:    #f97316;
    --red:       #ef4444;
    --muted:     #94a3b8;
    --text:      #e2e8f0;
  }

  html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--navy) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif;
  }

  [data-testid="stSidebar"] {
    background: #0d1321 !important;
    border-right: 1px solid var(--border) !important;
  }

  [data-testid="stSidebar"] * { color: var(--text) !important; }

  .sidebar-brand {
    text-align: center;
    padding: 18px 10px 10px;
  }
  .sidebar-brand h1 {
    font-family: 'Orbitron', monospace;
    font-size: 15px;
    font-weight: 700;
    color: var(--blue) !important;
    letter-spacing: 1px;
    line-height: 1.4;
    margin: 6px 0 0;
  }
  .sidebar-brand .icon { font-size: 32px; }

  .sidebar-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 14px 0;
  }

  .sidebar-section-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 2px;
    color: var(--muted) !important;
    text-transform: uppercase;
    margin-bottom: 8px;
    padding-left: 2px;
  }

  /* Metric Cards */
  [data-testid="stMetric"] {
    background: #131d2e !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 10px 14px !important;
    margin-bottom: 6px !important;
  }
  [data-testid="stMetricLabel"] { font-size: 11px !important; color: var(--muted) !important; }
  [data-testid="stMetricValue"] { font-size: 18px !important; color: var(--blue) !important; font-weight: 700 !important; }

  /* Buttons */
  .stButton > button {
    background: linear-gradient(135deg, #0066cc, #00d4ff) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.2s ease !important;
  }
  .stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(0,212,255,0.3) !important;
  }

  /* Radio & Selectbox */
  .stRadio label, .stSelectbox label { color: var(--text) !important; }

  /* Toggle */
  .stToggle label { color: var(--text) !important; }

  /* Slider */
  .stSlider label { color: var(--text) !important; }

  /* Dataframe */
  [data-testid="stDataFrame"] { border-radius: 10px !important; overflow: hidden !important; }

  /* Mobile responsive */
  @media (max-width: 768px) {
    .block-container { padding: 1rem !important; }
  }

  /* Hide Streamlit branding */
  #MainMenu, footer, header { visibility: hidden; }

  /* Scrollbar */
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: var(--navy); }
  ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Session State Defaults ────────────────────────────────────────────────────
if "unit"      not in st.session_state: st.session_state.unit      = "kW"
if "temp_unit" not in st.session_state: st.session_state.temp_unit = "°C"
if "dark_mode" not in st.session_state: st.session_state.dark_mode = True

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
      <div class="icon">🔌</div>
      <h1>Smart Grid<br>Load Forecasting</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-label">⚙️ Settings</div>', unsafe_allow_html=True)

    st.session_state.dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
    st.session_state.unit      = st.radio("📏 Unit",        ["kW", "MW"],  horizontal=True)
    st.session_state.temp_unit = st.radio("🌡️ Temperature", ["°C", "°F"], horizontal=True)

    st.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-section-label">📊 Model Performance</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("✅ Accuracy", "92%")
        st.metric("📉 MAE",     "45.23 kW")
    with col2:
        st.metric("📉 RMSE",   "61.84 kW")
        st.metric("🔢 Epochs", "50")

# ── Home Redirect Content ─────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 80px 20px;">
  <div style="font-size:64px;">🔌</div>
  <h1 style="font-family:'Orbitron',monospace; color:#00d4ff; font-size:2rem; margin:16px 0 8px;">
    Smart Grid Electric Load Forecasting
  </h1>
  <p style="color:#94a3b8; font-size:1.1rem;">
    Navigate using the sidebar pages to get started.
  </p>
</div>
""", unsafe_allow_html=True)
