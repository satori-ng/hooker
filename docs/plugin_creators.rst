Plugin Creators
===============

Event discovery
---------------

First of all you have to find the events that the developer of your
project provides. If the author does not give any info about the events
or they are outdated ``python -m hooker <script>`` can help. It doesn't
work too well, but it's a good start. If the developer does not give any
help even with ``python -m hooker``, break his balls to add some.

You can inject your code by adding your script too ``HOOKER_SCRIPTS``.
Either as module path or as regular filepath:

``HOOKER_SCRIPTS=plugins.simple_hook:plugins.simple_hook_with_dependency``
is exactly the same with
``HOOKER_SCRIPTS=plugins/simple_hook.py:plugins/simple_hook_with_dependency.py``

On the other hand, regular python's ``import`` will work as well, but it
will not give you the flexibility to interchange modules on each run.

Hook declaration
----------------

The simple one
^^^^^^^^^^^^^^

This is the simplest hook declaration.

What you need to keep in mind is that you need to know how many
arguments your hook expects.

``simple_hook.py``

.. code:: python

   import hooker

   @hooker.hook("on_start")
   def foo(argument_1):
       print("I'll be called when crawler starts!")
       return "hello"

The dependent one
^^^^^^^^^^^^^^^^^

This on the other hand utilizes dependencies, ``bar`` function will be
called AFTER ``foo`` function! This will happen because hooker waits to
find a module with ``__name__`` equal to ``simple_hook`` that hooks
``on_start`` at least once.

So after ALL ``on_start`` hooks are run by ``simple_hook``, ``bar``
function will run.

``simple_hook_with_dependency.py``

.. code:: python

   import hooker

   @hooker.hook("on_start", "simple_hook")
   def bar(argument_1):
       print("I'll be called when crawler starts, but after simple_hook is run")
       return "world"

If no dependency is used, hook calling is determined by the order that
the module was imported.

The one that uses previous hooks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This hook uses the magic argument ``__retvals__``. This argument contains
all the return values of previously executed hooks in an `OrderedDict`_:
``{<function_pointer>: <return value>}``

It also uses a list of dependencies. If you want to hook multiple
events, you can use a list of event names as well.

``__retvals___with_multi_deps.py``

.. code:: python

   import hooker

   # Won't run! See note below!
   @hooker.hook(["on_start", "with_open"], ["simple_hook", "simple_hook_with_dependency"])
   def baz(argument_1, __retvals__):
       print(__retvals__)
       print("I will throw HookException :(")
       return "asdf!"

NOTE: The above code does NOT run, as it hooks 2 events and has 2
dependencies. The dependencies are applicable to both events

That means that both ``simple_hook`` and ``simple_hook_with_dependency``
must hook both ``on_start`` and ``with_open``, which is not the case.

To work around that, you can do the following:

``__retvals___with_multi_deps.py``

.. code:: python

   import hooker

   # This will run happily
   @hooker.hook("on_start", ["simple_hook", "simple_hook_with_dependency"])
   @hooker.hook("with_open")
   def baz(argument_1, __retvals__):
       print(__retvals__)
       print("I'll be called after simple_hook and simple_hook_with_dependency on on_start")
       print("But I'll be called on with_open too!")
       return "asdf!"

.. _OrderedDict: https://docs.python.org/3/library/collections.html#collections.OrderedDict
