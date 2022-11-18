import json

import redis

from .base_pubsub import BasePubSub


class SyncRedisPubSub(BasePubSub):
    """
    Class for handling synchronous redis pubsub
    this class is write only which means you can only publish messages
    this class does not provides api for listening incoming messages yet.
    """

    def __init__(self, url="redis://localhost:6379/0",
                 connected_redis_inst: redis.Redis = None, redis_options=None):
        self.url = url
        self.redis_options = redis_options or {}
        self.redis: redis.Redis | None = connected_redis_inst

    def connect(self):
        self.redis = redis.Redis.from_url(self.url, **self.redis_options)

    def publish(self, channel_name: str, data):
        self.redis.publish(channel_name, json.dumps(data))
