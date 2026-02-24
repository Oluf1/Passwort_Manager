import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import hmac
import base64
import json
def encrypt(Master_pass,Password,Service,Mail):
    Nonce = os.urandom(12)# will be saved with the password, 2 different Nonces will be generated

    key = open("examplekey.txt").read() #Will be saved on a hard drive
    key = bytes.fromhex(key)
    salt = os.urandom(16)
    aad= os.urandom(16)
    KDFIterations = 1200000
    
    kdf = PBKDF2HMAC( # Will not be saved
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDFIterations,
    )
    Derived_Master = kdf.derive(Master_pass) # will not be saved
    final_key =  hmac.new(key=key, msg=Derived_Master, digestmod=hashlib.sha256).digest() # will not be saved
    aesgcm = AESGCM(final_key) # will not be saved
    encryptedpassword = aesgcm.encrypt(Nonce,Password,aad) # will be saved



    Datatosave = {
        "Service":Service,
        "Mail": Mail,
        "Nonce":base64.b64encode(Nonce).decode(),
        "salt":base64.b64encode(salt).decode(),
        "iterations":KDFIterations,
        "ciphertext":base64.b64encode(encryptedpassword).decode(),
        "aad": base64.b64encode(aad).decode()
                }
    with open("exampledata.json") as f:
        Database = json.load(f)

    Database["Entries"].append(Datatosave)
    with open("exampledata.json", "w") as f:
        json.dump(Database, f, indent=2)