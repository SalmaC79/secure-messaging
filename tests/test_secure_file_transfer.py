import sys
import os
import subprocess  # pour ouvrir le fichier audio après déchiffrement

# Ajouter le dossier src au path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # dossier tests
SRC_PATH = os.path.join(BASE_DIR, "..", "src")        # dossier src
sys.path.insert(0, SRC_PATH)

# Imports
from aes_module import generate_aes_key
from secure_file_transfer import secure_file_encrypt, secure_file_decrypt
from El_gamal_module import generate_keypair  # pour générer clés ElGamal

def main():
    print("===== TEST RÉEL : Secure File Transfer =====\n")

    # -----------------------------
    # 1️⃣ Génération des clés
    # -----------------------------
    print("🔐 Génération des clés ElGamal pour la signature...")
    sender_public_key, sender_private_key = generate_keypair("sender_test")

    print("🔑 Génération de la clé AES...")
    aes_key = generate_aes_key()

    # -----------------------------
    # 2️⃣ Chemins relatifs des fichiers
    # -----------------------------
    # Crée un sous-dossier 'files' pour stocker les fichiers de test
    FILES_DIR = os.path.join(BASE_DIR, "files")
    os.makedirs(FILES_DIR, exist_ok=True)

    INPUT_FILE = os.path.join(FILES_DIR, "audio_test.ogg")
    ENCRYPTED_JSON = os.path.join(FILES_DIR, "audio_test_secure.json")
    DECRYPTED_FILE = os.path.join(FILES_DIR, "audio_test_decrypted.ogg")

    if not os.path.exists(INPUT_FILE):
        print(f"❌ Fichier introuvable : {INPUT_FILE}")
        return

    # Supprimer le fichier déchiffré existant pour éviter les erreurs de permissions
    if os.path.exists(DECRYPTED_FILE):
        os.remove(DECRYPTED_FILE)

    # -----------------------------
    # 3️⃣ Chiffrement + Signature
    # -----------------------------
    print("\n📦 Chiffrement et signature du fichier...")
    try:
        json_path = secure_file_encrypt(
            infile_path=INPUT_FILE,
            aes_key=aes_key,
            sender_private_key=sender_private_key,
            outfile_json=ENCRYPTED_JSON
        )
        print(f"\n✅ Fichier chiffré et sauvegardé dans : {ENCRYPTED_JSON}")
    except Exception as e:
        print(f"❌ Erreur lors du chiffrement: {e}")
        return

    # -----------------------------
    # 4️⃣ Déchiffrement + Vérification
    # -----------------------------
    print("\n📂 Déchiffrement et vérification...")
    try:
        signature_valid = secure_file_decrypt(
            infile_json=json_path,
            aes_key=aes_key,
            sender_public_key=sender_public_key,
            output_path=DECRYPTED_FILE
        )
        print(f"\n✅ Fichier déchiffré sauvegardé dans : {DECRYPTED_FILE}")
    except Exception as e:
        print(f"❌ Erreur lors du déchiffrement: {e}")
        return

    # -----------------------------
    # 5️⃣ Vérification finale du contenu
    # -----------------------------
    print("\n🧪 Comparaison du fichier original et déchiffré...")
    with open(INPUT_FILE, "rb") as f_original, open(DECRYPTED_FILE, "rb") as f_decrypted:
        if f_original.read() == f_decrypted.read():
            print("✅ SUCCESS : le fichier déchiffré est IDENTIQUE à l'original")
        else:
            print("❌ ERROR : le contenu du fichier est différent")

    print("\n🔎 Signature valide :", signature_valid)

    # -----------------------------
    # 6️⃣ Lecture automatique du fichier audio
    # -----------------------------
    try:
        print("\n🔊 Lecture du fichier audio déchiffré...")
        if sys.platform == "win32":
            os.startfile(DECRYPTED_FILE)
        elif sys.platform == "darwin":  # macOS
            subprocess.run(["open", DECRYPTED_FILE])
        else:  # Linux
            subprocess.run(["xdg-open", DECRYPTED_FILE])
    except Exception as e:
        print(f"❌ Impossible de lire le fichier audio automatiquement: {e}")

    print("\n===== FIN DU TEST =====")


if __name__ == "__main__":
    main()
