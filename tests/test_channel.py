import pytest
from spilo.channel import Channel


def test_channel_instance():
    channel = Channel("test_channel")
    isinstance(channel.clients, set)
    isinstance(channel.dict_clients, dict)


def test_adding_new_client_in_channel(client):
    channel = Channel("test_channel")
    channel.add_client(client)

    assert len(channel.clients) == 1
    for client_1 in channel.clients:
        assert client_1 is client


@pytest.mark.asyncio
async def test_remove_client_from_channel(client):
    channel = Channel("test_channel")
    channel.add_client(client)

    await channel.remove_client(client)
    assert len(channel.clients) == 0
    assert channel.dict_clients.get(client.client_id) is None

