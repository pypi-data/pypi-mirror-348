import os
import secrets
from argon2 import PasswordHasher, exceptions
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM, AESCCM, AESSIV
from cryptography.hazmat.primitives import constant_time
from cryptography.hazmat.backends import default_backend
import base64

def derive_siv_key(password: str) -> bytes:
    # AES-SIV requires a 64-byte key (512 bits) for AES-SIV-512
    digest = hashes.Hash(hashes.SHA512())
    digest.update(password.encode('utf-8'))
    return digest.finalize()

def encrypt_password(password: str) -> str:
    key = derive_siv_key(password)
    aes_siv = AESSIV(key)
    plaintext = password.encode('utf-8')
    ciphertext = aes_siv.encrypt(associated_data=[], data=plaintext)
    return base64.b64encode(ciphertext).decode('utf-8')


PEPPER_LIST = list("mM}€!@#$%^}&*()-_=+[]/{:;'<>,.?/|\`~aAbB1234567890xXzZqQrRtTnNeE")

ph = PasswordHasher()

def hash_password(password: str) -> str:
    if not isinstance(password, str):
        password = password.decode('utf-8')

    pepper = secrets.choice(PEPPER_LIST)
    combined = password + pepper
    encrypted = encrypt_password(combined)
    hashed = ph.hash(encrypted)
    return hashed

def verify_password(password: str, hashed: str) -> bool:
    if not isinstance(password, str):
        password = password.decode('utf-8')
    i = 0

    for pepper in PEPPER_LIST:
        i+=1
        try:
            combined = password + pepper
            encrypted = encrypt_password(combined)
            if ph.verify(hashed, encrypted):
                return True
        except exceptions.VerifyMismatchError as e:
            continue
        except Exception as e:
            print(f"Error occurred: {e}")
            return False
    return False