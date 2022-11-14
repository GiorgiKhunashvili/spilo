import pytest

from spilo.channel import Channel


def test_adding_new_client_in_channel(client, channel):
    assert len(channel) == 0
    channel.add_client(client)

    assert len(channel) == 1
    assert channel[client.client_id] is client


@pytest.mark.asyncio
async def test_remove_client_from_channel(client, channel):
    channel.add_client(client)

    await channel.remove_client(client)
    assert len(channel) == 0
    assert channel[client.client_id] is None

