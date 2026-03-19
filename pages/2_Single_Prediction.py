import streamlit as st
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helper import (load_model_and_scalers, preprocess_input,
                           create_sequence, predict_load, convert_unit,
                           get_load_category, encode_season, send_email_alert)

st.set_page_config(page_title="Single Prediction | Smart Grid", page_icon="🔮", layout="wide")

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap');
  html, body, [data-testid="stAppViewContainer"] {
    background: #0a0e1a !important; color: #e2e8f0 !important; font-family: 'Inter', sans-serif;
  }
  [data-testid="stSidebar"] { background: #0d1321 !important; border-right: 1px solid #1e3a5f !important; }
  #MainMenu, footer, header { visibility: hidden; }
  .page-title {
    font-family: 'Orbitron', monospace; font-size: 1.6rem; font-weight: 700;
    color: #00d4ff; margin-bottom: 4px;
  }
  .section-card {
    background: #111827; border: 1px solid #1e3a5f; border-radius: 16px; padding: 24px; margin-bottom: 20px;
  }
  .result-box {
    background: linear-gradient(135deg, #0d1f3c, #111827);
    border: 1px solid #00d4ff; border-radius: 16px; padding: 30px; text-align: center;
  }
  .result-value {
    font-family: 'Orbitron', monospace; font-size: 3.5rem; font-weight: 900;
    color: #00d4ff; line-height: 1;
  }
  .result-unit { font-size: 1rem; color: #64748b; margin-top: 4px; }
  .confidence { color: #94a3b8; font-size: 0.85rem; margin-top: 8px; }
  .badge {
    display: inline-block; padding: 6px 18px; border-radius: 50px;
    font-weight: 700; font-size: 0.85rem; margin-top: 10px;
  }
  .section-label { font-size: 10px; font-weight: 600; letter-spacing: 3px; color: #475569; text-transform: uppercase; margin-bottom: 12px; }
  .stButton > button {
    background: linear-gradient(135deg, #0066cc, #00d4ff) !important;
    color: #fff !important; border: none !important; border-radius: 8px !important;
    font-weight: 600 !important; width: 100% !important; padding: 12px !important; font-size: 1rem !important;
  }
  .stSlider label, .stSelectbox label, .stToggle label, .stNumberInput label { color: #e2e8f0 !important; }
  [data-testid="stMetric"] { background: #131d2e !important; border: 1px solid #1e3a5f !important; border-radius: 10px !important; padding: 10px 14px !important; }
  [data-testid="stMetricValue"] { color: #00d4ff !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)

# ── Title ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="page-title">🔮 Single Load Prediction</div>', unsafe_allow_html=True)
st.markdown('<p style="color:#64748b;margin-bottom:24px;">Enter parameters to predict hourly electricity load</p>', unsafe_allow_html=True)

unit = st.session_state.get("unit", "kW")

# ── Input Form ────────────────────────────────────────────────────────────────
with st.container():
    st.markdown('<div class="section-label">⚙️ Input Parameters</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        hour    = st.slider("🕐 Hour of Day", 0, 23, 12)
        weekday = st.selectbox("📆 Weekday", ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
        weekday_num = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"].index(weekday)
        month   = st.selectbox("🗓️ Month", list(range(1,13)),
                               format_func=lambda x: ["Jan","Feb","Mar","Apr","May","Jun",
                                                       "Jul","Aug","Sep","Oct","Nov","Dec"][x-1])
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        season     = st.selectbox("🌤️ Season", ["Dry", "Rainy", "Harmattan"])
        temp_input = st.slider("🌡️ Temperature (°C)", -5.0, 45.0, 25.0, step=0.5)
        load_kw    = st.number_input("⚡ Reference Load (kW)", min_value=0.0, value=450.0, step=10.0)
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        is_weekend  = st.toggle("📅 Is Weekend", value=weekday_num >= 5)
        is_rain_day = st.toggle("🌧️ Is Rain Day", value=False)
        st.markdown("<br>", unsafe_allow_html=True)
        st.info(f"**Day:** {weekday}\n\n**Season:** {season}\n\n**Temp:** {temp_input}°C")
        st.markdown('</div>', unsafe_allow_html=True)

# ── Predict Button ────────────────────────────────────────────────────────────
predict_btn = st.button("⚡ PREDICT LOAD", use_container_width=True)

if predict_btn:
    with st.spinner("🔄 Running LSTM prediction..."):
        try:
            model, feature_scaler, target_scaler = load_model_and_scalers()
            season_enc = encode_season(season)

            input_dict = {
                "load_kw":          load_kw,
                "hour":             hour,
                "weekday":          weekday_num,
                "month":            month,
                "is_weekend":       int(is_weekend),
                "season_dry":       season_enc["season_dry"],
                "season_rainy":     season_enc["season_rainy"],
                "season_harmattan": season_enc["season_harmattan"],
                "temperature":      temp_input,
                "is_rain_day":      int(is_rain_day),
            }

            scaled   = preprocess_input(input_dict, feature_scaler)
            sequence = create_sequence(scaled)
            pred_kw  = predict_load(model, sequence, target_scaler)
            pred_val = convert_unit(pred_kw, unit)
            category, color = get_load_category(pred_kw)
            conf_low  = convert_unit(pred_kw * 0.95, unit)
            conf_high = convert_unit(pred_kw * 1.05, unit)

            st.session_state["last_prediction"] = pred_kw

            # ── Results ───────────────────────────────────────────────────────
            r1, r2 = st.columns([1, 1])

            with r1:
                st.markdown(f"""
                <div class="result-box">
                  <div style="color:#64748b;font-size:0.8rem;letter-spacing:2px;text-transform:uppercase;margin-bottom:8px;">Predicted Load</div>
                  <div class="result-value">{pred_val}</div>
                  <div class="result-unit">{unit}</div>
                  <div class="confidence">Confidence Range: {conf_low} – {conf_high} {unit}</div>
                  <div>
                    <span class="badge" style="background:{color}22;color:{color};border:1px solid {color};">
                      {category} Load
                    </span>
                  </div>
                </div>
                """, unsafe_allow_html=True)

            with r2:
                # Gauge Chart
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=pred_kw,
                    number={"suffix": " kW", "font": {"color": "#00d4ff", "size": 28}},
                    gauge={
                        "axis": {"range": [0, 1000], "tickcolor": "#64748b",
                                 "tickfont": {"color": "#64748b"}},
                        "bar":  {"color": color, "thickness": 0.3},
                        "bgcolor": "#111827",
                        "bordercolor": "#1e3a5f",
                        "steps": [
                            {"range": [0,   300], "color": "#052e16"},
                            {"range": [300, 600], "color": "#1c1008"},
                            {"range": [600, 1000],"color": "#1c0a0a"},
                        ],
                        "threshold": {
                            "line":  {"color": color, "width": 3},
                            "thickness": 0.8,
                            "value": pred_kw
                        }
                    },
                    title={"text": "Load Level (kW)", "font": {"color": "#94a3b8", "size": 14}}
                ))
                fig.update_layout(
                    height=280,
                    paper_bgcolor="#111827",
                    plot_bgcolor="#111827",
                    font={"color": "#94a3b8"},
                    margin=dict(l=20, r=20, t=40, b=10)
                )
                st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")

    # ── Email Alert ───────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-label">📧 Email Alert</div>', unsafe_allow_html=True)
    email_toggle = st.toggle("Enable Email Alert")

    if email_toggle:
        ea1, ea2 = st.columns(2)
        with ea1:
            to_email  = st.text_input("📨 Recipient Email")
        with ea2:
            threshold = st.slider("⚠️ Alert Threshold (kW)", 100, 1000, 600)

        if st.button("📤 Send Alert Email"):
            pred_kw = st.session_state.get("last_prediction", 0)
            if pred_kw > threshold:
                success = send_email_alert(to_email, pred_kw, threshold, hour)
                if success:
                    st.success("✅ Alert email sent successfully!")
                else:
                    st.error("❌ Failed to send email. Check credentials in secrets.")
            else:
                st.info(f"ℹ️ Predicted load ({pred_kw:.1f} kW) is below threshold ({threshold} kW). No alert needed.")
