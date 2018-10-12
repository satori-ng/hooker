import hooker

hooker.EVENTS.append("test1", "This is the first hook. Where am I defined?")

import dep_and_event
import iterables
import simple_hook
import simple_subhook
import wildcard
import wildcard2

print("Calling test1:")
# print(hooker.EVENTS["test1"]())
print(hooker.EVENTS["test1"]())
print("Calling test2 (defined by dep_and_event):")
print(hooker.EVENTS["test2"]())
print("Calling test3 (defined by dep_and_event):")
print(hooker.EVENTS["test3"]())
