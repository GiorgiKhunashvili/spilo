import asyncio
from typing import Set, Dict, Any

from .base_client import BaseClient
from .base_pubsub import BasePubSub


class Channel:
    """
    Class for handling clients adding new clients, removing clients in one specific channel.
    :param channel_name: The channel name where clients|client will be subscribed.
    clients will send and receive messages through channel_name.
    """

    _channel_cache = {}

    def __init__(self, channel_name: str, pubsub_manager: BasePubSub):
        self.channel_name = channel_name
        self.clients: Set[BaseClient] = set()
        self.dict_clients: Dict[Any, BaseClient] = {}
        self.pubsub_manager: BasePubSub = pubsub_manager
        self.receiver_task: asyncio.Task =asyncio.create_task(self.receiver())
    
    def __len__(self):
        """
        returns active clients count.
        """
        return len(self.clients)

    def __getitem__(self, channel_name: str):
        """
        returns channel class if one exists.
        """
        return self._channel_cache[channel_name]

    @classmethod
    def get(cls, channel_name: str, pubsub_manager: BasePubSub) -> "Channel":
        """
        Class method for getting channel class if channel class does not exist
        method will create new one and will return from function.
        """
        if channel_name in cls._channel_cache:
            return cls._channel_cache[channel_name]
        channel = cls(channel_name, pubsub_manager)
        cls._channel_cache[channel_name] = channel
        return channel

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

        await self._cleanup()

    async def _cleanup(self):
        """
        Method for canceling pubsub backend listener and
        removing channel instance from channel_cache
        """
        if len(self.clients) == 0:
            self.receiver_task.cancel()
            del self.__class__[self.channel_name]
            await self.pubsub_manager.unsubscribe(self.channel_name)

    async def receiver(self):
        """
        Method for listening pubsub backend channel
        and sending messeges to channel clients.
        """
        async for raw in self.pubsub_manager.listen(self.channel_name):
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
        """
        Method for publishing messages to the specific channel.
        """
        await self.pubsub_manager.publish(self.channel_name, data)
