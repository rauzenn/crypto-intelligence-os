from typing import Any, Dict, List
from src.sources.base import BaseSourceAdapter
from src.models.events import NormalizedEvent
from src.utils.logger import logger
from datetime import datetime, timezone

class DefiLlamaAdapter(BaseSourceAdapter):
    def __init__(self):
        super().__init__(name="defillama", base_url="https://api.llama.fi")
        
    async def fetch_data(self) -> Any:
        try:
            # Fetch top chains TVL
            response = await self.client.get("/v2/chains")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"DeFiLlama fetch failed: {e}")
            return []

    def normalize_events(self, raw_data: Any) -> List[NormalizedEvent]:
        events = []
        # Process top 10 chains
        for chain_data in raw_data[:10]:
            chain_name = chain_data.get('name', 'Unknown')
            tvl = chain_data.get('tvl', 0)
            events.append(
                NormalizedEvent(
                    event_type="chain_metrics_snapshot",
                    chain=chain_name.lower(),
                    source=self.name,
                    raw_reference=f"dl_chain_{chain_name.lower()}_{int(datetime.now(timezone.utc).timestamp())}",
                    metadata={"tvl": tvl}
                )
            )
        return events
