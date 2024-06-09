import os
import hashlib
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def hash_data(data):
    hash_object = hashlib.sha256(data.encode('utf-8'))
    return hash_object.hexdigest()

def hash_data_md5(data):
    hash_object = hashlib.md5(data.encode('utf-8'))
    return hash_object.hexdigest()


def hash_data_sha512(data):
    hash_object = hashlib.sha512()
    hash_object.update(data.encode('utf-8'))
    return hash_object.hexdigest()


## Metodo RC4
def generate_key():
    return os.urandom(16)

def rc_encrypt(key, data):
    algorithm = algorithms.ARC4(key)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(data.encode('utf-8')) 
    
def rc_decrypt(key, data):
    algorithm = algorithms.ARC4(key)
    cipher = Cipher(algorithm, mode=None, backend=default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(data).decode('utf-8')