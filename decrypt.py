from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import hmac
import base64
import json



def decrypt(Master_pass,Password,Service,Mail):
    key = open("examplekey.txt").read() 
    key = bytes.fromhex(key)
    
    with open("exampledata.json") as f:
        Database = json.load(f)
    for entry in Database["Entries"]:
        salt = base64.b64decode( entry["salt"])
        Nonce = base64.b64decode(entry["Nonce"])
        aad = base64.b64decode(entry["aad"])
        ciphertrext = base64.b64decode(entry["ciphertext"])
        iterations = entry["iterations"]
        Service = entry["Service"]
        Mail = entry["Mail"]
        
        kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=iterations,
        )
        Derived_Master = kdf.derive(Master_pass)
        final_key =  hmac.new(key=key, msg=Derived_Master, digestmod=hashlib.sha256).digest() # will not be saved
        aesgcm = AESGCM(final_key)
        decrypted_Password = aesgcm.decrypt(Nonce,ciphertrext,aad)
        print(decrypted_Password)
        

        
decrypt(b"example",b"example",b"example",b"example")
