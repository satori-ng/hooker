Plugin Creators
===============

So you found a project that uses hooker! Yey! But it's missing that
XYZ feature. Nay...

Let's see how you can extend this program via hooker plugins!

Event discovery
---------------

First of all you have to find the events that the developer of your
project provides. If the author does not give any info about the events
or they are outdated, ``python -m hooker <script>`` can help. It doesn't
work too well (due to various reasons that I probably can't fix),
but it's a good start. If the developer does not give any help even
with ``python -m hooker``, break his balls to add some. Or you do that
and do a Merge Request. It's VERY easy, :doc:`check it out <project_authors>`.
It's even written on the first paragraph! Anyway...

Test it in this project's :doc:`crypter <example>` example:

.. code:: sh

   hooker/example/crypter $ python -m hooker crypter.py

   pre_open_in: Input file will open. Arguments: path<str>. Return: path<str> - /home/dzervas/Lab/satori/hooker/example/crypter/crypter.py:6
   pre_open_out: Output file will open. Arguments: path<str>. Return: path<str> - /home/dzervas/Lab/satori/hooker/example/crypter/crypter.py:7
   encrypt: Encrypt data. Arguments: data<bytearray>. Return: data<str> - /home/dzervas/Lab/satori/hooker/example/crypter/crypter.py:8
   decrypt: Decrypt data. Arguments: data<bytearray>. Return: data<str> - /home/dzervas/Lab/satori/hooker/example/crypter/crypter.py:9

The first column is the event name (that's what you've been searching!),
second is what that event is all about and the last is the file and line number
that the event is declared (useful when you want to read the code around it).

So, by now you should have the event that you want to hook on, in order to
implement the missing functionality.

Let's code!

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
       print("I'll be called when crawler starts, but after simple_hook is run!")
       return "world"

If no dependency is used, hook calling is determined by the order that
the module was imported (that could change, use dependencies if your
code can't run before another plugin is run).

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

.. error::
   The above code does NOT run, as it hooks 2 events and has 2
   dependencies. The dependencies are applicable to both events

That means that both ``simple_hook`` and ``simple_hook_with_dependency``
must hook both ``on_start`` and ``with_open``, which is not the case. Why?

When ``on_start`` is fired, ``simple_hook`` is run, then
``simple_hook_with_dependency`` is run and then ``baz``.
``baz`` runs last because it depends on the other 2.

When ``with_open`` runs, ``simple_hook`` and ``simple_hook_with_dependency``
will **NOT** run, as they have declared that they hook only
the ``on_start`` event!

This is an example of missing dependency!

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
       print("But I'll be called on with_open too - probably alone")
       return "asdf!"

Using your plugin
-----------------

By now you should have at least SOME hook that awaits patiently for an event.
You can call that a plugin! But how do you call (= use) it?

You can inject your code by adding your script to ``HOOKER_SCRIPTS``.
Either as module path or as regular filepath:

``HOOKER_SCRIPTS=plugins.simple_hook:plugins.simple_hook_with_dependency``
is exactly the same with
``HOOKER_SCRIPTS=plugins/simple_hook.py:plugins/simple_hook_with_dependency.py``

On the other hand, regular python's ``import`` will work as well, but it
will not give you the flexibility to interchange modules on each run,
as you will have to ``import`` your plugin inside the project.

This is useful for projects that rely solely on plugins.

.. _OrderedDict: https://docs.python.org/3/library/collections.html#collections.OrderedDict
