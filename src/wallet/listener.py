import asyncio
from typing import Dict, Any
from src.utils.logger import logger
from src.event_bus.bus import bus
from src.wallet.hunter import WalletHunter2
from src.normalization.events import NormalizedEvent, Provenance

hunter = WalletHunter2()

async def handle_wallet_event(message: Dict[str, Any]):
    """
    Subscribes to 'events.normalized' to catch wallet movements.
    """
    try:
        event_type = message.get("event_type")
        if event_type not in ["wallet_transfer", "swap"]:
            return # Ignore non-wallet events
            
        wallet_address = message.get("wallet")
        if not wallet_address:
            return
            
        logger.debug(f"[WalletListener] Received wallet event for {wallet_address}")
        
        # In a real scenario, this is where we query recent trades from the DB for this wallet
        # and feed it to the hunter. For now we use the event directly or mock the history fetch.
        mock_history = [
            {"pnl_pct": 50.0, "pnl_usd": 1500.0, "lead_time_hours": 24.5}
        ]
        
        profile = hunter.analyze_history(
            address=wallet_address,
            chain=message.get("chain", "unknown"),
            trade_history=mock_history
        )
        
        # We can also persist the profile to the DB here
        
    except Exception as e:
        logger.error(f"[WalletListener] Error handling event: {e}")

def setup_wallet_listeners():
    """Register all wallet engine subscriptions to the event bus."""
    asyncio.create_task(bus.subscribe("events.normalized", handle_wallet_event))
    logger.info("[WalletHunter] Listeners registered.")
