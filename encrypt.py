import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import hmac
import base64
import json

def encrypt(Master_pass:bytes,Password: bytes,Service:str,Mail:str,count:int,Update_Existing:bool):
    with open("config.json") as f:
        config = json.load(f)  

    key_path = config["directories"][0]
    data_path = config["directories"][1]
    
    Nonce = os.urandom(12)# will be saved with the password, 2 different Nonces will be generated
    try:
        with open(key_path, "r") as f:
            key = f.read()
    except FileNotFoundError:
        raise SystemExit("File not found change values in config.json")
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

    try:
        with open(data_path) as f:
            Database = json.load(f)
    except FileNotFoundError:
        raise SystemExit("File not found change values in config.json")
    
    Datatosave = {
                    "Service":Service,
                    "Mail": Mail,
                    "Nonce":base64.b64encode(Nonce).decode(),
                    "salt":base64.b64encode(salt).decode(),
                    "iterations":KDFIterations,
                    "ciphertext":base64.b64encode(encryptedpassword).decode(),
                    "aad": base64.b64encode(aad).decode(),
                    "count":count
                            }
    
    entries = Database.setdefault("Entries", [])
    updated = False
    for entry in entries:
        if (entry["count"] == count
            and Update_Existing
            and entry["Service"] == Service
            and entry["Mail"] == Mail):
            entry.update(Datatosave)
            updated = True
            break

    if not updated:
        entries.append(Datatosave)
            
    with open("exampledata.json", "w") as f:
        json.dump(Database, f, indent=2)