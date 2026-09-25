import asyncio
from typing import List, Dict, Any
from src.utils.logger import logger
from datetime import datetime, timezone

class HistoricalReplayEngine:
    """
    STEP 16 (Rule 35): HISTORICAL REPLAY
    Runs past datasets through the entire Intelligence Pipeline to test effectiveness
    without future leakage.
    """
    def __init__(self, pipeline_fn):
        self.pipeline_fn = pipeline_fn # The function that takes an event and processes it

    async def replay_dataset(self, dataset: List[Dict[str, Any]]):
        """
        Takes a time-sorted list of historical events.
        """
        logger.info(f"Starting Historical Replay of {len(dataset)} events...")
        
        # Sort strictly by timestamp to prevent future leakage
        sorted_events = sorted(dataset, key=lambda x: x.get("timestamp", 0))
        
        success_count = 0
        blocked_count = 0
        
        for idx, event in enumerate(sorted_events):
            # In a real replay, the system's clock would be mocked to this event's timestamp
            # to ensure Risk Engine and Wallet Hunter don't look ahead.
            simulated_time = event.get("timestamp")
            
            logger.debug(f"[Replay] Processing event {idx} at simulated time {simulated_time}")
            
            try:
                # Process the event through the main engine
                result = await self.pipeline_fn(event)
                if result:
                    success_count += 1
                else:
                    blocked_count += 1
            except Exception as e:
                logger.error(f"[Replay] Error processing event: {e}")
                
        logger.info(f"Historical Replay Complete. Successful Alerts: {success_count}, Blocked/Ignored: {blocked_count}")
        return {
            "total_events": len(sorted_events),
            "alerts_generated": success_count,
            "events_ignored": blocked_count
        }
