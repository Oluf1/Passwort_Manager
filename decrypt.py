from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import hmac
import base64
import json
import cryptography.exceptions



def decrypt(Master_pass,Service,Mail,count):
    with open("config.json") as f:
        config = json.load(f)  

    key_path = config["directories"][0]
    data_path = config["directories"][1]
    try:
        with open(key_path, "r") as f:
            key = f.read()
    except FileNotFoundError:
        raise SystemExit("File not found change values in config.json")
    key = bytes.fromhex(key)
    try:
        with open(data_path) as f:
            Database = json.load(f)
    except FileNotFoundError:
        raise SystemExit("File not found change values in config.json")
        
    for entry in Database["Entries"]:
        salt = base64.b64decode( entry["salt"])
        Nonce = base64.b64decode(entry["Nonce"])
        aad = base64.b64decode(entry["aad"])
        ciphertrext = base64.b64decode(entry["ciphertext"])
        iterations = entry["iterations"]
        entry_Service = entry["Service"]
        entry_Mail = entry["Mail"]
        entry_count = entry["count"]
            
            
        
        
        if entry_Service == Service and entry_Mail== Mail and entry_count == count:
            kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=iterations,
            )       
            Derived_Master = kdf.derive(Master_pass)
            final_key =  hmac.new(key=key, msg=Derived_Master, digestmod=hashlib.sha256).digest() # will not be saved
            aesgcm = AESGCM(final_key)
            try:
                decrypted_Password = aesgcm.decrypt(Nonce,ciphertrext,aad).decode('utf-8')
                print(F"Password: {decrypted_Password}")
                
                
            except cryptography.exceptions.InvalidTag:
                print("Wrong masterpassword")   
            except Exception as error:
                print(f"different error:{error}")
                
            break
    else:
        print("No Matching entry")
        

        

