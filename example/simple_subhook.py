import hooker


@hooker.hook("test2", "wildcard")
def foo():
    print("\tbar")
