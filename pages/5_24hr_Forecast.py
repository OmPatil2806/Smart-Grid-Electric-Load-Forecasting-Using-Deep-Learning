import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from datetime import date
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helper import (load_model_and_scalers, preprocess_input,
                           create_sequence, predict_load, convert_unit,
                           get_load_category, encode_season, send_email_alert)

st.set_page_config(page_title="24hr Forecast | Smart Grid", page_icon="🗓️", layout="wide")

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap');
  html, body, [data-testid="stAppViewContainer"] {
    background: #0a0e1a !important; color: #e2e8f0 !important; font-family: 'Inter', sans-serif;
  }
  [data-testid="stSidebar"] { background: #0d1321 !important; border-right: 1px solid #1e3a5f !important; }
  #MainMenu, footer, header { visibility: hidden; }
  .page-title { font-family: 'Orbitron', monospace; font-size: 1.6rem; font-weight: 700; color: #00d4ff; }
  .peak-card {
    background: linear-gradient(135deg, #1c0a0a, #111827);
    border: 1px solid #ef4444; border-radius: 16px; padding: 24px; text-align: center; margin-bottom: 20px;
  }
  .peak-title { font-family: 'Orbitron', monospace; font-size: 0.8rem; color: #ef4444; letter-spacing: 2px; text-transform: uppercase; }
  .peak-value { font-family: 'Orbitron', monospace; font-size: 2.5rem; font-weight: 900; color: #ef4444; margin: 8px 0; }
  .peak-sub   { color: #94a3b8; font-size: 0.85rem; }
  .info-card  { background: #111827; border: 1px solid #1e3a5f; border-radius: 12px; padding: 18px; margin-bottom: 14px; }
  .section-label { font-size: 10px; font-weight: 600; letter-spacing: 3px; color: #475569; text-transform: uppercase; margin-bottom: 12px; }
  .stButton > button {
    background: linear-gradient(135deg, #0066cc, #00d4ff) !important;
    color: #fff !important; border: none !important; border-radius: 8px !important;
    font-weight: 600 !important; width: 100% !important; padding: 12px !important; font-size: 1rem !important;
  }
  .stSlider label, .stSelectbox label, .stToggle label, .stDateInput label { color: #e2e8f0 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">🗓️ 24-Hour Load Forecast</div>', unsafe_allow_html=True)
st.markdown('<p style="color:#64748b;margin-bottom:24px;">Generate an hourly electricity load forecast for a full day</p>', unsafe_allow_html=True)

unit = st.session_state.get("unit", "kW")

# ── Input Parameters ──────────────────────────────────────────────────────────
st.markdown('<div class="section-label">⚙️ Forecast Parameters</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    forecast_date = st.date_input("📅 Forecast Date", value=date.today())
    weekday_num   = forecast_date.weekday()        # 0=Mon, 6=Sun
    is_weekend    = weekday_num >= 5
    weekday_names = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    st.markdown(f"""
    <div class="info-card">
      <div style="color:#64748b;font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;">Auto-Detected</div>
      <div style="margin-top:8px;">
        <span style="color:#00d4ff;font-weight:600;">Day:</span> {weekday_names[weekday_num]}<br>
        <span style="color:#00d4ff;font-weight:600;">Weekend:</span> {"✅ Yes" if is_weekend else "❌ No"}<br>
        <span style="color:#00d4ff;font-weight:600;">Month:</span> {forecast_date.month}
      </div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    temperature = st.slider("🌡️ Expected Temperature (°C)", -5.0, 45.0, 25.0, step=0.5)
    season      = st.selectbox("🌤️ Season", ["Dry", "Rainy", "Harmattan"])

with c3:
    is_rain_day = st.toggle("🌧️ Rain Day", value=False)
    load_ref    = st.number_input("⚡ Reference Load (kW)", min_value=0.0, value=450.0, step=10.0)
    st.markdown("<br>", unsafe_allow_html=True)
    st.info(f"Forecasting **{forecast_date.strftime('%d %B %Y')}**\n\n{weekday_names[weekday_num]} | Temp: {temperature}°C")

# ── Generate Button ───────────────────────────────────────────────────────────
gen_btn = st.button("🗓️ GENERATE 24-HOUR FORECAST", use_container_width=True)

if gen_btn:
    with st.spinner("🔄 Generating forecast for all 24 hours..."):
        try:
            model, feature_scaler, target_scaler = load_model_and_scalers()
            season_enc = encode_season(season)

            hours       = list(range(24))
            predictions = []

            for h in hours:
                input_dict = {
                    "load_kw":          load_ref,
                    "hour":             h,
                    "weekday":          weekday_num,
                    "month":            forecast_date.month,
                    "is_weekend":       int(is_weekend),
                    "season_dry":       season_enc["season_dry"],
                    "season_rainy":     season_enc["season_rainy"],
                    "season_harmattan": season_enc["season_harmattan"],
                    "temperature":      temperature,
                    "is_rain_day":      int(is_rain_day),
                }
                scaled   = preprocess_input(input_dict, feature_scaler)
                sequence = create_sequence(scaled)
                pred_kw  = predict_load(model, sequence, target_scaler)
                predictions.append(pred_kw)

            # Find peak
            peak_idx  = predictions.index(max(predictions))
            peak_load = predictions[peak_idx]
            peak_cat, peak_color = get_load_category(peak_load)

            # ── Peak Card ─────────────────────────────────────────────────────
            st.markdown(f"""
            <div class="peak-card">
              <div class="peak-title">⚡ Peak Hour Alert</div>
              <div class="peak-value">{convert_unit(peak_load, unit):.1f} {unit}</div>
              <div class="peak-sub">
                Hour {peak_idx:02d}:00 &nbsp;|&nbsp;
                <span style="color:{peak_color};font-weight:600;">{peak_cat} Load</span>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Forecast Chart ────────────────────────────────────────────────
            converted_preds = [convert_unit(p, unit) for p in predictions]
            colors_list     = [get_load_category(p)[1] for p in predictions]

            fig = go.Figure()

            # Area fill
            fig.add_trace(go.Scatter(
                x=hours, y=converted_preds,
                fill="tozeroy", fillcolor="rgba(0,212,255,0.05)",
                mode="none", showlegend=False
            ))

            # Main line
            fig.add_trace(go.Scatter(
                x=hours, y=converted_preds,
                mode="lines+markers",
                name="Predicted Load",
                line={"color": "#00d4ff", "width": 2.5},
                marker={"color": colors_list, "size": 9,
                        "line": {"color": "#0a0e1a", "width": 2}}
            ))

            # Peak marker
            fig.add_trace(go.Scatter(
                x=[peak_idx], y=[converted_preds[peak_idx]],
                mode="markers+text",
                name=f"Peak Hour ({peak_idx}:00)",
                marker={"color": "#ef4444", "size": 16, "symbol": "star",
                        "line": {"color": "#fff", "width": 1.5}},
                text=[f"  ⚡ Peak\n{converted_preds[peak_idx]:.1f} {unit}"],
                textposition="top right",
                textfont={"color": "#ef4444", "size": 12}
            ))

            fig.update_layout(
                title=f"24-Hour Load Forecast — {forecast_date.strftime('%d %B %Y')}",
                xaxis_title="Hour of Day",
                yaxis_title=f"Predicted Load ({unit})",
                xaxis={"tickvals": hours, "ticktext": [f"{h:02d}:00" for h in hours],
                       "gridcolor": "#1e3a5f", "linecolor": "#1e3a5f", "tickangle": -45},
                yaxis={"gridcolor": "#1e3a5f", "linecolor": "#1e3a5f"},
                paper_bgcolor="#111827", plot_bgcolor="#111827",
                font={"color": "#94a3b8"},
                legend={"bgcolor": "#0d1321", "bordercolor": "#1e3a5f", "borderwidth": 1},
                height=430
            )
            st.plotly_chart(fig, use_container_width=True)

            # ── Forecast Table ────────────────────────────────────────────────
            st.markdown("### 📋 Hour-by-Hour Breakdown")
            table_df = pd.DataFrame({
                "Hour":                [f"{h:02d}:00" for h in hours],
                f"Predicted Load ({unit})": [round(convert_unit(p, unit), 3) for p in predictions],
                "Category":            [get_load_category(p)[0] for p in predictions],
            })

            def style_category(val):
                colors_map = {"Low": "#052e16", "Medium": "#1c1008", "High": "#1c0a0a"}
                return f"background-color: {colors_map.get(val, '')}; color: white;"

            st.dataframe(
                table_df.style.applymap(style_category, subset=["Category"]),
                use_container_width=True
            )

            # Download
            csv_out = table_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="📥 Download Forecast as CSV",
                data=csv_out,
                file_name=f"forecast_{forecast_date}.csv",
                mime="text/csv",
                use_container_width=True
            )

            # ── Email Alert ───────────────────────────────────────────────────
            st.markdown("---")
            st.markdown('<div class="section-label">📧 Peak Load Email Alert</div>', unsafe_allow_html=True)
            email_toggle = st.toggle("Enable Email Alert for Peak Load")

            if email_toggle:
                ea1, ea2 = st.columns(2)
                with ea1:
                    to_email  = st.text_input("📨 Recipient Email")
                with ea2:
                    threshold = st.slider("⚠️ Alert Threshold (kW)", 100, 1000, 600)

                if st.button("📤 Send Peak Load Alert"):
                    if peak_load > threshold:
                        success = send_email_alert(to_email, peak_load, threshold, hour=peak_idx)
                        if success:
                            st.success("✅ Peak load alert email sent!")
                        else:
                            st.error("❌ Failed to send email.")
                    else:
                        st.info(f"ℹ️ Peak load ({peak_load:.1f} kW) is below threshold ({threshold} kW).")

        except Exception as e:
            st.error(f"❌ Forecast failed: {e}")
