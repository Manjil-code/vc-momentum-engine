import streamlit as st
import sqlite3
import pandas as pd
from scout.ranking import MomentumRanking

DB_PATH = "data/signals.db"

st.set_page_config(layout="wide")

st.title("🚀 VC Momentum Intelligence Dashboard")

# Load raw signals
conn = sqlite3.connect(DB_PATH)
signals_df = pd.read_sql("SELECT * FROM signals", conn)

if signals_df.empty:
    st.warning("No signals found. Run ingest.py first.")
    st.stop()

# Compute ranking
ranking_df = MomentumRanking.compute()

# Sidebar filters
st.sidebar.header("Filters")

selected_entity = st.sidebar.selectbox(
    "Select Company",
    ["All"] + sorted(signals_df["entity_name"].unique())
)

selected_category = st.sidebar.multiselect(
    "Signal Category",
    signals_df["category_tag"].unique()
)

filtered_df = signals_df.copy()

if selected_entity != "All":
    filtered_df = filtered_df[filtered_df["entity_name"] == selected_entity]

if selected_category:
    filtered_df = filtered_df[filtered_df["category_tag"].isin(selected_category)]

# Layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔥 Top 10 Momentum Companies")
    st.dataframe(ranking_df.head(10))

with col2:
    st.subheader("📊 Signal Category Distribution")
    category_counts = signals_df["category_tag"].value_counts()
    st.bar_chart(category_counts)

st.subheader("📈 All Signals")
st.dataframe(filtered_df.sort_values("confidence_score", ascending=False))

# Export
st.download_button(
    "Download Filtered Signals as CSV",
    filtered_df.to_csv(index=False),
    file_name="filtered_signals.csv"
)
