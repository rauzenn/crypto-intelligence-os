import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
from src.config.settings import settings

# Sync engine for Streamlit
sync_db_url = settings.DATABASE_URL.replace("postgresql+asyncpg", "postgresql")
engine = create_engine(sync_db_url)

st.set_page_config(page_title="JARVIS Crypto OS", layout="wide", page_icon="🧠")

# Styling
st.markdown("""
<style>
    .reportview-container .main .block-container{
        padding-top: 2rem;
    }
    .metric-card {
        background-color: #1E1E1E;
        padding: 15px;
        border-radius: 5px;
        text-align: center;
        border-left: 5px solid #00FF00;
    }
    .risk-critical { border-left: 5px solid #FF0000; }
    .risk-high { border-left: 5px solid #FFA500; }
    .risk-medium { border-left: 5px solid #FFFF00; }
</style>
""", unsafe_allow_html=True)

st.title("🧠 JARVIS Intelligence Panel")

def fetch_table(table_name, limit=100, order_by="id DESC"):
    try:
        with engine.connect() as conn:
            query = f"SELECT * FROM {table_name} ORDER BY {order_by} LIMIT {limit}"
            df = pd.read_sql(query, conn)
            return df
    except Exception as e:
        return pd.DataFrame()

# Sidebar
st.sidebar.title("System Status")
st.sidebar.success("Database: Online")
st.sidebar.success("Event Bus (Redis): Subscribed")
st.sidebar.markdown("---")
st.sidebar.subheader("Active Modules")
st.sidebar.checkbox("Layer A: Ingestion", value=True, disabled=True)
st.sidebar.checkbox("Layer C: Event Bus", value=True, disabled=True)
st.sidebar.checkbox("Layer D: Alpha Radar 2.0", value=True, disabled=True)
st.sidebar.checkbox("Layer F: Wallet Hunter 2.0", value=True, disabled=True)
st.sidebar.checkbox("Layer G: Narrative Engine 2.0", value=True, disabled=True)
st.sidebar.checkbox("Layer H: Risk Engine 2.0", value=True, disabled=True)

if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()

# Layout
col1, col2, col3, col4 = st.columns(4)
with col1:
    events_count = 0
    try:
        with engine.connect() as conn:
            events_count = conn.execute(text("SELECT COUNT(*) FROM events")).scalar()
    except: pass
    st.markdown(f'<div class="metric-card"><h2>{events_count}</h2><p>Processed Events</p></div>', unsafe_allow_html=True)

# Tabs
tab_alerts, tab_wallets, tab_narratives, tab_events = st.tabs([
    "🚨 Alpha Alerts", 
    "🕵️ Wallet Hunter", 
    "📈 Narratives", 
    "📡 Event Stream"
])

with tab_alerts:
    st.subheader("Alpha Signals (Radar 2.0 & Fusion)")
    alerts_df = fetch_table("alerts", order_by="detected_at DESC")
    if not alerts_df.empty:
        for idx, row in alerts_df.iterrows():
            with st.expander(f"{row['detected_at']} | {row['title']} | Asset: {row['asset']}", expanded=(idx==0)):
                content = row.get("content_json", {})
                if isinstance(content, dict):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write(f"**What Changed:** {content.get('what_changed', 'N/A')}")
                        st.write(f"**Score:** {content.get('composite_score', 'N/A')}")
                        st.write(f"**Earlyness:** {content.get('earlyness', 'N/A')}")
                        st.write(f"**Priority:** {content.get('priority', 'N/A')}")
                    with col_b:
                        st.write("**Evidence Graph:**")
                        for ev in content.get('evidence', []):
                            st.write(f"- {ev}")
                        st.write("**Risk Flags:**")
                        for r in content.get('risk_flags', []):
                            st.write(f"- {r}")
                else:
                    st.json(content)
    else:
        st.info("No Alpha Alerts have bypassed the Risk Engine yet.")

with tab_wallets:
    st.subheader("Smart Money Intelligence")
    wallets_df = fetch_table("wallets", order_by="reputation_score DESC")
    if not wallets_df.empty:
        st.dataframe(
            wallets_df[['address', 'lifecycle_state', 'reputation_score', 'confidence', 'win_rate', 'sample_size', 'last_active']],
            use_container_width=True
        )
    else:
        st.write("No wallets tracked in Memory yet.")

with tab_narratives:
    st.subheader("Market Narratives & Lifecycle")
    narr_df = fetch_table("narratives", order_by="mention_velocity DESC")
    if not narr_df.empty:
        st.dataframe(
            narr_df[['topic', 'lifecycle_state', 'mention_velocity', 'capital_flow_usd', 'confidence_score', 'last_updated']],
            use_container_width=True
        )
    else:
        st.write("No narratives emerged yet.")

with tab_events:
    st.subheader("Raw Ingestion Stream")
    events_df = fetch_table("events", limit=100, order_by="timestamp DESC")
    if not events_df.empty:
        st.dataframe(
            events_df[['timestamp', 'event_type', 'asset', 'chain', 'source']], 
            use_container_width=True
        )
    else:
        st.write("No events collected.")
