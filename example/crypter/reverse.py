from hooker import hook

@hook(["encrypt", "decrypt"])
def pre_open(data):
    return data[::-1]
