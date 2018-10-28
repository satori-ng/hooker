# Arcane Hooker

I'm a hooker from Silvermoon City. Let me show you the Arcane way to Python

NOTE: Use me, use me haaaard...

For documentation check the [wiki](https://satori-ng.github.io/hooker/)

Installation: `pip install hooker`

---

This is my attempt to reinvent the hooking wheel.
I try to keep it simple for both providers and consumers.

The whole idea is that there are events, created by either the guts of the app
or a plugin itself on runtime.
After that, the required plugins that actually implemnt hooks on the events
should be imported.

While the code is not a mess, I'm using a fair bit of python magic,
at least that's what I think so. The target is to provide the simplest
possible API for both project and plugin authors.

If you have a better way to do something, at least open an issue to
discuss it, I'm very interested!

Happy Hacking! :)
