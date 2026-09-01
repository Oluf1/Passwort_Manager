import base64
import hashlib
import hmac
import json
import os

from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def encrypt(
    master_pass: bytes,
    password: bytes,
    service: str,
    mail: str,
    count: int,
    update_existing: bool,
    new_mail:str,
    vault,
    Kdf_type
):
    key_path = vault.key_path
    data_path = vault.data_path

    nonce = os.urandom(12)  # saved with the password
    try:
        with open(key_path, "r") as f:
            key_hex = f.read()
    except FileNotFoundError:
        raise SystemExit("File not found, change values in config.json")

    key = bytes.fromhex(key_hex)

    salt = os.urandom(16)
    aad = os.urandom(16)
    kdf_iterations = 1_200_000
    match Kdf_type:
        case "PBKDF2":
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=kdf_iterations,
            )
            derived_master = kdf.derive(master_pass)
        case "Argon2":
            derived_master = hash_secret_raw(
                secret=master_pass,
                salt=salt,
                time_cost=3,
                memory_cost=65536,  
                parallelism=4,
                hash_len=32,
                type=Type.ID,
            )
        case _:
            raise SystemExit("not a KDF Function")
            

   

    final_key = hmac.new(
        key=key,
        msg=derived_master,
        digestmod=hashlib.sha256,
    ).digest()

    aesgcm = AESGCM(final_key)
    encrypted_password = aesgcm.encrypt(nonce, password, aad)

    try:
        with open(data_path) as f:
            database = json.load(f)
    except FileNotFoundError:
        raise SystemExit("File not found, change values in config.json")

    data_to_save = {
        "Service": service,
        "Mail": mail,
        "Nonce": base64.b64encode(nonce).decode(),
        "salt": base64.b64encode(salt).decode(),
        "iterations": kdf_iterations,
        "Kdf_type":Kdf_type,
        "ciphertext": base64.b64encode(encrypted_password).decode(),
        "aad": base64.b64encode(aad).decode(),
        "count": count,
    }

    
    if not update_existing:
        for ele in database["services"][service]:
            if ele["Mail"] == mail:
                count+=1 
        
        data_to_save["count"] = count        
        
        database["services"].setdefault(service,[])
        database["services"][service].append(data_to_save)
    else:
        data_to_save["Mail"] = new_mail
        if mail != new_mail:
            count = 1
            for entry in database["services"][service]:
                if entry["Mail"] == new_mail:
                    count +=1 
            data_to_save["count"] = count
        
        for i, entry in enumerate(database["services"][service]):
            if entry["Mail"] == mail and entry["count"] == count:
                data_to_save["Mail"] = new_mail
                database["services"][service][i] = data_to_save
                break
        else:
            raise Exception("no matching entry found")
    
    with open(data_path, "w") as f:
        json.dump(database, f, indent=2)