import importlib
import sys

from .api import EVENTS

for arg in sys.argv[1:]:
    importarg = arg.replace("/", ".").replace("\\", ".")
    if importarg[-3:] == ".py":
        importarg = importarg[:-3]

    try:
        importlib.import_module(importarg)
    except (ModuleNotFoundError, TypeError):
        exec(open(arg).read())

for name in EVENTS._help:
    help, inspect = EVENTS._help[name]
    print(f"{name}: {help} - {inspect.filename}:{inspect.lineno}")
