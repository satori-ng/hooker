import hooker
import simple_hook

hooker.EVENTS.append(["test2", "test3"])

# "retvals" is a magic argument that when found will include all the return
# values of the previously called hooks
@hooker.hook("test1", "simple_hook")
def world(retvals):
    print("\tworld")
    print("\t\t" + retvals[simple_hook.hello])
