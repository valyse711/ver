# generate_version_json.py
import json
import os
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

# AES key must match your C++ key (32 bytes)
AES_KEY = bytes([
    0x9f, 0xa1, 0x3c, 0x8d, 0x7e, 0x5b, 0x12, 0x4a,
    0xbb, 0xef, 0x90, 0x67, 0xd4, 0x21, 0xfa, 0x3c,
    0x88, 0x11, 0x66, 0x2a, 0x99, 0xcd, 0x57, 0x0b,
    0x3e, 0x44, 0xde, 0x71, 0x8f, 0x0a, 0x23, 0x5c
])

# Inner JSON (what your C++ client decrypts)
inner_json = {
    "success": 1,
    "version": {"version": "1.6"}
}

# Convert to bytes
plaintext = json.dumps(inner_json).encode()

# PKCS7 padding
padder = padding.PKCS7(128).padder()
padded_data = padder.update(plaintext) + padder.finalize()

# Random IV
iv = os.urandom(16)

# AES-CBC encryption
cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv), backend=default_backend())
encryptor = cipher.encryptor()
ciphertext = encryptor.update(padded_data) + encryptor.finalize()

# Base64 encode IV and ciphertext
version_data = {
    "iv": base64.b64encode(iv).decode(),
    "data": base64.b64encode(ciphertext).decode()
}

# Save JSON
with open("version.json", "w") as f:
    json.dump(version_data, f, indent=2)

print("version.json generated successfully!")
