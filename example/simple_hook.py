import hooker

@hooker.hook("test1")
def hello():
    print("\thello!")
