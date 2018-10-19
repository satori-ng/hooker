"""The HookList class"""
import inspect
from collections import Iterable

from hooker.logger import logger


class HookException(Exception):
    """A hook threw up!"""
    pass


class HookList(list):
    """Profesional grade list of hooks. Manages dependcy checking n' shit"""

    def __init__(self, *args, **kwargs):
        # If an extension is loaded before all its dependencies are loaded, put
        # it in this list and try to load it after loading the next extension
        self._later = []
        super(HookList, self).__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        if self._later:
            raise HookException(
                "Dependencies not met for: %s" %
                ", ".join([x.__name__ + ":" + x.__module__
                           for x in self._later])
            )

        # Prepare the retvals, which contains the return values of all previous
        # hooks for THIS event
        retval = {}
        if not kwargs:
            kwargs = {}

        for func in self:
            signature = inspect.getargspec(func)
            # Search the position of the positional argument "retvals"
            if "retvals" in kwargs.keys():
                logger.warning("WTF man? Don't use 'retvals' argument, I got dibs on it (read the wiki fucker)")
                position = tuple()
            else:
                position = tuple(x for x in range(len(signature.args)) if signature.args[x] == "retvals")
            nargs = list(args)
            if position:
                # Put return values in the found position
                nargs.insert(position[0], retval)

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
        """Checks if given hook module has been loaded"""
        if name is None:
            return True

        if isinstance(name, str):
            return (name in [x.__module__ for x in self])

        if isinstance(name, Iterable):
            # return set(name).issubset(self)
            for n in name:
                if not self.isloaded(n):
                    return False
            return True

        return False

    def hook(self, function, dependencies=None):
        """Tries to load a hook"""
        if not isinstance(dependencies, (Iterable, type(None), str)):
            raise HookException("Invalid list of dependencies provided!")

        # Tag the function with its dependencies
        if not hasattr(function, "__deps__"):
            function.__deps__ = dependencies

        if self.isloaded(function.__deps__):
            self.append(function)
        else:
            self._later.append(function)

        for ext in self._later:
            if self.isloaded(ext.__deps__):
                self._later.remove(ext)
                self.hook(ext)
