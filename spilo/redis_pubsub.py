import json

import aioredis
from aioredis import Redis
from aioredis.client import PubSub

from .base_pubsub import BasePubSub


class RedisPubSub(BasePubSub):

    _singleton = None
    
    def __new__(cls, url="redis://localhost:6379/0", redis_options=None, *args, **kwargs):
        if not cls._singleton:
            cls._singleton = super(RedisPubSub, cls).__new__(cls, *args, **kwargs)
        return cls._singleton

    def __init__(self, url="redis://localhost:6379/0", redis_options=None, connected_redis_inst: Redis=None):
        self.redis_url = url
        self.redis_options = redis_options or {}
        self.redis: Redis | None = connected_redis_inst
        self.pubsub: PubSub | None = None

    def connect(self):
        """
        If connected_redis_inst is provided
        connect method will not make new connect
        to the database and will reuse provided redis instance.
        """
        if self.redis is None:
            self.redis = aioredis.Redis.from_url(
                    self.redis_url,
                    decode_responses=True,
                    **self.redis_options
                    )
        self.pubsub = self.redis.pubsub(ignore_subscribe_messages=True)

    async def publish(self, channel_name: str, data):
        return await self.redis.publish(
            channel_name, json.dumps(data)
        )

    async def listen(self, channel_name: str):
        await self.pubsub.subscribe(channel_name)
        async for message in self.pubsub.listen():
            yield message

    async def unsubscribe(self, channel_name):
        """
        Method for unsubscribe specific channel this
        prevents from getting unnecessary information.
        """
        await self.pubsub.unsubscribe(channel_name)
