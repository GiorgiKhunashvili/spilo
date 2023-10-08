from typing import Callable, Dict

from .base_client import BaseClient


class EventRegistry:
    def __init__(self, event_key_name: str = "event_type"):
        self.event_key_name = event_key_name
        self.__events = {}

    def on(self, event_name: str = None):
        """
        function decorator for handling specific events
        """
        def decorator(func: Callable) -> Callable:
            if event_name:
                self.__events[event_name] = func
            else:
                self.__events[func.__name__] = func
            return func
        return decorator

    async def handle_event(self, data: Dict, client: BaseClient, channel):
        try:
            event_name = data[self.event_key_name]
            if event_handler := self.__events.get(event_name):
                await event_handler(data, client, channel)
            else:
                raise ValueError(f"Event with name ${event_name} is not registered. Please register event.")
        except KeyError:
            raise KeyError(f"Can not find event key name please specify correctly")
