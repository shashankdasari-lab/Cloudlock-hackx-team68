from cryptography.fernet import Fernet
import base64
import hashlib
import os
import uuid

def generate_key(password: str) -> bytes:
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

def encrypt_text(text: str, password: str) -> str:
    key = generate_key(password)
    f = Fernet(key)
    return f.encrypt(text.encode()).decode()

def decrypt_text(token: str, password: str) -> str:
    key = generate_key(password)
    f = Fernet(key)
    return f.decrypt(token.encode()).decode()

def encrypt_file(file_path: str, password: str) -> str:
    key = generate_key(password)
    f = Fernet(key)
    with open(file_path, 'rb') as fp:
        data = fp.read()
    encrypted = f.encrypt(data)
    enc_path = f"{file_path}.enc"
    with open(enc_path, 'wb') as fp:
        fp.write(encrypted)
    # remove original file to keep only encrypted
    try:
        os.remove(file_path)
    except Exception:
        pass
    return enc_path

def decrypt_file(enc_path: str, password: str) -> str:
    key = generate_key(password)
    f = Fernet(key)
    with open(enc_path, 'rb') as fp:
        data = fp.read()
    decrypted = f.decrypt(data)
    # write to a temp file
    base = os.path.splitext(enc_path)[0]
    temp_out = f"{base}_decrypted_{uuid.uuid4().hex[:6]}{os.path.splitext(base)[1]}"
    with open(temp_out, 'wb') as fp:
        fp.write(decrypted)
    return temp_out


