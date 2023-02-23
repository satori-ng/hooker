from collections.abc import Iterable

from inspect import getframeinfo, stack
import fnmatch

from .logger import logger
from .hook_list import HookList


class EventList():

    _events = {}
    _help = {}

    def __init__(self, is_waterfall=False):
        """A list that holds all the events, each of which hold all hooks"""
        self.is_waterfall = is_waterfall

    def clear(self):
        self._events.clear()
        self._help.clear()

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

        if not isinstance(event, list):
            event = [event]

        for e in event:
            if not isinstance(e, str):
                raise TypeError("Events must be strings, '%s' given" % type(e))

            self._events[e] = HookList(e, is_waterfall=self.is_waterfall)
            self._help[e] = (help, getframeinfo(stack()[1][0]))

            if not help:
                logger.debug("It is advised to provide a 'help' parameter for the created events")

    def hook(self, function, event='*', dependencies=[]):
        """Tries to load the hook to the event

        Args:
            function (func): Function that will be called when the event is called
            event (str): Name or glob to match events to hook

        Kwargs:
            dependencies (str): String or Iterable with modules whose hooks should be called before this one

        Raises:
            NameError

        Note that the dependencies are module-wide, that means that if
        `parent.foo` and `parent.bar` are both subscribed to `example` event
        and `child` enumerates `parent` as dependcy, **both** `foo` and `bar`
        must be called in order for the dependcy to get resolved.
        """

        # Hooks all events (applying the glob)

        if not isinstance(event, list):
            event = [event]

        matching_events = []
        for e in event:
            if not e: continue
            m = fnmatch.filter(self._events.keys(), e)
            if len(m) == 0:
                logger.warning(
                    "Invalid key/glob provided '%s'. Valid Events: '%s'. Ignoring!"
                    % (event, ", ".join(self._events.keys()))
                )
            matching_events.extend(m)
            matching_events = sorted(matching_events)

        for e in matching_events:
            # Hook a simple event
            hook_list = self._events[e]
            hook_list.hook(function, dependencies)

    def __getitem__(self, name):
        return self._events[name]

    def __repr__(self):  # pragma: no cover
        return self._events.__repr__()

    def __len__(self):
        return self._events.__len__()