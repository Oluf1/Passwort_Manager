import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hashlib

Device_Key = open("examplekey.txt").read()
Example_Masterpasswort = "Passwort123"

