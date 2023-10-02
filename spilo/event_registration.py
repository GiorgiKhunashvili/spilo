

PLUGINS = dict()


def register(event_name):
    """Register a function as a plug-in with a specific event name"""
    def decorator(func):
        PLUGINS[event_name] = func
        return func
    return decorator


@register("say_hello")
def say_hello(name):
    return f"Hello {name}"


@register("say_goodbye")
def say_goodbye(name):
    return f"Goodbye {name}"


print(PLUGINS)


class EventHandling:
    def __int__(self):
        self.__events = {}

