import os
import sys

# Ajouter le dossier src au path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from El_gamal_module import generate_keypair, encrypt_aes_key, decrypt_aes_key
from aes_module import generate_aes_key, encrypt_message, decrypt_message, serialize_encrypted_message, deserialize_encrypted_message

def test_secure_messaging():
    print("=== Test Secure Messaging Pipeline ===")

    # -----------------------------
    # 1️⃣ Génération des clés ElGamal (Receiver)
    # -----------------------------
    public, private = generate_keypair(bits=512)
    print("\nReceiver ElGamal keys generated.")

    # -----------------------------
    # 2️⃣ Sender génère une clé AES
    # -----------------------------
    aes_key = generate_aes_key()
    print("Sender AES key:", aes_key.hex())

    # -----------------------------
    # 3️⃣ Sender chiffre la clé AES avec ElGamal
    # -----------------------------
    cipher = encrypt_aes_key(aes_key, public)
    print("AES key encrypted with ElGamal.")

    # -----------------------------
    # 4️⃣ Receiver déchiffre la clé AES
    # -----------------------------
    recovered_aes = decrypt_aes_key(cipher, private)
    #print("Receiver decrypted AES key:", recovered_aes.hex())

    # Vérification clé AES
    assert recovered_aes == aes_key, " AES keys do not match!"
    print("✔ AES key exchange successful")

    # -----------------------------
    # 5️⃣ Test AES message encryption
    # -----------------------------
    message = "Bonjour, ceci est un message test sécurisé."
    message_bytes = message.encode("utf-8")

# Chiffrement AES
    encrypted_msg = encrypt_message(aes_key, message_bytes)
    serialized = serialize_encrypted_message(encrypted_msg)

# Déchiffrement AES
    deserialized = deserialize_encrypted_message(serialized)
    decrypted_msg = decrypt_message(
        aes_key,
        deserialized["nonce"],
        deserialized["ciphertext"],
        deserialized["tag"]
        )

    decrypted_str = decrypted_msg.decode("utf-8")
    assert decrypted_str == message, "AES decryption failed!"

    print("✔ AES message encryption/decryption successful")

if __name__ == "__main__":
    test_secure_messaging()
