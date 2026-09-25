from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod
import httpx
from src.utils.logger import logger

class BaseSourceAdapter(ABC):
    def __init__(self, name: str, base_url: str):
        self.name = name
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url, timeout=10.0)
    
    async def close(self):
        await self.client.aclose()

    @abstractmethod
    async def fetch_data(self, **kwargs) -> Any:
        pass
        
    @abstractmethod
    def normalize_events(self, raw_data: Any) -> List[Dict[str, Any]]:
        pass
