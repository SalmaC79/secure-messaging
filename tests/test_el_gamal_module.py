import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from El_gamal_module import generate_keypair, save_keys, load_keys, encrypt_aes_key, decrypt_aes_key
from Crypto.Random import get_random_bytes

def main():
    # 1️⃣ Génération des clés ElGamal
    public, private = generate_keypair(bits=1024)  # 1024 bits suffisent pour le test
    save_keys("testuser", public, private)

    # 2️⃣ Charger les clés (simule l'utilisation après sauvegarde)
    public, private = load_keys("testuser")

    # 3️⃣ Générer une clé AES (16 octets)
    aes_key = get_random_bytes(16)
    print("Clé AES originale :", aes_key.hex())

    # 4️⃣ Chiffrement de la clé AES
    cipher = encrypt_aes_key(aes_key, public)
    print("Ciphertext :", cipher)

    # 5️⃣ Déchiffrement de la clé AES
    recovered_key = decrypt_aes_key(cipher, private)
    print("Clé AES récupérée :", recovered_key.hex())

    # ✅ Vérification
    if recovered_key == aes_key:
        print("Succès : la clé AES récupérée est identique à l'originale !")
    else:
        print("Erreur : la clé AES récupérée est différente !")

if __name__ == "__main__":
    main()
