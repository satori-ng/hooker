![](https://github.com/satori-ng/hooker/workflows/py2%20tests/badge.svg)
![](https://github.com/satori-ng/hooker/workflows/py3%20tests/badge.svg)

# Arcane Hooker

I'm a hooker from Silvermoon City. Let me show you the Arcane way to Python

---

Hooker is a hooking library that tries to simplify event firing and catching.
It gives the ability to plugin creators to create plugins for many different
parts, without having to break the logic in separate destinations, if it's not
needed. The main features include:
- Event declaration with help message support
- `Waterfall` events that pass their output as arguments to next hook
- Simple CLI tool to view all defined events of a project and its help messages
- Functions decorators to hook on events
- Dependency requirement for hooks (`a` hook has to be run before `b`)
- `HOOKER_SCRIPTS` environmental variable allows to load additional scripts (aka plugins)
- Wildcard hooks that are fired on all events
- When a hook accepts the `__retvals__` argument, the returned values of the previous
hooks (and the whole hook functions) will be passed into it as an [OrderedDict](https://docs.python.org/3/library/collections.html#collections.OrderedDict)
- Python 2 compatibility - I'll try to keep that for as long as I can

Terminology:
- `Project`: A project that uses Hooker
- `Plugin`: A piece of code that adds functionality to a `Project` using `hooks`
- `Event`: A name for something that `Plugins` can hook on. It is called on specific times
(that the `Project` author has programmed) so that `Plugins` can add functionality
- `Hook`: A function that the `Plugin` creator wrote and is declared as hook using
the `@hooker.hook` decorator. Contains at least one `Event` name (or none if its a wildcard
hook) and optionally `Dependencies`
- `Dependency`: A `Hook` can declare to be called after a plugin has run. `Dependency` can
include the name(s) of the python module(s) (**NOT** the function name) that include hooks
that need to be run before the `Hook`

For documentation check the [wiki](https://satori-ng.github.io/hooker/)

## Installation

`pip install -U hooker`

## Usage

To find defined hooks in a project use `python -m hooker <python file/module directory>`

Example:

`$ py -m hooker example/crypter/crypter.py`
```
pre_open_in: Input file will open. Arguments: path<str>. Return: path<str> - /home/dzervas/Lab/satori/hooker/example/crypter/crypter.py:6
pre_open_out: Output file will open. Arguments: path<str>. Return: path<str> - /home/dzervas/Lab/satori/hooker/example/crypter/crypter.py:7
encrypt: Encrypt data. Arguments: data<bytearray>. Return: data<str> - /home/dzervas/Lab/satori/hooker/example/crypter/crypter.py:8
decrypt: Decrypt data. Arguments: data<bytearray>. Return: data<str> - /home/dzervas/Lab/satori/hooker/example/crypter/crypter.py:9
```

As a Project Author to use hooker you have to declare an event and then fire it

Example:
```python
# project.py
import hooker

hooker.EVENTS.append("test", "Fired after Hello World is printed")

print("Hello World")
hooker.EVENTS["test"]()
```

As a Plugin Creator to extend a project using hooker, you have to create a function
using the `@hooker.hook` decorator and define the event you want to hook on:

Example:
```python
# my_plugin.py
import hooker

@hooker.hook("test")
def hello():
    print("Goodbye World")
``` 

Now to use the plugin, you either have to `import` it in the project, or execute the
project using the environment variable `HOOKER_SCRIPTS` as follows:

`$ HOOKER_SCRIPTS=my_plugin python project.py`
```
Hello World
Goodbye World
```

---

While the code is not a mess, I'm using a fair bit of python magic.
The target is to provide the simplest and most convenient API for
both project and plugin authors.

If you have a better way to do something, at least open an issue to
discuss it, I'm very interested!

Happy Hacking! :)
