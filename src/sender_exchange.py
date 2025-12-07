import json
import os
import sys
from Crypto.Random import get_random_bytes

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from El_gamal_module import load_keys, encrypt_aes_key
from aes_module import generate_aes_key   

def main():
    # Charger la clé publique du receiver
    public, _ = load_keys("receiver")

    # 1) Générer la clé AES (session)
    aes_key = generate_aes_key()
    print("Sender AES Key:", aes_key.hex())

    # 2) Chiffrer la clé AES avec ElGamal (Task 1.1)
    cipher = encrypt_aes_key(aes_key, public)  # {'a': int, 'b': int}

    # 3) Sauvegarder ciphertext dans un fichier (simulation d'envoi)
    cipher_json = {"a": str(cipher["a"]), "b": str(cipher["b"])}
    with open("cipher_aes_key.json", "w") as f:
        json.dump(cipher_json, f)

    # Optionnel : sauvegarder la clé AES pour test
    with open("sender_session_key.bin", "wb") as f:
        f.write(aes_key)

    print("Ciphertext sent → cipher_aes_key.json")

if __name__ == "__main__":
    main()
