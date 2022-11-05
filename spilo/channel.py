from typing import Set, Dict, Type

from .client import BaseClient


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

    def add_client(self, client: Type[BaseClient]) -> None:
        self.clients.add(client)
        self.dict_clients[client.client_id] = client
