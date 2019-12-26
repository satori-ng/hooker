import sys

from hooker import EVENTS, hook

# Declare the events
EVENTS.append("pre_open_in", "Input file will open. Arguments: path<str>. Return: path<str>")
EVENTS.append("pre_open_out", "Output file will open. Arguments: path<str>. Return: path<str>")
EVENTS.append("encrypt", "Encrypt data. Arguments: data<bytearray>. Return: data<str>")
EVENTS.append("decrypt", "Decrypt data. Arguments: data<bytearray>. Return: data<str>")

@hook("pre_open_in")
def pre_open_in(path):
    return path

@hook("pre_open_out")
def pre_open_out(path):
    return path

@hook("encrypt")
def encrypt(data):
    return data

@hook("decrypt")
def decrypt(data):
    return data

def main():
    encdec = sys.argv[1]
    path_in = sys.argv[2]
    path_out = sys.argv[3]

    if encdec != "-e" and encdec != "-d":
        print("Usage: %s <-e|-d> <input_file> <output_file>" % os.argv[0])
        print("\t-e\tEncrypts input and saves it to `file`")
        print("\t-d\tDecrypts input and saves it to `file`")
        exit(1)

    # Fire the pre_open hook to do path transformations
    pre_in_results = EVENTS["pre_open_in"](path_in)
    # Get the return value of the last hook
    pre_in = pre_in_results.last[1]


    with open(pre_in, "rb") as ind:
        pre_out_results = EVENTS["pre_open_out"](path_out)
        pre_out = pre_out_results.last[1]

        bdatain = bytearray(ind.read())

        with open(pre_out, "wb") as outd:
            # Fire the en/decrypt hook to do data transformations
            if encdec == "-e":
                dataout_results = EVENTS["encrypt"](bdatain)
            elif encdec == "-d":
                dataout_results = EVENTS["decrypt"](bdatain)

            dataout = dataout_results.last[1]
            outd.write(dataout)

if __name__ == "__main__":
    main()
