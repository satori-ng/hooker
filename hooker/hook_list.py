"""The HookList class"""
import logging
import inspect
from collections import Iterable


logger = logging.getLogger(__name__)


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

        for func in self:
            # Skip extension if it doens't accept the arguments passed
            try:
                # Using deprecated getcallargs to be python2 compatible
                inspect.getcallargs(func, *args, **kwargs)
            except TypeError:
                logger.warning("Skipping %s" % func.__name__)
                continue
            func(*args, **kwargs)

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
