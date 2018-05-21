# Arcane Hooker

I'm a hooker from Silvermoon City. Let me show you the Arcane way to Python

NOTE: Use me, use me haaaard...

---

This is my attempt to reinvent the hooking wheel.
I try to keep it simple for both providers and consumers.

The whole idea is that there are events, created by either the guts of the app
or an plugin itself on runtime.
After that, the required plugins that actually implemnt hooks on the events
should be imported. Example:

`main.py`
```python
import hooker
hooker.EVENTS.append(["on_start", "with_open"])

import foo
import test
import anothertest

hooker.EVENTS["on_start"]()
hooker.EVENTS["on_start"]("/tmp/path", 1234)
```

`foo.py`
```python
@hook("on_start")
def bar():
	print("I'll be called when crawler starts!")
```

`test.py`
```python
@hook("on_start", "foo")
def foo():
	print("I'll be called when crawler starts, but after `foo` hooks!")
```

`anothertest.py`
```python
@hook("with_open", "test")
def foo(path, fd):
	print("This will not work! Dependencies are per-event!")
	print("`test` module should have a 'with_open' hook as well!")
```
