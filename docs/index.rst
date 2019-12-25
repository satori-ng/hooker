.. Hooker documentation master file, created by
   sphinx-quickstart on Sun Oct 28 07:01:54 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Hooker's documentation!
==================================

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   plugin_creators
   project_authors
   example
   Reference <modules>

Yellow! This is a simple project that makes the event-driver plugin
architecture a bit easier in python.

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

Event-driven plugin architecture?
---------------------------------

It's the idea that whenever you carry out a "worthy" operation,
you fire up an event, you take some results from the plugins
and you act on them.

A "worthy" operation is a functionality that someone will likely
be interested in changing through a plugin.

An "event" is like broadcast to all currently loaded plugins and if
someone is interested (which is declared through ``@hooker.hook`` decorator)
it is notified and given the appropriate call arguments.

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
