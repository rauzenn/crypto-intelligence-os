from typing import Any, Dict, List
from src.ingestion.base import BaseSourceAdapter
from src.normalization.events import NormalizedEvent
from src.utils.logger import logger
from datetime import datetime, timezone

class NewsAdapter(BaseSourceAdapter):
    def __init__(self):
        # Using CryptoPanic public API as a generic news source
        super().__init__(name="cryptopanic", base_url="https://cryptopanic.com/api/v1")
        
    async def fetch_data(self) -> Any:
        try:
            # We would need an API key for CryptoPanic, but let's assume we have a free one or we mock
            # If no auth is provided, this might fail, so we catch it
            response = await self.client.get("/posts/?public=true")
            if response.status_code == 200:
                return response.json()
            return {"results": []}
        except Exception as e:
            logger.error(f"News fetch failed: {e}")
            return {"results": []}

    def normalize_events(self, raw_data: Any) -> List[NormalizedEvent]:
        events = []
        for post in raw_data.get("results", [])[:10]:
            events.append(
                NormalizedEvent(
                    event_type="news_article",
                    chain="multiple",
                    asset="various",
                    source=self.name,
                    raw_reference=str(post.get("id")),
                    metadata={
                        "title": post.get("title"),
                        "domain": post.get("domain"),
                        "url": post.get("url")
                    }
                )
            )
        return events
