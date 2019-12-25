import importlib

from .event_list import EventList

EVENTS = EventList()
WATERFALL = EventList(is_waterfall=True)

if "ModuleNotFoundError" not in globals():
    ModuleNotFoundError = NameError


def hook(event=None, dependencies=None):
    """Hooking decorator. Just `@hook(event, dependencies)` on your function

    Kwargs:
        event (str): String or Iterable with events to hook
        dependencies (str): String or Iterable with modules whose hooks have
        to be called before this one for **this** event

    Wraps :func:`EventList.hook`
    """

    def wrapper(func):
        """I'm a simple wrapper that manages event hooking"""
        EVENTS.hook(func, event, dependencies)
        return func
    return wrapper

def load(path):
    """Helper function that tries to load a filepath (or python module notation)
    as a python module and on failure `exec` it.

    Args:
        path (str): Path or module to load

    The function tries to import `example.module` when either `example.module`,
    `example/module` or `example/module.py` is given.
    """

    importpath = path.replace("/", ".").replace("\\", ".")
    if importpath[-3:] == ".py":
        importpath = importpath[:-3]

    try:
        importlib.import_module(importpath)
    except (ModuleNotFoundError, TypeError):
        exec(open(path).read())
