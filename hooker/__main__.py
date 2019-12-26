import sys

from .api import EVENTS, load

for arg in sys.argv[1:]:
    load(arg)

for name in EVENTS._help:
    help, inspect = EVENTS._help[name]
    print("%s: %s - %s:%s" %
            (name, help, inspect.filename, inspect.lineno))
