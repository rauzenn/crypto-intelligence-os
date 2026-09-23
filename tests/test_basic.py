import pytest
from src.models.events import Alert, NormalizedEvent
from datetime import datetime

def test_alert_model_formatting():
    alert = Alert(
        title="Whale Accumulation",
        asset="DEGEN",
        chain="Base",
        what_changed="A top 100 wallet bought 5% of supply.",
        why_now="Price dipped 20% in last hour.",
        evidence=["Tx hash: 0x123", "Wallet age: 100 days"],
        earlyness="Early - No social mentions yet.",
        risk_flags=["Low liquidity"],
        sources=["On-chain", "DexScreener"],
        next_to_watch="Watch for social volume increase."
    )
    
    formatted = alert.format_telegram()
    assert "[ALPHA] Whale Accumulation" in formatted
    assert "Asset: DEGEN" in formatted
    assert "- Tx hash: 0x123" in formatted

def test_normalized_event():
    event = NormalizedEvent(
        event_type="swap",
        chain="solana",
        wallet="7Y...",
        asset="WIF",
        source="helius",
        raw_reference="sig_xyz123"
    )
    assert event.chain == "solana"
    assert event.event_type == "swap"
    assert isinstance(event.timestamp, datetime)
