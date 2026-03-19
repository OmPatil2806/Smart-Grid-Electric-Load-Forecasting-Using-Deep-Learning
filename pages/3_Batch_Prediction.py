import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import io, sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helper import (load_model_and_scalers, preprocess_input,
                           create_sequence, predict_load, convert_unit, get_load_category)

st.set_page_config(page_title="Batch Prediction | Smart Grid", page_icon="📅", layout="wide")

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap');
  html, body, [data-testid="stAppViewContainer"] {
    background: #0a0e1a !important; color: #e2e8f0 !important; font-family: 'Inter', sans-serif;
  }
  [data-testid="stSidebar"] { background: #0d1321 !important; border-right: 1px solid #1e3a5f !important; }
  #MainMenu, footer, header { visibility: hidden; }
  .page-title { font-family: 'Orbitron', monospace; font-size: 1.6rem; font-weight: 700; color: #00d4ff; }
  .info-card { background: #111827; border: 1px solid #1e3a5f; border-radius: 12px; padding: 20px; margin-bottom: 16px; }
  .stButton > button {
    background: linear-gradient(135deg, #0066cc, #00d4ff) !important;
    color: #fff !important; border: none !important; border-radius: 8px !important; font-weight: 600 !important;
  }
  [data-testid="stMetric"] { background: #131d2e !important; border: 1px solid #1e3a5f !important; border-radius: 10px !important; padding: 10px 14px !important; }
  [data-testid="stMetricValue"] { color: #00d4ff !important; font-weight: 700 !important; }
  .required-cols { background: #131d2e; border: 1px solid #1e3a5f; border-radius: 8px; padding: 14px; font-size: 0.8rem; color: #94a3b8; }
</style>
""", unsafe_allow_html=True)

REQUIRED_COLS = ['load_kw','hour','weekday','month','is_weekend',
                 'season_dry','season_rainy','season_harmattan','temperature','is_rain_day']

st.markdown('<div class="page-title">📅 Batch CSV Prediction</div>', unsafe_allow_html=True)
st.markdown('<p style="color:#64748b;margin-bottom:24px;">Upload a CSV file to predict load for multiple rows at once</p>', unsafe_allow_html=True)

# ── Required Columns Info ─────────────────────────────────────────────────────
with st.expander("📋 Required CSV Columns"):
    st.markdown(f"""
    <div class="required-cols">
      Your CSV must contain these columns:<br><br>
      <code>{', '.join(REQUIRED_COLS)}</code>
    </div>
    """, unsafe_allow_html=True)

# ── File Uploader ─────────────────────────────────────────────────────────────
uploaded = st.file_uploader("📂 Upload CSV File", type=["csv"])

if uploaded:
    try:
        df = pd.read_csv(uploaded)
        file_size = uploaded.size / 1024

        # Sidebar file info
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 📁 File Info")
            st.metric("Rows",    f"{len(df):,}")
            st.metric("Columns", f"{len(df.columns)}")
            st.metric("Size",    f"{file_size:.1f} KB")

        st.markdown("**Preview (first 5 rows):**")
        st.dataframe(df.head(), use_container_width=True)

        # Validate columns
        missing = [c for c in REQUIRED_COLS if c not in df.columns]
        if missing:
            st.error(f"❌ Missing required columns: {', '.join(missing)}")
            st.stop()

        st.success(f"✅ File validated — {len(df):,} rows ready for prediction")

        if st.button("⚡ Run Batch Prediction", use_container_width=True):
            with st.spinner(f"🔄 Running predictions on {len(df):,} rows..."):
                model, feature_scaler, target_scaler = load_model_and_scalers()
                unit = st.session_state.get("unit", "kW")

                predictions = []
                progress = st.progress(0)

                for i, row in df.iterrows():
                    input_dict = {col: row[col] for col in REQUIRED_COLS}
                    scaled     = preprocess_input(input_dict, feature_scaler)
                    sequence   = create_sequence(scaled)
                    pred_kw    = predict_load(model, sequence, target_scaler)
                    predictions.append(pred_kw)
                    progress.progress((i + 1) / len(df))

                df["Predicted_Load_kW"] = predictions
                df["Load_Category"]     = [get_load_category(p)[0] for p in predictions]

                progress.empty()
                st.success(f"✅ Predictions complete for {len(df):,} rows!")

                # Sidebar summary stats
                with st.sidebar:
                    st.markdown("### 📊 Prediction Summary")
                    st.metric("Min Load",  f"{min(predictions):.1f} kW")
                    st.metric("Max Load",  f"{max(predictions):.1f} kW")
                    st.metric("Avg Load",  f"{np.mean(predictions):.1f} kW")

                # Results table
                st.markdown("### 📋 Results Table")
                st.dataframe(df, use_container_width=True)

                # Chart
                st.markdown("### 📈 Predicted Load Chart")
                fig = go.Figure()

                if "load_kw" in df.columns:
                    fig.add_trace(go.Scatter(
                        y=df["load_kw"].values,
                        mode="lines", name="Actual Load",
                        line={"color": "#22c55e", "width": 1.5}
                    ))

                fig.add_trace(go.Scatter(
                    y=predictions,
                    mode="lines", name="Predicted Load",
                    line={"color": "#00d4ff", "width": 2}
                ))

                fig.update_layout(
                    title="Actual vs Predicted Load",
                    xaxis_title="Row Index",
                    yaxis_title=f"Load ({unit})",
                    paper_bgcolor="#111827",
                    plot_bgcolor="#111827",
                    font={"color": "#94a3b8"},
                    legend={"bgcolor": "#0d1321", "bordercolor": "#1e3a5f", "borderwidth": 1},
                    xaxis={"gridcolor": "#1e3a5f"},
                    yaxis={"gridcolor": "#1e3a5f"},
                    height=400
                )
                st.plotly_chart(fig, use_container_width=True)

                # Download
                csv_out = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv_out,
                    file_name="smart_grid_predictions.csv",
                    mime="text/csv",
                    use_container_width=True
                )

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
else:
    st.markdown("""
    <div style="text-align:center;padding:60px;background:#111827;border:2px dashed #1e3a5f;
                border-radius:16px;color:#475569;">
      <div style="font-size:48px;margin-bottom:12px;">📂</div>
      <div style="font-size:1rem;">Upload a CSV file to get started</div>
      <div style="font-size:0.8rem;margin-top:6px;">Supports up to thousands of rows</div>
    </div>
    """, unsafe_allow_html=True)
