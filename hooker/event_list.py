try:
    from collections.abc import Iterable
except ImportError:
    # Python 2
    from collections import Iterable

from inspect import getframeinfo, stack

from .logger import logger
from .hook_list import HookList


class EventList():
    """A list that holds all the events, each of which hold all hooks"""
    _events = {}
    _help = {}

    def __init__(self, is_waterfall=False):
        self.is_waterfall = is_waterfall

    def append(self, event, help=""):
        """Creates a new event. `event` may be iterable or string

        Args:
            event (str): Name of event to declare

        Kwrgs:
            help (str): Help string for the event

        Raises:
            TypeError

        **Please** describe the event and its calling arguments in the help
        string.
        """
        if isinstance(event, str):
            self._events[event] = HookList(is_waterfall=self.is_waterfall)
            self._help[event] = (help, getframeinfo(stack()[1][0]))

            if not help:
                logger.debug("Great, don't say anything about your hooks and \
                wait for plugin creators to figure it out.")
        elif isinstance(event, Iterable):
            # Depricated. It does not give the ability to give help string
            # TODO: Remove this
            for name in event:
                self.append(name)
        else:
            raise TypeError("Invalid event name!")

    def hook(self, function, event, dependencies):
        """Tries to load the hook to the event

        Args:
            function (func): Function that will be called when the event is called

        Kwargs:
            dependencies (str): String or Iterable with modules whose hooks should be called before this one

        Raises:
            NameError

        Note that the dependencies are module-wide, that means that if
        `parent.foo` and `parent.bar` are both subscribed to `example` event
        and `child` enumerates `parent` as dependcy, **both** `foo` and `bar`
        must be called in order for the dependcy to get resolved.
        """
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
            logger.debug(
                "Invalid key provided '%s'. Valid options: %s. Ignoring!"
                % (event, ", ".join(self._events.keys()))
            )
            return

        return event_list.hook(function, dependencies)

    def __getitem__(self, name):
        return self._events[name]
