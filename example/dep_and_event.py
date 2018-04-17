import hooker

hooker.EVENTS.append(["test2", "test3"])

@hooker.hook("test1", "simple_hook")
def world():
    print("\tworld")
