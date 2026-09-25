import asyncio
from typing import Dict, Any
from src.utils.logger import logger
from src.event_bus.bus import bus
from src.chain.discovery import ChainDiscoveryEngine

chain_engine = ChainDiscoveryEngine()

async def handle_chain_metrics(message: Dict[str, Any]):
    try:
        event_type = message.get("event_type")
        if event_type == "chain_metrics":
            metadata = message.get("metadata", {})
            chain_name = message.get("chain", "unknown")
            chain_engine.process_chain_metrics(chain_name, metadata)
    except Exception as e:
        logger.error(f"[ChainListener] Error handling event: {e}")

def setup_chain_listeners():
    asyncio.create_task(bus.subscribe("events.normalized", handle_chain_metrics))
    logger.info("[ChainDiscovery] Listeners registered.")
