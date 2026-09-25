from typing import Any, Dict, List
from src.ingestion.base import BaseSourceAdapter
from src.normalization.events import NormalizedEvent
from src.utils.logger import logger
import asyncio
from datetime import datetime, timezone

class CoinGeckoAdapter(BaseSourceAdapter):
    def __init__(self):
        super().__init__(name="coingecko", base_url="https://api.coingecko.com/api/v3")
        
    async def fetch_data(self, coin_ids: List[str] = ["bitcoin", "ethereum", "solana"]) -> Any:
        try:
            ids_str = ",".join(coin_ids)
            response = await self.client.get(f"/simple/price?ids={ids_str}&vs_currencies=usd&include_24hr_vol=true&include_24hr_change=true")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"CoinGecko fetch failed: {e}")
            return {}

    def normalize_events(self, raw_data: Any) -> List[NormalizedEvent]:
        events = []
        from src.normalization.events import Provenance
        for asset, data in raw_data.items():
            events.append(
                NormalizedEvent(
                    event_type="market_snapshot",
                    chain="multiple",
                    asset=asset.upper(),
                    provenance=Provenance(
                        source_id=self.name,
                        source_type="market_data",
                        raw_reference=f"cg_{asset}_{int(datetime.now(timezone.utc).timestamp())}"
                    ),
                    metadata=data
                )
            )
        return events
