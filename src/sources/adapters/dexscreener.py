from typing import Any, Dict, List
from src.sources.base import BaseSourceAdapter
from src.models.events import NormalizedEvent
from src.utils.logger import logger
from datetime import datetime, timezone

class DexScreenerAdapter(BaseSourceAdapter):
    def __init__(self):
        super().__init__(name="dexscreener", base_url="https://api.dexscreener.com/latest/dex")
        
    async def fetch_data(self, search_query: str = "WIF") -> Any:
        try:
            response = await self.client.get(f"/search?q={search_query}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"DexScreener fetch failed: {e}")
            return {"pairs": []}

    def normalize_events(self, raw_data: Any) -> List[NormalizedEvent]:
        events = []
        pairs = raw_data.get('pairs', [])
        for pair in pairs[:5]: # Take top 5 results
            chain_id = pair.get('chainId', 'unknown')
            base_token = pair.get('baseToken', {}).get('symbol', 'UNKNOWN')
            pair_address = pair.get('pairAddress')
            
            events.append(
                NormalizedEvent(
                    event_type="dex_pair_snapshot",
                    chain=chain_id,
                    asset=base_token,
                    source=self.name,
                    raw_reference=f"dx_{pair_address}_{int(datetime.now(timezone.utc).timestamp())}",
                    metadata={
                        "priceUsd": pair.get('priceUsd'),
                        "volume24h": pair.get('volume', {}).get('h24'),
                        "liquidityUsd": pair.get('liquidity', {}).get('usd')
                    }
                )
            )
        return events
