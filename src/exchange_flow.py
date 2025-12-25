import os
import sys
import json
from colorama import init, Fore, Back, Style
init(autoreset=True)

# Accès aux modules dans src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))
KEYS_DIR = "keys"

from El_gamal_module import (
    generate_keypair,
    load_keys,
    encrypt_aes_key,
    decrypt_aes_key
)

from aes_module import (
    generate_aes_key,
)

# =========================================================
# 1️⃣ Initialisation du Receiver (ElGamal)
# =========================================================

def setupkeysElgamal(user_prefix):
    """
    Génère (si nécessaire) les clés ElGamal du receiver
    """
    public, private = generate_keypair(user_prefix)
    #print(Style.DIM +"✔ Receiver is ready (ElGamal keys available).")
    return public, private



# =========================================================
# 2️⃣ Sender : génération + chiffrement de la clé AES
# =========================================================

def sender_send_session_key(receiver_prefix):
    """
    Le sender génère une clé AES et la chiffre avec la clé publique du receiver
    """
    os.makedirs(KEYS_DIR, exist_ok=True)

    public_key, _ = load_keys(receiver_prefix)

    aes_key = generate_aes_key()
    print(Style.DIM +"✔ Sender generated AES session key .")

    cipher = encrypt_aes_key(aes_key, public_key)

    cipher_json = {
        "a": str(cipher["a"]),
        "b": str(cipher["b"])
    }

    cipher_path = os.path.join(KEYS_DIR, "cipher_aes_key.json")

    with open(cipher_path, "w") as f:
        json.dump(cipher_json, f, indent=4)

    return aes_key  # utile pour test/debug


# =========================================================
# 3️⃣ Receiver : déchiffrement et stockage de la clé AES
# =========================================================
def receiver_receive_session_key(receiver_prefix):
    """
    Le receiver déchiffre la clé AES reçue et la stocke localement
    """
    _, private_key = load_keys(receiver_prefix)

    cipher_path = os.path.join(KEYS_DIR, "cipher_aes_key.json")

    if not os.path.exists(cipher_path):
        print(Fore.RED + "\n❌ Error: No encrypted AES key found.")
        print(" Make sure the sender has sent the AES key first.")
        return 

    try:
        with open(cipher_path, "r") as f:
            data = json.load(f)

        cipher = {
            "a": int(data["a"]),
            "b": int(data["b"])
        }

    except (KeyError, ValueError, json.JSONDecodeError):
        print("❌ Error: Encrypted AES key file is corrupted or invalid.")
        return None

    aes_key = decrypt_aes_key(cipher, private_key)

    session_key_path = os.path.join(KEYS_DIR, "session_key.bin")

    with open(session_key_path, "wb") as f:
        f.write(aes_key)

    #print("✔ Receiver decrypted AES key:", aes_key.hex())
    print(Style.DIM +f"✔ Session key stored ({session_key_path})")

    return aes_key
