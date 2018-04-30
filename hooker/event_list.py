from collections import Iterable

from hooker.logger import logger
from hooker.hook_list import HookList


class EventException(Exception):
    """An event threw up!"""
    pass


class EventList():
    """A list that holds all the events, each of which hold all hooks"""
    _events = {}

    def append(self, event):
        """Creates a new event. `event` may be iterable or string"""
        if isinstance(event, str):
            self._events[event] = HookList()
            return

        if isinstance(event, Iterable):
            for name in event:
                self.append(name)
            return

        raise EventException("De hell did you give me as an event name? O.o")

    def hook(self, function, event, dependencies):
        """Tries to load the hook to the event"""
        if event is None:
            for e in self._events.keys():
                self.hook(function, e, dependencies)
            return

        if not isinstance(event, str) and isinstance(event, Iterable):
            for e in event:
                self.hook(function, e, dependencies)
            return

        event_list = self._events.get(event, None)
        if event_list is None:
            logger.warning(
                "Invalid key provided '%s'. Valid options: %s"
                % (event, ", ".join(self._events.keys()))
            )
            return

        event_list.hook(function, dependencies)

    def __getitem__(self, name):
        """Get the HookList"""
        return self._events[name]
