from collections import Iterable
from inspect import getframeinfo, stack

from hooker.logger import logger
from hooker.hook_list import HookList


class EventException(Exception):
    """An event threw up!"""
    pass


class EventList():
    """A list that holds all the events, each of which hold all hooks"""
    _events = {}
    _help = {}

    def append(self, event, help=""):
        """Creates a new event. `event` may be iterable or string"""
        if isinstance(event, str):
            self._events[event] = HookList()
            self._help[event] = (help, getframeinfo(stack()[1][0]))
        elif isinstance(event, Iterable):
            for name in event:
                self.append(name)
        else:
            raise EventException("De hell did you give me as an event name? O.o")

    def hook(self, function, event, dependencies):
        """Tries to load the hook to the event"""
        # Hooks all events (recursively)
        if event is None:
            for e in self._events.keys():
                self.hook(function, e, dependencies)
            return

        # Hook multiple, but specific events (recursively)
        if not isinstance(event, str) and isinstance(event, Iterable):
            for e in event:
                self.hook(function, e, dependencies)
            return

        # Hook a simple event
        event_list = self._events.get(event, None)
        if event_list is None:
            logger.warning(
                "Invalid key provided '%s'. Valid options: %s"
                % (event, ", ".join(self._events.keys()))
            )
            return

        return event_list.hook(function, dependencies)

    def __getitem__(self, name):
        """Get the HookList"""
        return self._events[name]
