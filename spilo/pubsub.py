from abc import ABC, abstractmethod


class PubSub(ABC):
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
    async def publish(self, data):
        """
        Method for publishing messages.
        """


    @abstractmethod
    async def listen(self, data):
        """
        Method for listening incoming messages.
        """

