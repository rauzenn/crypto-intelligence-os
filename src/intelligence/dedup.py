import redis.asyncio as redis
from src.config.settings import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

class AlertDeduplicator:
    def __init__(self, ttl_seconds: int = 3600 * 24): # 24 hours
        self.ttl = ttl_seconds
        
    async def is_duplicate(self, asset: str, chain: str, alert_type: str) -> bool:
        key = f"dedup:{alert_type}:{chain}:{asset}"
        exists = await redis_client.exists(key)
        if exists:
            return True
            
        await redis_client.set(key, "1", ex=self.ttl)
        return False
