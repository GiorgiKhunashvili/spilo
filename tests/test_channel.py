import pytest
from spilo.channel import Channel
from spilo.client import BaseClient


class Client(BaseClient):

    async def send(self, data):
        pass

    async def close(self):
        pass


def test_channel_instance():
    channel = Channel("test_channel")
    isinstance(channel.clients, set)
    isinstance(channel.dict_clients, dict)


def test_adding_new_client_in_channel():
    client_1 = Client()
    channel = Channel("test_channel")
    channel.add_client(client_1)

    assert len(channel.clients) == 1
    for client in channel.clients:
        assert client is client_1


@pytest.mark.asyncio
async def test_remove_client_from_channel():
    client = Client()
    channel = Channel("test_channel")
    channel.add_client(client)

    await channel.remove_client(client)
    assert len(channel.clients) == 0
    assert channel.dict_clients.get(client.client_id) is None

