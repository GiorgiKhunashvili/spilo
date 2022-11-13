import asyncio
import pytest
import pytest_asyncio

from spilo.base_client import BaseClient
from spilo.channel import Channel
from spilo.redis_pubsub import RedisPubSub


class Client(BaseClient):

    async def send(self, data):
        pass

    async def close(self):
        pass


@pytest.fixture
def client():
    c = Client()
    yield c


@pytest_asyncio.fixture
async def channel():
    redis_pubsub = RedisPubSub().connect()
    channel = Channel.get("test_channel", redis_pubsub)
    yield channel

