import asyncio
from typing import Dict, Any
from src.utils.logger import logger
from src.event_bus.bus import bus
from src.detection.radar import AlphaRadar
from src.normalization.events import NormalizedEvent, Provenance

radar = AlphaRadar()

async def handle_normalized_event(message: Dict[str, Any]):
    """
    Subscribes to 'events.normalized'
    Routes the event to the appropriate detectors (AlphaRadar, NarrativeEngine, etc.)
    """
    logger.debug(f"[DetectionEngine] Received event via EventBus: {message.get('event_type')}")
    try:
        # Reconstruct the NormalizedEvent from dict
        prov_data = message.get("provenance", {})
        provenance = Provenance(**prov_data)
        
        event = NormalizedEvent(
            event_id=message.get("event_id"),
            event_type=message.get("event_type"),
            chain=message.get("chain"),
            wallet=message.get("wallet"),
            asset=message.get("asset"),
            provenance=provenance,
            metadata=message.get("metadata", {})
        )
        
        # 1. Feed to Alpha Radar (Market Anomaly detection)
        # Context is real context; for now it's empty as per "FAKE DATA YASAK"
        # In the future, this will query the Memory/Knowledge layer
        context = {}
        alert = await radar.process_event(event, context)
        
        if alert:
            logger.info(f"ALPHA ALERT GENERATED via EventBus: {alert.title}")
            from src.interface.telegram_service import send_alert
            await send_alert(alert.format_telegram())
            
    except Exception as e:
        logger.error(f"[DetectionEngine] Error handling event: {e}")

def setup_detection_listeners():
    """Register all detection engine subscriptions to the event bus."""
    # We schedule the subscription to run in the current event loop
    asyncio.create_task(bus.subscribe("events.normalized", handle_normalized_event))
    logger.info("[DetectionEngine] Listeners registered.")
