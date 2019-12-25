Project Authors
===============

First you got to declare your event like that:

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

   results1 = hooker.EVENTS["on_start"]()
   results2 = hooker.EVENTS["with_open"]("/tmp/path", 1234)

The return value is an `OrderedDict`_:
``{<hook_function_pointer>: <return value>}``, so that you know exactly
the order that the hooks where fired and you can get info about the hook
from the function pointer.

You don't have to import all the plugins, as the user can use the
``HOOKER_SCRIPTS`` environment variable.

.. _note:-don't-use-__retvals__-as-argument-when-you're-calling-a-hook.-it-is-a-reserved-magic-variable!:

.. attention::
   NOTE: Don't use ``__retvals__`` as argument when you're calling a hook. It is a reserved magic variable!

Happy Hacking! :)

.. _OrderedDict: https://docs.python.org/3/library/collections.html#collections.OrderedDict