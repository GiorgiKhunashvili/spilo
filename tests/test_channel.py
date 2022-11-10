import pytest

from spilo.channel import Channel


def test_channel_instance(channel):
    isinstance(channel.clients, set)
    isinstance(channel.dict_clients, dict)


def test_adding_new_client_in_channel(client, channel):
    assert len(channel) == 0
    channel.add_client(client)

    assert len(channel) == 1
    for client_1 in channel.clients:
        assert client_1 is client


@pytest.mark.asyncio
async def test_remove_client_from_channel(client, channel):
    channel.add_client(client)

    await channel.remove_client(client)
    assert len(channel.clients) == 0
    assert channel.dict_clients.get(client.client_id) is None


@pytest.mark.asyncio
async def test_getting_channel_with_brackets(channel):
    exc_channel = channel["test_channel"]
    assert exc_channel is channel

