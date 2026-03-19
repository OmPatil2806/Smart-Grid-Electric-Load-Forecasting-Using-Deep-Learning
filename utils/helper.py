import os
import numpy as np
import pandas as pd
import joblib
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import streamlit as st

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH  = os.path.join(BASE_DIR, "saved_model", "lstm_smartgrid_model.h5")
FSCALER_PATH = os.path.join(BASE_DIR, "saved_model", "feature_scaler.pkl")
TSCALER_PATH = os.path.join(BASE_DIR, "saved_model", "target_scaler.pkl")
DATA_PATH   = os.path.join(BASE_DIR, "data", "smartgrid_5yr_hourly_natural.csv")

FEATURE_COLS = [
    'load_kw', 'hour', 'weekday', 'month',
    'is_weekend', 'season_dry', 'season_rainy',
    'season_harmattan', 'temperature', 'is_rain_day'
]

# ── 1. Load Model & Scalers ───────────────────────────────────────────────────
@st.cache_resource
def load_model_and_scalers():
    from tensorflow.keras.models import load_model
    model          = load_model(MODEL_PATH)
    feature_scaler = joblib.load(FSCALER_PATH)
    target_scaler  = joblib.load(TSCALER_PATH)
    return model, feature_scaler, target_scaler

# ── 2. Preprocess Input ───────────────────────────────────────────────────────
def preprocess_input(input_dict, feature_scaler):
    df = pd.DataFrame([input_dict])[FEATURE_COLS]
    scaled = feature_scaler.transform(df)
    return scaled

# ── 3. Create Sequence ────────────────────────────────────────────────────────
def create_sequence(scaled_input, time_steps=24):
    seq = np.tile(scaled_input, (time_steps, 1))          # (24, 10)
    return seq.reshape(1, time_steps, scaled_input.shape[1])  # (1, 24, 10)

# ── 4. Predict Load ───────────────────────────────────────────────────────────
def predict_load(model, sequence, target_scaler):
    pred_scaled = model.predict(sequence, verbose=0)
    pred_kw     = target_scaler.inverse_transform(pred_scaled)
    return float(pred_kw[0][0])

# ── 5. Convert Unit ───────────────────────────────────────────────────────────
def convert_unit(value_kw, unit):
    if unit == "MW":
        return round(value_kw / 1000, 4)
    return round(value_kw, 2)

# ── 6. Send Email Alert ───────────────────────────────────────────────────────
def send_email_alert(to_email, predicted_load, threshold, hour=None):
    try:
        sender_email = st.secrets["email"]
        password     = st.secrets["password"]

        hour_str = f"Hour {hour}:00" if hour is not None else "current prediction"

        html_body = f"""
        <html><body style="font-family:Arial,sans-serif;background:#0a0e1a;color:#e0e0e0;padding:30px;">
          <div style="max-width:600px;margin:auto;background:#111827;border-radius:12px;
                      border:1px solid #1e3a5f;padding:30px;">
            <h2 style="color:#00d4ff;">⚠️ Smart Grid Load Alert!</h2>
            <p style="color:#94a3b8;">A high electricity load has been detected.</p>
            <table style="width:100%;border-collapse:collapse;margin:20px 0;">
              <tr style="background:#1e3a5f;">
                <td style="padding:12px;color:#94a3b8;">Predicted Load</td>
                <td style="padding:12px;color:#f97316;font-weight:bold;">
                  {predicted_load:.2f} kW
                </td>
              </tr>
              <tr>
                <td style="padding:12px;color:#94a3b8;">Threshold</td>
                <td style="padding:12px;color:#22c55e;font-weight:bold;">
                  {threshold:.2f} kW
                </td>
              </tr>
              <tr style="background:#1e3a5f;">
                <td style="padding:12px;color:#94a3b8;">Time</td>
                <td style="padding:12px;color:#e0e0e0;">{hour_str}</td>
              </tr>
            </table>
            <div style="background:#1e3a5f;border-left:4px solid #f97316;
                        padding:15px;border-radius:8px;margin-top:20px;">
              <p style="margin:0;color:#fbbf24;">
                💡 <strong>Recommendation:</strong> Consider load shedding or 
                activating backup power to avoid grid overload.
              </p>
            </div>
            <p style="color:#475569;font-size:12px;margin-top:20px;">
              — Smart Grid Electric Load Forecasting System | Om Patil
            </p>
          </div>
        </body></html>
        """

        msg = MIMEMultipart("alternative")
        msg["Subject"] = "⚠️ Smart Grid Load Alert!"
        msg["From"]    = sender_email
        msg["To"]      = to_email
        msg.attach(MIMEText(html_body, "html"))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, to_email, msg.as_string())
        return True
    except Exception as e:
        st.error(f"Email error: {e}")
        return False

# ── 7. Get Load Category ──────────────────────────────────────────────────────
def get_load_category(value_kw):
    if value_kw < 300:
        return "Low", "#22c55e"
    elif value_kw <= 600:
        return "Medium", "#f97316"
    else:
        return "High", "#ef4444"

# ── 8. Season Encoder ─────────────────────────────────────────────────────────
def encode_season(season):
    return {
        "season_dry":       1 if season == "Dry"       else 0,
        "season_rainy":     1 if season == "Rainy"     else 0,
        "season_harmattan": 1 if season == "Harmattan" else 0,
    }

# ── 9. Load Dataset ───────────────────────────────────────────────────────────
@st.cache_data
def load_dataset():
    df = pd.read_csv(DATA_PATH)
    bool_cols = ['is_weekend', 'season_dry', 'season_rainy', 'season_harmattan', 'is_rain_day']
    for col in bool_cols:
        if col in df.columns:
            df[col] = df[col].astype(int)
    return df
