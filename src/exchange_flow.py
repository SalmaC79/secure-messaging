import os
import sys
import json

# Accès aux modules dans src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from El_gamal_module import (
    generate_keypair,
    load_keys,
    encrypt_aes_key,
    decrypt_aes_key
)

from aes_module import (
    generate_aes_key,
    encrypt_message,
    decrypt_message,
    serialize_encrypted_message,
    deserialize_encrypted_message
)

# =========================================================
# 1️⃣ Initialisation du Receiver (ElGamal)
# =========================================================

def receiver_setup(user_prefix="receiver"):
    """
    Génère (si nécessaire) les clés ElGamal du receiver
    """
    generate_keypair(user_prefix)
    print("✔ Receiver is ready (ElGamal keys available).")


# =========================================================
# 2️⃣ Sender : génération + chiffrement de la clé AES
# =========================================================

def sender_send_session_key(receiver_prefix="receiver"):
    """
    Le sender génère une clé AES et la chiffre avec la clé publique du receiver
    """
    public_key, _ = load_keys(receiver_prefix)

    aes_key = generate_aes_key()
    print("✔ Sender generated AES session key:", aes_key.hex())

    cipher = encrypt_aes_key(aes_key, public_key)

    cipher_json = {
        "a": str(cipher["a"]),
        "b": str(cipher["b"])
    }

    with open("cipher_aes_key.json", "w") as f:
        json.dump(cipher_json, f)

    print("✔ Encrypted AES key sent (cipher_aes_key.json)")

    return aes_key  # utile pour test/debug


# =========================================================
# 3️⃣ Receiver : déchiffrement et stockage de la clé AES
# =========================================================

def receiver_receive_session_key(receiver_prefix="receiver"):
    """
    Le receiver déchiffre la clé AES reçue et la stocke localement
    """
    _, private_key = load_keys(receiver_prefix)

    with open("cipher_aes_key.json", "r") as f:
        data = json.load(f)

    cipher = {
        "a": int(data["a"]),
        "b": int(data["b"])
    }

    aes_key = decrypt_aes_key(cipher, private_key)

    with open("session_key.bin", "wb") as f:
        f.write(aes_key)

    print("✔ Receiver decrypted AES key:", aes_key.hex())
    print("✔ Session key stored (session_key.bin)")

    return aes_key


# =========================================================
# 4️⃣ Messagerie sécurisée avec AES-GCM
# =========================================================

def secure_message_exchange(message: str):
    """
    Chiffrement et déchiffrement d'un message avec AES-GCM
    """
    if not os.path.exists("session_key.bin"):
        raise FileNotFoundError("❌ session_key.bin not found. Run key exchange first.")

    with open("session_key.bin", "rb") as f:
        aes_key = f.read()

    print("✔ AES session key loaded.")

    plaintext_bytes = message.encode("utf-8")

    encrypted = encrypt_message(aes_key, plaintext_bytes)
    serialized = serialize_encrypted_message(encrypted)

    print("\n📤 Encrypted message (JSON):")
    print(serialized)

    received = deserialize_encrypted_message(serialized)

    decrypted = decrypt_message(
        aes_key,
        received["nonce"],
        received["ciphertext"],
        received["tag"]
    )

    print("\n📥 Decrypted message:")
    print(decrypted.decode("utf-8"))


