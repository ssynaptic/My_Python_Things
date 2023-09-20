from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from os.path import (dirname,
                     join,
                     exists)
import cryptography
import secrets
import base64

class CryptoHandler:
    def __init__(self):
        pass

    def generate_salt(self, size=16):
        return secrets.token_bytes(nbytes=size)

    def derive_key(self, salt, password):
        kdf = Scrypt(salt=salt,
                     length=32,
                     n=2**14,
                     r=8,
                     p=1)
        return kdf.derive(password.encode(encoding="utf-8"))

    def load_salt(self):
       salt_path = join(dirname(__file__), "salt.salt")
       return open("salt.salt", "rb").read()

    def generate_key(self, password, salt_size, load_existing_salt=False, save_salt=True):
        if load_existing_salt:
            salt = self.load_salt()
        elif save_salt:
            salt = self.generate_salt(size=salt_size)
            with open("salt.salt", "wb") as salt_file:
                salt_file.write(salt)
        derived_key = self.derive_key(salt=salt,
                                      password=password)
        return base64.urlsafe_b64encode(derived_key)

    def encrypt(self, filename, key):
        f = Fernet(key=key)
        with open(filename, "rb") as file:
            file_data = file.read()

        encrypted_data = f.encrypt(file_data)

        with open(filename, "wb") as file:
            file.write(encrypted_data)

        return "encrypted_successfully"

    def decrypt(self, filename, key):
        f = Fernet(key)
        with open(filename, "rb") as file:
            encrypted_data = file.read()
        try:
            decrypted_data = f.decrypt(encrypted_data)
            with open(filename, "wb") as file:
                file.write(decrypted_data)

            return "decrypted_succesfully"

        except cryptography.fernet.InvalidToken:
            return "decrypted_failed"

        with open(filename, "wb") as file:
            file.write(decrypted_data)

    # write_key()
    # key = load_key()
    # print(key)

    # sms = "This is a proof, a very long proof".encode(encoding="utf-8")

    # f = Fernet(key=key)
    # encrypted = f.encrypt(sms)
    # print(encrypted)

    # decrypted = f.decrypt(encrypted)
    # print(decrypted)