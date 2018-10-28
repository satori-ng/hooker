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
   Reference <modules>

Yellow! This is a simple project that makes the "hooking" plugin
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
