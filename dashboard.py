import streamlit as st
import pandas as pd
import requests

API_BASE = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="VC Momentum Intelligence",
    layout="wide"
)

st.title("🚀 VC Momentum Intelligence Platform")
st.caption("AI Classification • Time-Decay Scoring • Sector Analytics • Statistical Anomaly Detection")

# ----------------------------------------
# API Helper
# ----------------------------------------

def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_BASE}/{endpoint}")
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            st.error(f"API returned {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"API connection error: {e}")
        return pd.DataFrame()

# ----------------------------------------
# Fetch Data
# ----------------------------------------

ranking_df = fetch_data("rankings")
sector_df = fetch_data("sectors")
region_df = fetch_data("regions")
breakout_df = fetch_data("breakouts")
anomaly_df = fetch_data("anomalies")

# ----------------------------------------
# Executive Metrics
# ----------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Companies Ranked", len(ranking_df))

with col2:
    if not ranking_df.empty:
        st.metric("Avg Momentum", round(ranking_df["momentum_score"].mean(), 2))
    else:
        st.metric("Avg Momentum", 0)

with col3:
    if not sector_df.empty:
        st.metric("Top Sector", sector_df.iloc[0]["sector"])
    else:
        st.metric("Top Sector", "N/A")

with col4:
    st.metric("Anomalies Detected", len(anomaly_df))

st.divider()

# ----------------------------------------
# Top Momentum Companies
# ----------------------------------------

st.subheader("🔥 Top Momentum Companies")

if not ranking_df.empty:
    st.dataframe(ranking_df.head(15), use_container_width=True)
else:
    st.info("No ranking data available.")

# ----------------------------------------
# Sector Intelligence
# ----------------------------------------

st.subheader("🏭 Sector Momentum")

if not sector_df.empty:
    st.bar_chart(sector_df.set_index("sector")["momentum_score"])

# ----------------------------------------
# Region Intelligence
# ----------------------------------------

st.subheader("🌍 Region Momentum")

if not region_df.empty:
    st.bar_chart(region_df.set_index("region")["momentum_score"])

# ----------------------------------------
# Breakout Detection
# ----------------------------------------

st.subheader("🚨 Breakout Candidates")

if not breakout_df.empty:
    st.dataframe(breakout_df, use_container_width=True)
else:
    st.info("No breakout spikes detected.")

# ----------------------------------------
# Statistical Anomaly Detection
# ----------------------------------------

st.subheader("📈 Statistical Anomalies (Z-Score > 2)")

if not anomaly_df.empty:
    st.dataframe(anomaly_df, use_container_width=True)
else:
    st.success("No statistical anomalies detected.")

st.divider()
st.caption("VC Momentum Engine v2.0 • Built with FastAPI, Streamlit, and Transformer-based NLP")
