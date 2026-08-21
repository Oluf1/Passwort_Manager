import base64
import hashlib
import hmac
import json
from typing import TYPE_CHECKING

import cryptography.exceptions
from argon2.low_level import Type, hash_secret_raw
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

if TYPE_CHECKING:
    from main import App  #avoids Circular Importing

def decrypt(master_pass: bytes, service: str, mail: str, count: int,vault_name:str,app:"App")-> str:    
    vault = app.VAULTMANAGER.get_vault(vault_name)
    
    if vault.vault_type == "server":
        return "error server not yet supported"

    key_path = vault.key_path
    data_path = vault.data_path

    try:
        with open(key_path, "r") as f:
            key_hex = f.read()
    except FileNotFoundError:
        raise SystemExit("File not found, change values in config.json")

    key = bytes.fromhex(key_hex)

    try:
        with open(data_path) as f:
            database = json.load(f)
    except FileNotFoundError:
        raise SystemExit("File not found, change values in config.json")

    entry = database["services"][service]

    for Mails in entry:
        salt = base64.b64decode(Mails["salt"])
        nonce = base64.b64decode(Mails["Nonce"])
        aad = base64.b64decode(Mails["aad"])
        ciphertext = base64.b64decode(Mails["ciphertext"])

        iterations = Mails["iterations"]
        entry_service = Mails["Service"]
        entry_mail = Mails["Mail"]
        entry_count = Mails["count"]
        Kdf_type = Mails["Kdf_type"]

        if (
            entry_service == service
            and entry_mail == mail
            and entry_count == count
        ):
    
            match Kdf_type:
                case "PBKDF2":
                    kdf = PBKDF2HMAC(
                        algorithm=hashes.SHA256(),
                        length=32,
                        salt=salt,
                        iterations=iterations,
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

            try:
                decrypted_password = aesgcm.decrypt(
                    nonce,
                    ciphertext,
                    aad,
                ).decode("utf-8")
                
                return decrypted_password
            except cryptography.exceptions.InvalidTag:
                app.ui_handler.show_error("Wrong masterpassword")
                raise Exception("Wrong masterpassword")
            except Exception as error:
                raise Exception(f"Different error {error}")

    else:
        raise Exception("No matching entry")
