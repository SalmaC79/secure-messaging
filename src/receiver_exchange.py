import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from El_gamal_module import load_keys, decrypt_aes_key

def main():
    # Charger ses clés
    public, private = load_keys("receiver")

    # Lire ciphertext du sender
    with open("cipher_aes_key.json", "r") as f:
        data = json.load(f)

    cipher = {"a": int(data["a"]), "b": int(data["b"])}

    # Déchiffrer la clé AES
    aes_key = decrypt_aes_key(cipher, private)
    print("Receiver recovered AES Key:", aes_key.hex())

    # Sauvegarder la session key pour utilisation AES
    with open("session_key.bin", "wb") as f:
        f.write(aes_key)

    print("Session key stored → session_key.bin")

if __name__ == "__main__":
    main()
