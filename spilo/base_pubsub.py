from abc import ABC, abstractmethod
from typing import AsyncIterable


class BasePubSub(ABC):
    """
    This is abstract base class defines interface
    which should be implemented by any child class.
    """

    @abstractmethod
    async def connect(self):
        """
        Method for connecting pub sub backend.
        """

    @abstractmethod
    async def publish(self, channel_name: str, data):
        """
        Method for publishing messages.
        """

    @abstractmethod
    async def listen(self, channel_name: str) -> AsyncIterable:
        """
        Method for listening incoming messages.
        """

