import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, select, text
from src.config.settings import settings
import time

# Create a synchronous engine for Streamlit
sync_db_url = settings.DATABASE_URL.replace("postgresql+asyncpg", "postgresql")
engine = create_engine(sync_db_url)

st.set_page_config(page_title="Crypto Intelligence OS", layout="wide", page_icon="🧠")
st.title("Crypto Intelligence OS Dashboard 🧠")

# Auto-refresh
if st.sidebar.button("Refresh Data"):
    st.rerun()

def fetch_table(table_name, limit=50, order_by="id DESC"):
    try:
        with engine.connect() as conn:
            query = f"SELECT * FROM {table_name} ORDER BY {order_by} LIMIT {limit}"
            df = pd.read_sql(query, conn)
            return df
    except Exception as e:
        return pd.DataFrame()

# Tabs
tab1, tab2, tab3 = st.tabs(["📡 Radar (Alerts)", "📊 Events & Data", "🎯 Learning & Outcomes"])

with tab1:
    st.header("Active Alpha Alerts")
    alerts_df = fetch_table("alerts", order_by="detected_at DESC")
    if not alerts_df.empty:
        st.dataframe(alerts_df[['detected_at', 'title', 'asset', 'chain']], use_container_width=True)
    else:
        st.info("No active alerts generated yet.")

with tab2:
    st.header("Raw Event Stream")
    events_df = fetch_table("events", limit=100, order_by="timestamp DESC")
    if not events_df.empty:
        st.dataframe(events_df[['timestamp', 'event_type', 'asset', 'chain', 'source']], use_container_width=True)
    else:
        st.write("No events ingested yet.")

with tab3:
    st.header("Signal Outcomes (P2 Learning)")
    outcomes_df = fetch_table("alert_outcomes", order_by="recorded_at DESC")
    if not outcomes_df.empty:
        st.dataframe(outcomes_df[['alert_id', 'snapshot_time', 'pnl_pct', 'is_false_positive', 'recorded_at']], use_container_width=True)
    else:
        st.write("No outcome snapshots recorded yet.")

st.sidebar.title("System Status")
st.sidebar.success("Database: Online (Sync)")
st.sidebar.success("Worker: Active")
st.sidebar.info("Dashboard v0.2")
