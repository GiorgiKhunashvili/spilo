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

