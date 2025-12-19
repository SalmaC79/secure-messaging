# secure_file_transfer.py

import base64
import json
from file_module import encrypt_file, save_encrypted_file, load_encrypted_file, decrypt_file
from El_gamal_module import generate_keypair
from digital_signature_module import sign, verify  # fonctions de signature ElGamal

# ---------------------------------------------------
# Fonction pour chiffrer un fichier et signer
# ---------------------------------------------------
def secure_file_encrypt(infile_path: str, aes_key: bytes, sender_private_key: dict, outfile_json: str) -> str:
    """
    Chiffre le fichier avec AES et signe le hash avec ElGamal.
    Sauvegarde le tout dans un fichier JSON.
    Affiche le contenu chiffré.
    """
    try:
        # 1️⃣ Chiffrement AES
        enc_dict = encrypt_file(aes_key, infile_path)

        # 2️⃣ Signature ElGamal du hash du fichier original
        signature = sign(infile_path, sender_private_key, data_type="file")

        # 3️⃣ Ajouter signature dans le JSON
        enc_dict["signature"] = signature

        # 4️⃣ Sauvegarder JSON
        save_encrypted_file(enc_dict, outfile_json)

        # 5️⃣ Afficher le contenu chiffré dans la console
        print("\n🔒 Contenu chiffré (JSON) :")
        print(json.dumps(enc_dict, indent=4))

        return outfile_json
    except Exception as e:
        raise RuntimeError(f"Erreur dans secure_file_encrypt: {e}")


# ---------------------------------------------------
# Fonction pour déchiffrer un fichier et vérifier la signature
# ---------------------------------------------------
def secure_file_decrypt(infile_json: str, aes_key: bytes, sender_public_key: dict, output_path: str) -> bool:
    """
    Déchiffre le fichier JSON et vérifie la signature avec la clé publique.
    Sauvegarde le fichier déchiffré.
    Retourne True si la signature est valide, False sinon.
    """
    try:
        # 1️⃣ Charger JSON
        enc_dict = load_encrypted_file(infile_json)

        # 2️⃣ Extraire la signature
        signature = enc_dict.pop("signature", None)
        if signature is None:
            raise ValueError("Aucune signature trouvée dans le JSON")

        # 3️⃣ Déchiffrement AES
        decrypt_file(aes_key, enc_dict, output_path)

        # 4️⃣ Vérification de la signature
        valid = verify(output_path, signature, sender_public_key, data_type="file")

        return valid
    except Exception as e:
        raise RuntimeError(f"Erreur dans secure_file_decrypt: {e}")
