import streamlit as st

st.set_page_config(page_title="About | Smart Grid", page_icon="ℹ️", layout="wide")

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap');
  html, body, [data-testid="stAppViewContainer"] {
    background: #0a0e1a !important; color: #e2e8f0 !important; font-family: 'Inter', sans-serif;
  }
  [data-testid="stSidebar"] { background: #0d1321 !important; border-right: 1px solid #1e3a5f !important; }
  #MainMenu, footer, header { visibility: hidden; }
  .page-title { font-family: 'Orbitron', monospace; font-size: 1.6rem; font-weight: 700; color: #00d4ff; }
  .dev-card {
    background: linear-gradient(135deg, #0d1f3c, #111827);
    border: 1px solid #00d4ff; border-radius: 20px; padding: 32px; text-align: center; margin-bottom: 24px;
  }
  .dev-avatar {
    width: 80px; height: 80px; border-radius: 50%;
    background: linear-gradient(135deg, #0066cc, #00d4ff);
    display: flex; align-items: center; justify-content: center;
    font-size: 36px; margin: 0 auto 16px;
  }
  .dev-name { font-family: 'Orbitron', monospace; font-size: 1.4rem; font-weight: 700; color: #00d4ff; }
  .dev-role { color: #94a3b8; font-size: 0.9rem; margin-top: 6px; }
  .info-card { background: #111827; border: 1px solid #1e3a5f; border-radius: 16px; padding: 24px; margin-bottom: 16px; }
  .info-card h3 { font-family: 'Orbitron', monospace; font-size: 0.85rem; color: #00d4ff; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 14px; }
  .layer-row {
    display: flex; align-items: center; gap: 10px; margin-bottom: 10px;
  }
  .layer-box {
    flex: 1; padding: 10px 14px; border-radius: 8px; font-size: 0.82rem; font-weight: 600; text-align: center;
  }
  .arrow { color: #475569; font-size: 1.2rem; }
  .badge-row { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; }
  .badge {
    padding: 5px 14px; border-radius: 50px; font-size: 0.75rem;
    font-weight: 600; border: 1px solid;
  }
  .section-label { font-size: 10px; font-weight: 600; letter-spacing: 3px; color: #475569; text-transform: uppercase; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">ℹ️ About This Project</div>', unsafe_allow_html=True)
st.markdown('<p style="color:#64748b;margin-bottom:24px;">Project details, developer info, and model architecture</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

# ── Developer Card ────────────────────────────────────────────────────────────
with col1:
    st.markdown("""
    <div class="dev-card">
      <div class="dev-avatar">👤</div>
      <div class="dev-name">Om Patil</div>
      <div class="dev-role">
        🎓 MSc Data Science, AI and Digital Business<br>
        📦 Module: M507C — Methods of Prediction<br><br>
        <span style="color:#00d4ff;">Smart Grid Electric Load Forecasting</span><br>
        <span style="color:#475569;font-size:0.8rem;">Using Deep Learning (LSTM)</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Project Description
    st.markdown("""
    <div class="info-card">
      <h3>📋 Project Description</h3>
      <p style="color:#94a3b8;font-size:0.88rem;line-height:1.7;">
        This project develops a deep learning pipeline for accurate short-term 
        electricity load forecasting using 5 years of smart grid data. The LSTM 
        model learns temporal, seasonal, and weather-driven patterns to predict 
        hourly power demand — helping utility operators optimize generation, 
        reduce costs, and maintain grid stability.
      </p>
      <div style="margin-top:12px;">
        <div style="color:#64748b;font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Dataset</div>
        <a href="https://www.kaggle.com/datasets/emperorgraphics/hourly-load-consumption-data"
           style="color:#00d4ff;font-size:0.85rem;">
          📁 Kaggle — Hourly Load Consumption Data
        </a>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Model Architecture ────────────────────────────────────────────────────────
with col2:
    st.markdown("""
    <div class="info-card">
      <h3>🏗️ LSTM Model Architecture</h3>

      <div class="layer-row">
        <div class="layer-box" style="background:#0d1f3c;color:#00d4ff;border:1px solid #00d4ff;">
          Input<br><span style="font-size:0.7rem;color:#64748b;">(24, 10)</span>
        </div>
      </div>
      <div style="text-align:center;color:#475569;">↓</div>

      <div class="layer-row">
        <div class="layer-box" style="background:#052e16;color:#22c55e;border:1px solid #22c55e;">
          LSTM (128 units)<br><span style="font-size:0.7rem;">return_sequences=True</span>
        </div>
      </div>
      <div style="text-align:center;color:#475569;">↓ Dropout (0.3)</div>

      <div class="layer-row">
        <div class="layer-box" style="background:#052e16;color:#22c55e;border:1px solid #22c55e;">
          LSTM (64 units)<br><span style="font-size:0.7rem;">return_sequences=True</span>
        </div>
      </div>
      <div style="text-align:center;color:#475569;">↓ Dropout (0.3)</div>

      <div class="layer-row">
        <div class="layer-box" style="background:#052e16;color:#22c55e;border:1px solid #22c55e;">
          LSTM (32 units)
        </div>
      </div>
      <div style="text-align:center;color:#475569;">↓ Dropout (0.3)</div>

      <div class="layer-row">
        <div class="layer-box" style="background:#1c0a0a;color:#f97316;border:1px solid #f97316;">
          Dense (1) — Output
        </div>
      </div>

      <div style="margin-top:16px;display:flex;gap:12px;flex-wrap:wrap;">
        <div style="flex:1;min-width:120px;background:#131d2e;border:1px solid #1e3a5f;border-radius:8px;padding:10px;text-align:center;">
          <div style="color:#64748b;font-size:0.7rem;text-transform:uppercase;">Optimizer</div>
          <div style="color:#00d4ff;font-weight:700;font-size:0.9rem;">Adam</div>
          <div style="color:#475569;font-size:0.72rem;">lr = 0.0005</div>
        </div>
        <div style="flex:1;min-width:120px;background:#131d2e;border:1px solid #1e3a5f;border-radius:8px;padding:10px;text-align:center;">
          <div style="color:#64748b;font-size:0.7rem;text-transform:uppercase;">Loss</div>
          <div style="color:#00d4ff;font-weight:700;font-size:0.9rem;">MSE</div>
          <div style="color:#475569;font-size:0.72rem;">Mean Squared Error</div>
        </div>
        <div style="flex:1;min-width:120px;background:#131d2e;border:1px solid #1e3a5f;border-radius:8px;padding:10px;text-align:center;">
          <div style="color:#64748b;font-size:0.7rem;text-transform:uppercase;">Accuracy</div>
          <div style="color:#22c55e;font-weight:700;font-size:0.9rem;">92%</div>
          <div style="color:#475569;font-size:0.72rem;">±5% tolerance</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Tech Stack
    st.markdown("""
    <div class="info-card">
      <h3>🛠️ Tech Stack</h3>
      <div class="badge-row">
        <span class="badge" style="color:#00d4ff;border-color:#00d4ff;background:#0d1f3c;">Streamlit</span>
        <span class="badge" style="color:#f97316;border-color:#f97316;background:#1c1008;">TensorFlow</span>
        <span class="badge" style="color:#22c55e;border-color:#22c55e;background:#052e16;">Keras</span>
        <span class="badge" style="color:#a78bfa;border-color:#a78bfa;background:#1a1030;">Pandas</span>
        <span class="badge" style="color:#60a5fa;border-color:#60a5fa;background:#0d1f3c;">NumPy</span>
        <span class="badge" style="color:#f472b6;border-color:#f472b6;background:#1c0a14;">Plotly</span>
        <span class="badge" style="color:#34d399;border-color:#34d399;background:#052e1a;">Scikit-learn</span>
        <span class="badge" style="color:#fbbf24;border-color:#fbbf24;background:#1c1408;">Joblib</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:32px;padding:20px;
            border-top:1px solid #1e3a5f;color:#475569;font-size:0.78rem;">
  © 2026 Om Patil &nbsp;|&nbsp; Smart Grid Electric Load Forecasting &nbsp;|&nbsp;
  MSc Data Science, AI and Digital Business
</div>
""", unsafe_allow_html=True)
