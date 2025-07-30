import os
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import json

class FBH:
    def __init__(self):
        self.key_length = 32
        self.salt_length = 16
        self.nonce_length = 16
        self.tag_length = 16

        self.metadata = {
            "instructions": (
                "This file is encrypted using FBH.\n"
                "To decrypt, run: FBH decode <password> <file>\n"
                "If encrypted without password, decryption is not possible.\n"
                "Contact t.me/Team_X_OG for support."
            ),
            "credits": "Created by t.me/dev_x_ninja and https://t.me/Team_X_OG"
        }

    def _derive_key(self, password, salt):
        """Derive AES key from password"""
        return PBKDF2(password.encode(), salt, dkLen=self.key_length, count=100000)

    def hide_file(self, input_file, output_file, password=None):
        """Encrypt file"""
        try:
            with open(input_file, 'rb') as f:
                data = f.read()

            metadata_bytes = json.dumps(self.metadata).encode()

            salt = get_random_bytes(self.salt_length)
            if password:
                key = self._derive_key(password, salt)
            else:
                key = get_random_bytes(self.key_length)

            cipher = AES.new(key, AES.MODE_GCM)
            nonce = cipher.nonce

            ciphertext, tag = cipher.encrypt_and_digest(metadata_bytes + b"|||" + data)

            with open(output_file, 'wb') as f:
                if password:
                    f.write(salt + nonce + tag + ciphertext)
                else:
                    f.write(nonce + tag + ciphertext)

            print(f"Encrypted: {output_file}")
        except Exception as e:
            print(f"Error encrypting: {e}")

    def decode_file(self, encrypted_file, output_file, password):
        """Decrypt file"""
        try:
            with open(encrypted_file, 'rb') as f:
                data = f.read()

            if len(data) < self.salt_length + self.nonce_length + self.tag_length:
                raise ValueError("Encrypted without password. Cannot decrypt.")

            salt = data[:self.salt_length]
            nonce = data[self.salt_length:self.salt_length + self.nonce_length]
            tag = data[self.salt_length + self.nonce_length:self.salt_length + self.nonce_length + self.tag_length]
            ciphertext = data[self.salt_length + self.nonce_length + self.tag_length:]

            key = self._derive_key(password, salt)

            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

            metadata_bytes, original_data = decrypted_data.split(b"|||", 1)
            metadata = json.loads(metadata_bytes.decode())

            with open(output_file, 'wb') as f:
                f.write(original_data)

            print("Metadata:")
            print(f"Instructions: {metadata['instructions']}")
            print(f"Credits: {metadata['credits']}")
            print(f"Decrypted: {output_file}")
        except Exception as e:
            print(f"Error decrypting: {e}")