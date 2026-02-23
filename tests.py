import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import hmac

Master_Pass = b"Password123" # Will not be saved
Nonce = open("Examplenonce.txt","rb").read() # will be saved with the password, 2 different Nonces will be generated
key = open("examplekey.txt").read() #Will be saved on a hard drive
key = bytes.fromhex(key)
salt = open("examplesalt.txt").read() # will be saved with the password 
salt = bytes.fromhex(salt)
data = b"Test_Daten" # Will be saved as an encrypted version
aad= b"" # Will just stay empty hence not saved
kdf = PBKDF2HMAC( # Will not be saved
    algorithm=hashes.SHA256(),
    length=32,
    salt=salt,
    iterations=1_200_000,
)
Derived_Password = kdf.derive(Master_Pass) # will not be saved
final_key =  hmac.new(key=key, msg=Derived_Password, digestmod=hashlib.sha256).digest() # will not be saved
aesgcm = AESGCM(final_key) # will not be saved
encryptedmsg = aesgcm.encrypt(Nonce,data,aad) # will be saved

print(encryptedmsg)
