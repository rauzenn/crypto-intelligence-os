import redis.asyncio as redis
from src.config.settings import settings

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

async def push_event(queue_name: str, event_json: str):
    await redis_client.rpush(queue_name, event_json)

async def pop_event(queue_name: str):
    return await redis_client.lpop(queue_name)
