Project Authors
===============

First you got to declare your event like that:

``my_project.py``

.. code:: python

   import hooker
   hooker.EVENTS.append("on_start", help="This will be called on start")
   hooker.EVENTS.append("with_open", help="This will be called after the file is opened")

.. note::
   **Please** include the ``help`` part, as it gives the help info for
   ``python -m hooker``. It will help your hook creators a lot. Describe
   **when** the event takes place and what **arguments** you pass to the
   hooks.

And then you can fire it whenever you like, like this:

.. code:: python

   # later in my_project.py
   results1 = hooker.EVENTS["on_start"]()
   results2 = hooker.EVENTS["with_open"]("/tmp/path", 1234)

.. attention::
   Don't use ``__retvals__`` as argument when you're calling a hook.
   It is a reserved magic argument that a hook can include in its
   signature to get the results of its ancestors. For more, read
   :doc:`here <plugin_creators>`

The return value is an `OrderedDict`_:
``{<hook_function_pointer>: <return value>}``, so that you know exactly
the order that the hooks where fired and you can get info about the hook
from the function pointer. The exact hook info should not be of real
interest to you, but with python's ``inspect`` module, you can see a lot
of stuff about the extension.

Now the problem is that you don't (and don't want to) know which plugins
will be loaded on runtime, so ``import``ing them is out of the game.
Thank god the user can use the ``HOOKER_SCRIPTS`` environment variable.

The user can call your program as follows, without you even worrying:

.. code:: sh

   $ HOOKER_SCRIPTS=random_plugin python my_project.py

If you do create a project that uses hooker, ping me so I can add you
in the README ``Used By`` list!

.. _OrderedDict: https://docs.python.org/3/library/collections.html#collections.OrderedDict
