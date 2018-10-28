import os
import base64
from getpass import getpass

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from hooker import hook

FERNET = None

@hook("pre_open_in")
def pre_open_in(path):
    global FERNET

    password = getpass("Please enter password: ")

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b"thisisunsafe!",
        iterations=100000,
        backend=default_backend()
    )
    derived = kdf.derive(bytes(password, "utf8"))
    key = base64.urlsafe_b64encode(derived)

    FERNET = Fernet(key)

    return path

@hook("encrypt")
def encrypt(data):
    global FERNET
    return FERNET.encrypt(bytes(data))

@hook("decrypt")
def decrypt(data):
    global FERNET
    return FERNET.decrypt(bytes(data))
