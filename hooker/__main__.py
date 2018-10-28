import sys

from .api import EVENTS, load

for arg in sys.argv[1:]:
    load(arg)

for name in EVENTS._help:
    help, inspect = EVENTS._help[name]
    print(f"{name}: {help} - {inspect.filename}:{inspect.lineno}")
