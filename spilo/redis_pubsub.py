import json

import aioredis
from aioredis import Redis
from aioredis.clinet import PubSub

from .pubsub import PubSub


class RedisPubSub(PubSub):

    def __init__(self, channel_name: str, url="redis://localhost:6379/0", redis_options=None):
        self.channel_name: str = channel_name
        self.redis_url = url
        self.redis_options = redis_options
        self.redis: None | Redis = None
        self.pubsub: None | PubSub = None

    def connect(self):
        self.redis = aioredis.Redis.from_url(self.redis_url, self.redis_options)
        self.pubsub = self.redis.pubsub(ignore_subscribe_messages=True)

    async def publish(self, data):
        return await self.redis.publish(
                self.channel_name, json.dumps(data)
                )
    
    async def listen(self):
        await self.pubsub.subscribe(self.channel_name)
        async for message in self.pubsub.listen():
            print(message)
            yield message
        await self.pubsub.unsubscribe(self.channel_name)
        
