import hooker

@hooker.hook(["test1", "test2"], ["wildcard", "wildcard2"])
def iterables():
    print("\tI listen to test1 AND test2 events with iterable dependencies!")
