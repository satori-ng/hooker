# Crypter

This is an example usage of hooker. It takes an input file,
transforms it (encrypt/encode/decrypt/decode) and writes it
to the output file.

The main script (`crypter.py`) only reads, writes files and determines
if encryption or decryption takes place (from the `-e/-d` flag). It fires
events to do the rest. So if you call it without `HOOKER_SCRIPTS`, the two
files will be identical.

Fernet encryption: `HOOKER_SCRIPTS=fernet py crypter.py -e /tmp/test /tmp/test.enc`

Fernet decryption: `HOOKER_SCRIPTS=fernet py crypter.py -d /tmp/test.enc /tmp/test.dec`

You can try `HOOKER_SCRIPTS=reverse`, which reverses its input.

As an excercise, you can hook the `pre_open_out` and `pre_open_in` events to make
the script read/write all the files in a hidden directory.

You can see all the events and its description by calling:
`python -m hooker crypter.py`

<aside class="warning">
As this is an example, nobody would use for real world scenarios, right?
</aside>
