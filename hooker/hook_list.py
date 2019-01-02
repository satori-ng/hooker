"""The HookList class"""
import importlib
import inspect
import os
from collections import Iterable, OrderedDict

from .logger import logger
import hooker


class HookException(Exception):
    """A hook threw up!"""
    pass


class HOrderedDict(OrderedDict):
    @property
    def last(self):
        key = next(reversed(self))
        return (key, self[key])


class HookList(list):
    """Profesional grade list of hooks. Manages dependcy checking n' shit"""
    _run = False

    def __init__(self, *args, is_waterfall=False, **kwargs):
        self._later = []
        self.is_waterfall = is_waterfall
        super(HookList, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        """Fire the hooks!
        It passes all args and kwargs to each hook that hooks this event

        Raises:
            :class:HookException

        Please do **not** use an arg/kwarg named `retvals`, it is reserved
        for the return values of previously executed hooks in current event,
        passed in each hook function, if it exists in its signature.
        """

        # Check for first run in order to load scripts from environment variable
        if not self._run:
            self._run = True
            for script in os.getenv("HOOKER_SCRIPTS","").split(":"):
                if script: # Check for empty string
                    hooker.load(script)

        # If _later still has requirements to be satisfied, they are not found...
        if self._later:
            raise HookException(
                "Dependencies not met for: %s" %
                ", ".join([x.__name__ + ":" + x.__module__
                           for x in self._later])
            )

        if self.is_waterfall:
            for func in self:
                args = func(*args)
                # if not isinstance(args, Iterable) or isinstance(args, str):
                args = (args,)
            return args

        # Prepare the retvals, which contains the return values of all previous
        # hooks for THIS event
        retval = HOrderedDict()
        if not kwargs:
            kwargs = {}

        # Now call the hooks
        for func in self:
            position = None
            signature = inspect.getargspec(func)

            # Search the position of the positional argument "retvals"
            if "retvals" in kwargs.keys():
                logger.warning("WTF man? Don't use 'retvals' argument, I got dibs on it (read the wiki fucker)")
            else:
                try:
                    position = signature.args.index("retvals")
                except ValueError:
                    pass

            nargs = list(args)
            if position:
                # Put return values in the found position
                nargs.insert(position, retval)

            # Skip extension if it doens't accept the arguments passed
            try:
                # Using deprecated getcallargs to be python2 compatible
                inspect.getcallargs(func, *nargs, **kwargs)
            except TypeError:
                logger.warning("Skipping %s due to limited arguments" % func.__name__)
                continue

            retval[func] = func(*nargs, **kwargs)

        return retval

    def isloaded(self, name):
        """Checks if given hook module has been loaded

        Args:
            name (str): The name of the module to check

        Returns:
            bool.  The return code::

                True -- Loaded
                False -- Not Loaded
        """
        if name is None:
            return True

        if isinstance(name, str):
            return (name in [x.__module__ for x in self])

        if isinstance(name, Iterable):
            return set(name).issubset([x.__module__ for x in self])

        return False

    def hook(self, function, dependencies=None):
        """Tries to load a hook

        Args:
            function (func): Function that will be called when the event is called

        Kwargs:
            dependencies (str): String or Iterable with modules whose hooks should be called before this one

        Raises:
            :class:TypeError

        Note that the dependencies are module-wide, that means that if
        `parent.foo` and `parent.bar` are both subscribed to `example` event
        and `child` enumerates `parent` as dependcy, **both** `foo` and `bar`
        must be called in order for the dependcy to get resolved.
        """
        if not isinstance(dependencies, (Iterable, type(None), str)):
            raise TypeError("Invalid list of dependencies provided!")

        # Tag the function with its dependencies
        if not hasattr(function, "__deps__"):
            function.__deps__ = dependencies

        # If a module is loaded before all its dependencies are loaded, put
        # it in _later list and don't load yet
        if self.isloaded(function.__deps__):
            self.append(function)
        else:
            self._later.append(function)

        # After each module load, retry to resolve dependencies
        for ext in self._later:
            if self.isloaded(ext.__deps__):
                self._later.remove(ext)
                self.hook(ext)
