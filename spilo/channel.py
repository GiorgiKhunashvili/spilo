from typing import Set, Dict, Any, Tuple

from .base_client import BaseClient
from .base_pubsub import BasePubSub


class Channel:
    """
    Class for handling clients adding new clients, removing clients in one specific channel.
    :param channel_name: The channel name where clients|client will be subscribed.
    clients will send and receive messages through channel_name.
    """

    channel_cache = {}

    def __init__(self, channel_name: str, pubsub_manager: BasePubSub):
        self.channel_name = channel_name
        self.clients: Set[BaseClient] = set()
        self.dict_clients: Dict[Any, BaseClient] = {}
        self.pubsub_manager = pubsub_manager

    @classmethod
    def get(cls, channel_name: str, pubsub_manager: BasePubSub) -> Tuple["Channel", bool]:
        """
        Class method for getting channel class if channel class does not exist
        method will create new one and will return from function.
        """
        if channel_name in cls.channel_cache:
            return cls.channel_cache[channel_name], True
        channel = cls(channel_name, pubsub_manager)
        cls.channel_cache[channel_name] = channel
        return channel, False

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

    async def receiver(self):
        async for raw in self.pubsub_manager.listen(self.channel_name):
            if raw:
                if raw["data"] == "STOP" and len(self.clients) == 0:
                    break
                if raw["channel"] != self.channel_name:
                    try:
                        await self.dict_clients[raw["channel"]].send(
                            raw["data"]
                        )
                    except KeyError:
                        # TODO LOG SOMETHING
                        pass
                else:
                    for client in self.clients:
                        await client.send(str(raw["data"]))

    async def publish(self, data):
        await self.pubsub_manager.publish(self.channel_name, data)
