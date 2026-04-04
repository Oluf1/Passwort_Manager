import base64
import hashlib
import hmac
import json
import os

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
):
    with open("config.json") as f:
        config = json.load(f)

    key_path = config["directories"][0]
    data_path = config["directories"][1]

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

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=kdf_iterations,
    )

    derived_master = kdf.derive(master_pass)

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
        "ciphertext": base64.b64encode(encrypted_password).decode(),
        "aad": base64.b64encode(aad).decode(),
        "count": count,
    }

    entries = database.setdefault("Entries", [])
    updated = False

    for entry in entries:
        if (
            entry["count"] == count
            and update_existing
            and entry["Service"] == service
            and entry["Mail"] == mail
        ):
            entry.update(data_to_save)
            updated = True
            break

    if not updated:
        entries.append(data_to_save)

    with open(data_path, "w") as f:
        json.dump(database, f, indent=2)