import unittest
import os
from src.aes_module import generate_aes_key
from src.file_module import (
    encrypt_file,
    decrypt_file,
    save_encrypted_file,
    load_encrypted_file
)

class TestFileModule(unittest.TestCase):

    def setUp(self):
        # Création d'un fichier de test
        self.test_filename = "fichier_test.txt"
        with open(self.test_filename, "w") as f:
            f.write("Ceci est un fichier de test pour le chiffrement.\n" * 5)

        self.aes_key = generate_aes_key()
        self.json_output = "fichier_chiffre.json"
        self.decrypted_output = "fichier_dechiffre.txt"

    def tearDown(self):
        # Nettoyage après les tests
        for file in [self.test_filename, self.json_output, self.decrypted_output]:
            if os.path.exists(file):
                os.remove(file)

    def test_chiffrement_fichier(self):
        enc = encrypt_file(self.aes_key, self.test_filename)
        self.assertIn("chunks", enc)
        self.assertGreater(len(enc["chunks"]), 0, "Le fichier doit générer au moins un chunk chiffré")

    def test_sauvegarde_et_chargement_json(self):
        enc = encrypt_file(self.aes_key, self.test_filename)
        save_encrypted_file(enc, self.json_output)

        self.assertTrue(os.path.exists(self.json_output), "Le fichier JSON doit être créé")

        loaded = load_encrypted_file(self.json_output)
        self.assertEqual(loaded["total_chunks"], len(enc["chunks"]))

    def test_cycle_complet(self):
        # Chiffrement
        enc = encrypt_file(self.aes_key, self.test_filename)
        save_encrypted_file(enc, self.json_output)

        # Chargement + déchiffrement
        loaded = load_encrypted_file(self.json_output)
        decrypt_file(self.aes_key, loaded, self.decrypted_output)

        # Comparaison des fichiers
        with open(self.test_filename, "rb") as f1, open(self.decrypted_output, "rb") as f2:
            self.assertEqual(f1.read(), f2.read(), "Le fichier déchiffré doit être identique à l'original")

if __name__ == "__main__":
    unittest.main()
