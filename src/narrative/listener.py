import asyncio
from typing import Dict, Any
from src.utils.logger import logger
from src.event_bus.bus import bus
from src.narrative.engine import NarrativeEngine2

narrative_engine = NarrativeEngine2()

async def handle_social_event(message: Dict[str, Any]):
    """
    Subscribes to 'events.normalized' and processes social/news data for narratives.
    """
    try:
        event_type = message.get("event_type")
        
        # 1. Process Text for Narrative Detection
        if event_type in ["social_mention", "news"]:
            metadata = message.get("metadata", {})
            text = metadata.get("text", "")
            source_id = message.get("provenance", {}).get("source_id", "unknown")
            author_id = metadata.get("author", "unknown")
            
            if text:
                detected = narrative_engine.process_social_event(text, source_id, author_id)
                if detected:
                    logger.debug(f"[NarrativeListener] Detected narratives: {detected} in event {message.get('event_id')}")
                    
        # 2. Process Capital Flow for Narrative Validation
        elif event_type in ["market_snapshot", "dex_pair_snapshot"]:
            # Very rough heuristic: if we see market data, we attempt to map it to a narrative
            # In a real system, the token->narrative mapping would be retrieved from Memory Layer
            # For demonstration, we'll mock a flow if metadata has volume
            volume = float(message.get("metadata", {}).get("volume24h", 0) or 0)
            if volume > 500_000:
                # Mocking that this volume was for the AI narrative
                narrative_engine.integrate_market_data("AI", capital_flow=volume * 0.01, token_activity=5.0)

    except Exception as e:
        logger.error(f"[NarrativeListener] Error handling event: {e}")

def setup_narrative_listeners():
    """Register all narrative engine subscriptions to the event bus."""
    asyncio.create_task(bus.subscribe("events.normalized", handle_social_event))
    logger.info("[NarrativeEngine] Listeners registered.")
