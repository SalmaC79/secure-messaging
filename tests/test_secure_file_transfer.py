import unittest
import os
from src.aes_module import generate_aes_key
from src.secure_file_transfer import envoyer_fichier_secure, recevoir_fichier_secure

# ---------------------------
# Mock des signatures pour le test
# ---------------------------
def fake_sign(file_path, private_key, data_type):
    return b"fake_signature"

def fake_verify(file_path, signature, public_key, data_type):
    return True  # Toujours valide pour le test

# Patch les fonctions du module pendant le test
import src.secure_file_transfer as sft
sft.sign = fake_sign
sft.verify = fake_verify

class TestSecureFileTransfer(unittest.TestCase):

    def setUp(self):
        # Fichier de test
        self.test_file = "test.txt"
        with open(self.test_file, "w") as f:
            f.write("Ceci est un fichier de test pour la transmission sécurisée.")

        # Clé AES pour le test
        self.aes_key = generate_aes_key()

        # Clés fictives pour test (bytes ok car mock)
        self.sender_private_key = b"fake_private_key"
        self.receiver_public_key = b"fake_public_key"

    def tearDown(self):
        # Supprimer les fichiers de test créés
        for f in ["test.txt", "test_dechiffre.txt"]:
            if os.path.exists(f):
                os.remove(f)

    def test_envoi_reception_fichier(self):
        # Envoyer et recevoir le fichier
        paquet = envoyer_fichier_secure(
            self.aes_key,
            self.test_file,
            self.sender_private_key,
            self.receiver_public_key
        )
        recevoir_fichier_secure(
            self.aes_key,
            paquet,
            self.sender_private_key,  # juste pour le test
            "test_dechiffre.txt"
        )

        # Vérifier que le fichier déchiffré est identique à l'original
        with open(self.test_file, "r") as f:
            original = f.read()
        with open("test_dechiffre.txt", "r") as f:
            dechiffre = f.read()

        self.assertEqual(original, dechiffre, "Le fichier déchiffré doit être identique à l'original")

if __name__ == "__main__":
    unittest.main()
