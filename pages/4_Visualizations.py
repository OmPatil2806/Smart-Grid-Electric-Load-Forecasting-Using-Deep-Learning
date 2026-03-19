import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.helper import load_dataset

st.set_page_config(page_title="Visualizations | Smart Grid", page_icon="📊", layout="wide")

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600&display=swap');
  html, body, [data-testid="stAppViewContainer"] {
    background: #0a0e1a !important; color: #e2e8f0 !important; font-family: 'Inter', sans-serif;
  }
  [data-testid="stSidebar"] { background: #0d1321 !important; border-right: 1px solid #1e3a5f !important; }
  #MainMenu, footer, header { visibility: hidden; }
  .page-title { font-family: 'Orbitron', monospace; font-size: 1.6rem; font-weight: 700; color: #00d4ff; }
  .chart-card { background: #111827; border: 1px solid #1e3a5f; border-radius: 16px; padding: 20px; margin-bottom: 20px; }
  .section-label { font-size: 10px; font-weight: 600; letter-spacing: 3px; color: #475569; text-transform: uppercase; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)

PLOTLY_LAYOUT = dict(
    paper_bgcolor="#111827", plot_bgcolor="#111827",
    font={"color": "#94a3b8", "family": "Inter"},
    xaxis={"gridcolor": "#1e3a5f", "linecolor": "#1e3a5f"},
    yaxis={"gridcolor": "#1e3a5f", "linecolor": "#1e3a5f"},
    legend={"bgcolor": "#0d1321", "bordercolor": "#1e3a5f", "borderwidth": 1},
    height=380
)

st.markdown('<div class="page-title">📊 Data Visualizations</div>', unsafe_allow_html=True)
st.markdown('<p style="color:#64748b;margin-bottom:24px;">Explore electricity load patterns from the smart grid dataset</p>', unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
with st.spinner("Loading dataset..."):
    try:
        df = load_dataset()
    except Exception as e:
        st.error(f"❌ Could not load dataset: {e}")
        st.stop()

# ── Sidebar Filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("---")
    st.markdown("### 🎛️ Filters")

    hour_range = st.slider("🕐 Hour Range", 0, 23, (0, 23))

    season_options = []
    if "season_dry"       in df.columns: season_options.append("Dry")
    if "season_rainy"     in df.columns: season_options.append("Rainy")
    if "season_harmattan" in df.columns: season_options.append("Harmattan")

    selected_seasons = st.multiselect("🌤️ Season", season_options, default=season_options)
    day_type = st.radio("📆 Day Type", ["All", "Weekday", "Weekend"])

# ── Apply Filters ─────────────────────────────────────────────────────────────
filtered = df.copy()

if "hour" in filtered.columns:
    filtered = filtered[(filtered["hour"] >= hour_range[0]) & (filtered["hour"] <= hour_range[1])]

# Season filter
if selected_seasons and len(selected_seasons) < len(season_options):
    season_mask = pd.Series([False] * len(filtered), index=filtered.index)
    if "Dry"       in selected_seasons and "season_dry"       in filtered.columns:
        season_mask |= filtered["season_dry"] == 1
    if "Rainy"     in selected_seasons and "season_rainy"     in filtered.columns:
        season_mask |= filtered["season_rainy"] == 1
    if "Harmattan" in selected_seasons and "season_harmattan" in filtered.columns:
        season_mask |= filtered["season_harmattan"] == 1
    filtered = filtered[season_mask]

# Day type filter
if day_type == "Weekday" and "is_weekend" in filtered.columns:
    filtered = filtered[filtered["is_weekend"] == 0]
elif day_type == "Weekend" and "is_weekend" in filtered.columns:
    filtered = filtered[filtered["is_weekend"] == 1]

st.markdown(f'<p style="color:#475569;font-size:0.8rem;">Showing {len(filtered):,} records after filters</p>', unsafe_allow_html=True)

import pandas as pd

# ── Chart 1 — Hourly Load Pattern ─────────────────────────────────────────────
st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Chart 1 — Hourly Load Pattern</div>', unsafe_allow_html=True)

if "hour" in filtered.columns and "load_kw" in filtered.columns and len(filtered) > 0:
    hourly_avg = filtered.groupby("hour")["load_kw"].mean().reset_index()
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(
        x=hourly_avg["hour"],
        y=hourly_avg["load_kw"],
        mode="lines+markers",
        name="Avg Load",
        line={"color": "#00d4ff", "width": 2.5},
        marker={"color": "#00d4ff", "size": 7,
                "line": {"color": "#0a0e1a", "width": 2}},
        fill="tozeroy",
        fillcolor="rgba(0,212,255,0.06)"
    ))
    fig1.update_layout(
        title="Average Electricity Load by Hour of Day",
        xaxis_title="Hour of Day",
        yaxis_title="Average Load (kW)",
        xaxis={"tickvals": list(range(0, 24)), "gridcolor": "#1e3a5f", "linecolor": "#1e3a5f"},
        **{k: v for k, v in PLOTLY_LAYOUT.items() if k != "xaxis"}
    )
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.info("Not enough data for hourly chart with current filters.")

st.markdown('</div>', unsafe_allow_html=True)

# ── Chart 2 — Temperature vs Load Scatter ─────────────────────────────────────
st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.markdown('<div class="section-label">Chart 2 — Temperature vs Load Scatter</div>', unsafe_allow_html=True)

if "temperature" in filtered.columns and "load_kw" in filtered.columns and len(filtered) > 0:
    # Add season label column
    plot_df = filtered.copy()
    def get_season_label(row):
        if row.get("season_dry", 0) == 1:       return "Dry"
        elif row.get("season_rainy", 0) == 1:   return "Rainy"
        elif row.get("season_harmattan", 0) == 1: return "Harmattan"
        return "Unknown"

    plot_df["Season"] = plot_df.apply(get_season_label, axis=1)

    color_map = {"Dry": "#f97316", "Rainy": "#00d4ff", "Harmattan": "#22c55e", "Unknown": "#94a3b8"}

    fig2 = px.scatter(
        plot_df.sample(min(3000, len(plot_df))),   # sample for performance
        x="temperature", y="load_kw",
        color="Season",
        color_discrete_map=color_map,
        opacity=0.6,
        title="Temperature vs Electricity Load",
        labels={"temperature": "Temperature (°C)", "load_kw": "Load (kW)"}
    )
    fig2.update_traces(marker_size=4)
    fig2.update_layout(**PLOTLY_LAYOUT)
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Not enough data for temperature scatter with current filters.")

st.markdown('</div>', unsafe_allow_html=True)
