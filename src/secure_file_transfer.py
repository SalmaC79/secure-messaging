import base64,os,sys
from src.file_module import encrypt_file, decrypt_file, save_encrypted_file, load_encrypted_file
# from src.digital_signature_module import sign, verify
BASE_DIR = os.path.dirname(__file__)       # /project/tests
SRC_PATH = os.path.abspath(os.path.join(BASE_DIR, ".."))  # /project

sys.path.append(SRC_PATH)

from src.digital_signature_module import sign, verify

# ----------------------
# Envoi d'un fichier sécurisé
# ----------------------
def envoyer_fichier_secure(aes_key, infile_path, sender_private_key, receiver_public_key):
    """
    Chiffre un fichier avec AES et signe le hash.
    Retourne un paquet dict {fichier_chiffre, signature}
    """
    # 1️⃣ Chiffrer le fichier
    enc_dict = encrypt_file(aes_key, infile_path)

    # 2️⃣ Signer le hash du fichier original
    signature = sign(infile_path, sender_private_key, data_type="file")

    # 3️⃣ Créer le paquet à envoyer
    paquet = {
        "fichier_chiffre": enc_dict,
        "signature": signature
    }

    return paquet

# ----------------------
# Réception d'un fichier sécurisé
# ----------------------
def recevoir_fichier_secure(aes_key, paquet, sender_public_key, output_path):
    """
    Déchiffre un fichier et vérifie la signature.
    """
    enc_dict = paquet["fichier_chiffre"]
    signature = paquet["signature"]

    # 1️⃣ Déchiffrer le fichier
    decrypt_file(aes_key, enc_dict, output_path)

    # 2️⃣ Vérifier la signature sur le fichier déchiffré
    if not verify(output_path, signature, sender_public_key, data_type="file"):
        raise ValueError("Signature invalide ! Le fichier peut avoir été altéré.")
