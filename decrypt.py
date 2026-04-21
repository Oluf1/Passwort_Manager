import base64
import hashlib
import hmac
import json

import cryptography.exceptions
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def decrypt(master_pass: bytes, service: str, mail: str, count: int,vault:str)-> str:
    with open("config.json") as f:
        config = json.load(f)["Vaults"][vault]
    if config["type"] == "server":
        return "error server not yet supported"
    key_path = config["directories"][0]
    data_path = config["directories"][1]

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

        if (
            entry_service == service
            and entry_mail == mail
            and entry_count == count
        ):
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=iterations,
            )

            derived_master = kdf.derive(master_pass)

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
                
                print("Wrong master password")
                return "Wrong master password"

            except Exception as error:
                print(f"Different error: {error}")
                return f"Different error: {error}"

            break
    else:
        
        print("No matching entry")
        return "No matching entry"