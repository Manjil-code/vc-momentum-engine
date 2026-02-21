import streamlit as st
import requests
import pandas as pd
import os

# ==============================
# CONFIG
# ==============================

API_BASE = "https://vc-momentum-api.onrender.com"

st.set_page_config(
    page_title="VC Momentum Intelligence Platform",
    layout="wide"
)

st.title("🚀 VC Momentum Intelligence Platform")
st.caption("AI Classification • Time-Decay Scoring • Sector Analytics • Statistical Anomaly Detection")


# ==============================
# SAFE API CALL FUNCTION
# ==============================

def fetch_data(endpoint):
    try:
        response = requests.get(f"{API_BASE}/{endpoint}", timeout=15)

        if response.status_code == 200:
            data = response.json()

            # Ensure it's a list (valid dataframe format)
            if isinstance(data, list):
                return pd.DataFrame(data)
            else:
                st.error(f"Unexpected response format from /{endpoint}")
                return pd.DataFrame()

        else:
            st.error(f"API Error {response.status_code}: {response.text}")
            return pd.DataFrame()

    except Exception as e:
        st.error(f"Connection error: {e}")
        return pd.DataFrame()


# ==============================
# LOAD DATA
# ==============================

ranking_df = fetch_data("rankings")
sector_df = fetch_data("sectors")
region_df = fetch_data("regions")
breakout_df = fetch_data("breakouts")
anomaly_df = fetch_data("anomalies")


# ==============================
# KPI SECTION
# ==============================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Companies Ranked", len(ranking_df))

with col2:
    avg_score = round(ranking_df["momentum_score"].mean(), 2) if not ranking_df.empty and "momentum_score" in ranking_df.columns else 0
    st.metric("Avg Momentum", avg_score)

with col3:
    top_sector = sector_df.iloc[0]["sector"] if not sector_df.empty else "N/A"
    st.metric("Top Sector", top_sector)

with col4:
    st.metric("Anomalies Detected", len(anomaly_df))


st.divider()


# ==============================
# MOMENTUM RANKINGS
# ==============================

st.subheader("🏆 Top Momentum Companies")

if not ranking_df.empty:
    st.dataframe(ranking_df.sort_values("momentum_score", ascending=False), use_container_width=True)
else:
    st.info("No ranking data available.")


# ==============================
# SECTOR ANALYTICS
# ==============================

st.subheader("📊 Sector Momentum")

if not sector_df.empty:
    st.bar_chart(sector_df.set_index("sector")["momentum_score"])
else:
    st.info("No sector data available.")


# ==============================
# REGION ANALYTICS
# ==============================

st.subheader("🌍 Regional Momentum")

if not region_df.empty:
    st.bar_chart(region_df.set_index("region")["momentum_score"])
else:
    st.info("No region data available.")


# ==============================
# BREAKOUT CANDIDATES
# ==============================

st.subheader("🚀 Breakout Candidates")

if not breakout_df.empty:
    st.dataframe(breakout_df, use_container_width=True)
else:
    st.info("No breakout candidates detected.")


# ==============================
# ANOMALY DETECTION
# ==============================

st.subheader("⚠️ Statistical Anomalies")

if not anomaly_df.empty:
    st.dataframe(anomaly_df, use_container_width=True)
else:
    st.info("No anomalies detected.")
