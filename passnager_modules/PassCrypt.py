from cryptography.fernet import Fernet

def pass_encrypt(plain_pwd, secret_key):
    f = Fernet(str.encode(secret_key))
    return f.encrypt(str.encode(plain_pwd)).decode()

def pass_decrypt(encrypted_pwd, secret_key):
    f = Fernet(str.encode(secret_key))
    return f.decrypt(str.encode(encrypted_pwd)).decode()