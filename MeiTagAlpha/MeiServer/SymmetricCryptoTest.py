#!/usr/bin/python\ 

import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def encryptF(password, salt, message): #use this to encrypt. All values are bytes
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    encrypted_text = f.encrypt(message)
    return encrypted_text

def decryptF(password, salt, encrypted_text): #use this to decrypt. All values are bytes
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
    key = base64.urlsafe_b64encode(kdf.derive(password))
    f = Fernet(key)
    decrypted_text = f.decrypt(encrypted_text)
    return decrypted_text
