import hooker
import simple_hook

hooker.EVENTS.append(["test2", "test3"])

# "__retvals__" is a magic argument that when found will include all the return
# values of the previously called hooks
@hooker.hook("test1", "simple_hook")
def world(__retvals__):
    print("\tworld")
    print("\t\t" + __retvals__[simple_hook.hello])
