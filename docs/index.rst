Welcome to Hooker's documentation!
==================================

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   project_authors
   plugin_creators
   example
   Reference <modules>

Yellow! This is a simple project that makes the event-driver plugin
architecture a bit easier in python.

If you know what I'm talking about and want to use it in your project,
read :doc:`this <project_authors>`

If you know what I'm talking about and want to write a plugin that uses
hooker, read :doc:`this <plugin_creators>`

Here, take a look:

.. code:: python

   import hooker
   # State your event
   hooker.EVENTS.append("fire", help="This is called when the gun is fired")

   # Hook your event
   @hooker.hook("fire")
   def cock():
       print("-> Fire was shot")

   print("Gun loaded")
   print("Firing")
   # Fire your hooked event
   hooker.EVENTS["fire"]()
   # cock() was called

If you're a

Event-driven plugin architecture?
---------------------------------

It's the idea that whenever you carry out an operation "worthy"
enough to be acted upon by plugins, you fire up an event,
maybe take some results from the plugins and act on them.

A "worthy" operation is a functionality that someone will likely
be interested in changing through a plugin.

An "event" is like a broadcasted message to all currently loaded plugins
and if someone is interested (which is declared through the ``@hooker.hook``
decorator) it is notified and given the appropriate call arguments.

Take for example the following workflow of a program that performs decryption
on the given file, without the utilization of events (let's say that you just
give a file as a parameter to that program):

.. graphviz::

   digraph Flatland {
      "File exists?" -> "File is valid?" -> "Decrypt file" -> "Print result";
   }


The problem here is that you can't alter the behaviour. Let's say that you want
to model the above program so that you could for add decryption algorithms:


.. graphviz::

   digraph Flatland {
      "File exists?" -> "File is valid?" -> "Call event for decryption algorithms" -> "Decrypt file based on previous event" -> "Print result";
   }

Of course there are many more points that it's useful to call events, but this
is an example after all. To see code that does the above, take a look :doc:`here <example>`