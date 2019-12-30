import sys

from .api import EVENTS, WATERFALL, load

for arg in sys.argv[1:]:
    load(arg)

help_dicts = EVENTS._help
help_dicts.update(WATERFALL._help)

for name in help_dicts:
    help_string, inspect = help_dicts[name]
    print("%s: %s - %s:%s" %
          (name, help_string, inspect.filename, inspect.lineno))
