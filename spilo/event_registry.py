from typing import Callable


class EventRegistry:
    def __init__(self, event_key_name: str = "event"):
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

    def handle_event(self, event_name: str):
        if event_handler := self.__events.get(event_name):
            event_handler()
        else:
            raise ValueError(f"Event with name ${event_name} is not registered. Please register event.")
