import os
import sys
from El_gamal_module import generate_keypair, encrypt_aes_key, decrypt_aes_key
from aes_module import encrypt_message, decrypt_message, generate_aes_key
from hash_module import hash_message

import json
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# -------------------------------------------
# WRAP: Encryption routine
# -------------------------------------------
def secure_encrypt(message: str, receiver_public_key):

    # Convert to bytes
    msg_bytes = message.encode()

    # 1) Hash message (string → hash)
    digest = hash_message(message)

    # 2) Generate AES key
    aes_key = generate_aes_key()

    # 3) Encrypt message with AES-GCM
    enc = encrypt_message(aes_key, msg_bytes)

    # 4) Encrypt AES key using receiver's ElGamal public key
    encrypted_aes_key = encrypt_aes_key(aes_key, receiver_public_key)

    # Package all
    package = {
        "ciphertext": enc["ciphertext"].hex(),
        "nonce": enc["nonce"].hex(),
        "tag": enc["tag"].hex(),
        "aes_key_enc": encrypted_aes_key,
        "hash": digest
    }

    return package


# -------------------------------------------
# WRAP: Decryption routine
# -------------------------------------------
def secure_decrypt(package, receiver_private_key):

    # 1) Recover AES key
    aes_key = decrypt_aes_key(package["aes_key_enc"], receiver_private_key)

    # 2) Convert hex → raw bytes
    ciphertext = bytes.fromhex(package["ciphertext"])
    nonce = bytes.fromhex(package["nonce"])
    tag = bytes.fromhex(package["tag"])

    # 3) AES-GCM decrypt
    plaintext_bytes = decrypt_message(aes_key, nonce, ciphertext, tag)

    plaintext = plaintext_bytes.decode()

    # 4) Hash verification
    digest = hash_message(plaintext)
    if digest != package["hash"]:
        raise ValueError("Integrity check failed! Hash mismatch.")

    return plaintext

