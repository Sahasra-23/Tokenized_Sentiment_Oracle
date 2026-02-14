# ===============================
# MEMBER 3 – DASHBOARD LAYER
# Fully Integrated Architecture
# ===============================
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
import pandas as pd
import plotly.express as px


# 🔗 Import Member 2 Oracle Engine
from signal_layer.oracle_engine import build_oracle_output_from_processed_csv

# ---------------------------------
# 1️⃣ PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="NarrativePulse | Oracle",
    layout="wide"
)

st.title("⚡ NARRATIVE PULSE ORACLE")

# ---------------------------------
# 2️⃣ LOAD MEMBER 1 OUTPUT
# ---------------------------------

PROCESSED_CSV_PATH = "data/processed_sentiment.csv"

try:
    df = pd.read_csv(PROCESSED_CSV_PATH)
except Exception as e:
    st.error(f"Processed sentiment file not found. Run Member 1 first.\nError: {e}")
    st.stop()

# ---------------------------------
# 3️⃣ RUN MEMBER 2 ORACLE ENGINE
# ---------------------------------

try:
    oracle = build_oracle_output_from_processed_csv(PROCESSED_CSV_PATH)
except Exception as e:
    st.error(f"Oracle engine failed.\nError: {e}")
    st.stop()

# ---------------------------------
# 4️⃣ DISPLAY STATUS
# ---------------------------------

st.markdown(
    f"### STATUS: `{oracle['sentiment_zone'].upper()}` "
    f"// CONFIDENCE: `{oracle['oracle_confidence']}%`"
)

st.markdown("---")

# ---------------------------------
# 5️⃣ METRICS
# ---------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Vibe Score", oracle["vibe_score"])
col2.metric("Sentiment Zone", oracle["sentiment_zone"].upper())
col3.metric("Hype Velocity", oracle["velocity_value"], oracle["hype_velocity"].upper())
col4.metric("Correlation", oracle["correlation_value"])

st.info(f"🤖 ORACLE DECISION: {oracle['contract_action']}")
st.warning(f"⚠ Risk Level: {oracle['risk_level'].upper()}")

st.markdown("---")

# ---------------------------------
# 6️⃣ DAILY TRENDS
# ---------------------------------

daily_df = df.groupby("date").agg(
    daily_avg_sentiment=("daily_avg_sentiment", "first"),
    daily_volume=("daily_volume", "first")
).reset_index()

fig1 = px.line(
    daily_df,
    x="date",
    y="daily_avg_sentiment",
    title="Daily Sentiment Trend"
)

st.plotly_chart(fig1, use_container_width=True)

fig2 = px.bar(
    daily_df,
    x="date",
    y="daily_volume",
    title="Tweet Volume Trend"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------------------------
# 7️⃣ RAW STREAM (OPTIONAL)
# ---------------------------------

if "tweet_text" in df.columns:
    st.markdown("---")
    st.subheader("📡 Latest Narrative Stream")
    st.dataframe(
        df[["date", "tweet_text", "sentiment_score"]].tail(10),
        use_container_width=True
    )
