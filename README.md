# Arcane Hooker

I'm a hooker from Silvermoon City. Let me show you the Arcane way to Python

NOTE: Use me, use me haaaard...

---

This is my attempt to reinvent the hooking wheel.
I try to keep it simple for both providers and consumers.

The whole idea is that there are events, created by either the guts of the app
or a plugin itself on runtime.
After that, the required plugins that actually implemnt hooks on the events
should be imported.

## For Hook Users

### Hook discovery

First of all you have to find the hooks that the developer of your project provides.
If the author does not give any info about the hooks or they are outdated
`python -m hooker <script>` can help. It doesn't work too well, but it's a
good start. If the developer does not give any help even with `python -m hooker`,
break his balls to add some.

You can inject your code by adding your script too `HOOKER_SCRIPTS`. Either as
module path or as regular filepath:

`HOOKER_SCRIPTS=plugins.simple_hook:plugins.simple_hook_with_dependency`
is exactly the same with
`HOOKER_SCRIPTS=plugins/simple_hook.py:plugins/simple_hook_with_dependency.py`

### Hook decleration

This is the simplest hook decleration. You need to know how many arguments your
hook expects though.

`simple_hook.py`
```python
import hooker

@hooker.hook("on_start")
def bar(argument_1):
    print("I'll be called when crawler starts!")
    return "hello"
```

This on the other hand utilizes dependencies!

`simple_hook_with_dependency.py`
```python
import hooker

@hooker.hook("on_start", "simple_hook")
def bar(argument_1):
    print("I'll be called when crawler starts, but after simple_hook is run")
    return "world"
```

This hook uses the magic argument `retvals`. This argument contains all the
return values of previously executed hooks in an OrderedDict:
`{<function_pointer>: <return value>}`

`retvals_with_multi_deps.py`
```python
import hooker

@hooker.hook("on_start", ["simple_hook", "simple_hook_with_dependency"])
def bar(argument_1, retvals):
    print(retvals)
    print("I'll be called after simple_hook and simple_hook_with_dependency")
    return "asdf!"
```

## For Hook Creators

It's really easy to use the hooker. This is an example usage:

`main.py`
```python
import hooker
hooker.EVENTS.append("on_start", help="This will be called on start")
hooker.EVENTS.append("with_open", help="This will be called after the file is opened")

import simple_hook
import simple_hook_with_dependency
import retvals_with_multi_deps

results1 = hooker.EVENTS["on_start"]()
results2 = hooker.EVENTS["on_start"]("/tmp/path", 1234)
```

`EVENTS.append` declares the hook name with string as first argument and help string as second.
The help string will be shown when `python -m hooker` is invoked. PLEASE give some insight
on what the hook does and where it is fired, as well as what argument is the hook called with.

Then to fire the hook, just `EVENTS[<hook>](<arguments>)`.

As expected, the return value is an OrderedDict: `{<hook_function_pointer>: <return value>}`.
So you know exactly the order that the hooks where fired and you can get
info about the hook from the function pointer.

You don't have to import all the plugins, as the user can use the `HOOKER_SCRIPTS` environment variable.

# NOTE: Don't use `retvals` as argument when you're calling a hook. See `retvals_with_multi_deps.py`!!!

Happy Hacking! :)
