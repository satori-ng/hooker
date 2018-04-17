from hooker.event_list import EventList

EVENTS = EventList()


def hook(event=None, dependencies=None):
    """Hooking decorator. Just `@hook(event, dependencies) on your function`"""

    def wrapper(func):
        """I'm a simple wrapper that manages event hooking"""
        func.__deps__ = dependencies
        EVENTS.hook(func, event, dependencies)
        return func
    return wrapper
