# Passwort_Manager
Passwort Manager using AES 256 GCM encryption with server Viability

Passwords get encrypted using a key which gets derived from a combination of a Masterpassword and a 256 byte key saved on disk.
The Masterpassword first gets derived using PBKDF2 (both the Salt and iterations get saved with the final password) then the final key is derived using HMAC with both the Masterpassword and the saved key 
Then a random Nonce is generated (12 bytes) this will also be saved with the final password
Afterwards AESGCM 256 is used with said Nonce and the Derived key with the aad

Master password is example
