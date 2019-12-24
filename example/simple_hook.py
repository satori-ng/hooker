import hooker


@hooker.hook("test1")
def hello():
    print("\thello!")
    return "I returned something"
