import importlib
import sys, os
import inspect

from .event_list import EventList
from .logger import logger

EVENTS = EventList()
WATERFALL = EventList(is_waterfall=True)

if "ModuleNotFoundError" not in globals():
    ModuleNotFoundError = NameError

if "FileNotFoundError" not in globals():
    FileNotFoundError = IOError


def reset():
    global EVENTS, WATERFALL
    EVENTS = EventList()
    WATERFALL = EventList(is_waterfall=True)


def hook(event='*', dependencies=None, event_list=EVENTS):
    """Hooking decorator. Just `@hook(event, dependencies)` on your function

    Kwargs:
        event (str): String or Iterable with events to hook
        dependencies (str): String or Iterable with module names whose hooks have
            to be called before this one for **this** event

    Wraps :func:`EventList.hook`
    """

    def wrapper(func):
        """I'm a simple wrapper that manages event hooking"""
        event_list.hook(func, event, dependencies)
        return func
    return wrapper

def load(path, overwrite=True):
    """Helper function that tries to load a filepath (or python module notation)
    as a python module and on failure `exec` it.

    Args:
        path (str): Path or module to load

    The function tries to import `example.module` when either `example.module`,
    `example/module` or `example/module.py` is given.
    """
    if path.startswith("http://") or path.startswith("https://"):
        import httpimport
        url, module = path.split("/", -1)
        with httpimport.remote_repo(url):
            __import__(module)
        return

        raise Exception("Loading plugins through HTTP/S is not implemented.")


    logger.info("Loading plugin at '%s'" % (path))

    importpath = path.replace("/", ".").replace("\\", ".")
    if importpath.endswith(".py"):  # Remove the file extension
        importpath = ".".join(importpath.split(".")[:-1])
        logger.info("Plugin module at '%s'" % (importpath))

    try:
        if overwrite and importpath in sys.modules:
            logger.info("Overwriting plugin '%s'!" % (importpath))
            importlib.reload(importpath)
        else:
            importlib.import_module(importpath)
    except (ModuleNotFoundError, ImportError, TypeError):
        logger.warning("Failed loading '%s' as module ('%s'). Trying execution as file..." % (path, importpath))

        try:
            with open(path) as f:
                exec(f.read())
        except FileNotFoundError:
            logger.error("Module or file '%s' was not found! Ignoring...", importpath)

def get_event_name():
    try:    # _getframe is faster but implementation specific
        return sys._getframe(2).f_locals['event_name']
    except:
        return inspect.stack()[2].frame.f_locals['event_name']
