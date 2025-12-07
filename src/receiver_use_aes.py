import os
import sys
import json

# Path vers les modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from aes_module import (
    encrypt_message,
    decrypt_message,
    serialize_encrypted_message,
    deserialize_encrypted_message
)

def main():

    # --------------------------
    # 1. Charger la session key
    # --------------------------
    if not os.path.exists("session_key.bin"):
        print("ERROR: session_key.bin not found! Run key exchange first.")
        return

    with open("session_key.bin", "rb") as f:
        aes_key = f.read()

    print("✔ Loaded AES session key:", aes_key.hex())

    # --------------------------
    # 2. Saisie du message user
    # --------------------------
    message = input("\n  Enter a message to encrypt: ").strip()

    if message == "":
        print("ERROR: Message cannot be empty.")
        return

    message_bytes = message.encode("utf-8")

    # --------------------------
    # 3. Encryption AES-GCM
    # --------------------------
    encrypted = encrypt_message(aes_key, message_bytes)
    serialized = serialize_encrypted_message(encrypted)

    print("\n📤 Encrypted message sent to peer (JSON):")
    print(serialized)

    # --------------------------
    # 4. Decryption
    # --------------------------
    received = deserialize_encrypted_message(serialized)
    decrypted = decrypt_message(
        aes_key,
        received["nonce"],
        received["ciphertext"],
        received["tag"]
    )

    print("\n📥 Decrypted message:")
    print(decrypted.decode("utf-8"))

    print("\n✔ Secure AES messaging works correctly!")

if __name__ == "__main__":
    main()
