from typing import Any, Dict, List
from src.sources.base import BaseSourceAdapter
from src.models.events import NormalizedEvent
from src.utils.logger import logger
import os

class AlchemyAdapter(BaseSourceAdapter):
    def __init__(self):
        api_key = os.getenv("ALCHEMY_API_KEY", "")
        # Defaults to eth-mainnet
        super().__init__(name="alchemy", base_url=f"https://eth-mainnet.g.alchemy.com/v2/{api_key}")
        self.api_key = api_key
        
    async def fetch_data(self, params: Dict[str, Any] = None) -> Any:
        if not self.api_key:
            logger.warning("ALCHEMY_API_KEY not set. Skipping fetch.")
            return {}
            
        try:
            # Example JSON-RPC call
            payload = {
                "id": 1,
                "jsonrpc": "2.0",
                "method": "eth_blockNumber",
                "params": []
            }
            response = await self.client.post("", json=payload)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Alchemy fetch failed: {e}")
            return {}

    def normalize_events(self, raw_data: Any) -> List[NormalizedEvent]:
        events = []
        if raw_data.get("result"):
            events.append(
                NormalizedEvent(
                    event_type="evm_block",
                    chain="ethereum",
                    source=self.name,
                    raw_reference=raw_data.get("result"),
                    metadata={"block_number_hex": raw_data.get("result")}
                )
            )
        return events
