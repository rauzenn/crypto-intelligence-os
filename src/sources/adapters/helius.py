from typing import Any, Dict, List
from src.sources.base import BaseSourceAdapter
from src.models.events import NormalizedEvent
from src.utils.logger import logger
from datetime import datetime, timezone
import os

class HeliusAdapter(BaseSourceAdapter):
    def __init__(self):
        # We expect HELIUS_API_KEY to be set
        api_key = os.getenv("HELIUS_API_KEY", "")
        super().__init__(name="helius", base_url=f"https://api.helius.xyz/v0")
        self.api_key = api_key
        
    async def fetch_data(self, address: str = "") -> Any:
        if not self.api_key:
            logger.warning("HELIUS_API_KEY not set. Skipping fetch.")
            return []
            
        try:
            # Example: fetch recent transactions for an address
            # In a real real-time feed, this would be a websocket connection
            response = await self.client.get(f"/addresses/{address}/transactions?api-key={self.api_key}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Helius fetch failed: {e}")
            return []

    def normalize_events(self, raw_data: Any) -> List[NormalizedEvent]:
        events = []
        for tx in raw_data:
            events.append(
                NormalizedEvent(
                    event_type="onchain_transaction",
                    chain="solana",
                    wallet=tx.get("feePayer"),
                    source=self.name,
                    raw_reference=tx.get("signature", ""),
                    metadata={
                        "type": tx.get("type"),
                        "source": tx.get("source"),
                        "timestamp": tx.get("timestamp")
                    }
                )
            )
        return events
