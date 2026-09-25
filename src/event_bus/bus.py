import asyncio
import json
from typing import Callable, Any, Dict, Awaitable
from src.utils.logger import logger
import redis.asyncio as redis
from src.config.settings import settings

class EventBus:
    """
    C. EVENT BUS / STREAM LAYER
    Loosely couples all JARVIS intelligence layers via Redis Pub/Sub.
    """
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL, decode_responses=True)
        self.pubsub = self.redis.pubsub()
        self.callbacks: Dict[str, Callable[[Dict[str, Any]], Awaitable[None]]] = {}
        self._listener_task = None

    async def publish(self, topic: str, message: Dict[str, Any]) -> None:
        """Publish a message to a specific topic."""
        try:
            payload = json.dumps(message)
            await self.redis.publish(topic, payload)
            logger.debug(f"[EventBus] Published to {topic}: {message.get('event_id', 'unknown')}")
        except Exception as e:
            logger.error(f"[EventBus] Publish error on {topic}: {e}")

    async def subscribe(self, topic: str, callback: Callable[[Dict[str, Any]], Awaitable[None]]) -> None:
        """Subscribe to a topic with an async callback."""
        self.callbacks[topic] = callback
        await self.pubsub.subscribe(topic)
        logger.info(f"[EventBus] Subscribed to {topic}")

        if self._listener_task is None:
            self._listener_task = asyncio.create_task(self._listen())

    async def _listen(self):
        """Background listener for incoming pubsub messages."""
        logger.info("[EventBus] Listener started.")
        try:
            async for message in self.pubsub.listen():
                if message["type"] == "message":
                    topic = message["channel"]
                    data = json.loads(message["data"])
                    callback = self.callbacks.get(topic)
                    if callback:
                        asyncio.create_task(self._safe_execute(callback, data, topic))
        except Exception as e:
            logger.error(f"[EventBus] Listener error: {e}")

    async def _safe_execute(self, callback, data, topic):
        try:
            await callback(data)
        except Exception as e:
            logger.error(f"[EventBus] Error in callback for topic {topic}: {e}")

    async def close(self):
        if self._listener_task:
            self._listener_task.cancel()
        await self.pubsub.close()
        await self.redis.close()

# Global Event Bus instance
bus = EventBus()
