from typing import Set, Dict

from .base_client import BaseClient


class Channel:
    """
    Class for handling clients adding new clients, removing clients in one specific channel.
    :param channel_name: The channel name where clients|client will be subscribed.
    clients will send and receive messages through channel_name
    """
    def __init__(self, channel_name: str):
        self.channel_name = channel_name
        self.clients: Set = set()
        self.dict_clients: Dict = {}

    def add_client(self, client: BaseClient) -> None:
        """
        Method for adding ws clients to channel.
        """
        self.clients.add(client)
        self.dict_clients[client.client_id] = client

    async def remove_client(self, client: BaseClient):
        """
        Method for removing client from channel.
        """
        if client in self.clients:
            await client.close()
            self.clients.remove(client)
            self.dict_clients.pop(client.client_id, None)

