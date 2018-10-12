import importlib
import sys

from .api import EVENTS

for arg in sys.argv[1:]:
    try:
        importlib.import_module(arg)
    except ModuleNotFoundError:
        exec(open(arg).read())

for name in EVENTS._help:
    help, inspect = EVENTS._help[name]
    print(f"{name}: {help} - {inspect.filename}:{inspect.lineno}")
