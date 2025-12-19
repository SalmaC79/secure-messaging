# Documentation : secure_file_transfer.py

## 1. Introduction

Le module `secure_file_transfer.py` permet de sécuriser le transfert de fichiers en combinant le chiffrement symétrique AES et la signature asymétrique ElGamal.  
Il garantit :
- **Confidentialité** : le contenu du fichier est chiffré avec AES.
- **Authenticité et intégrité** : le hash du fichier est signé avec ElGamal pour vérifier que le fichier n’a pas été modifié et provient bien de l’expéditeur.

Ce module est conçu pour fonctionner avec **tout type de fichiers** : texte, image, audio, vidéo, etc.

---

## 2. Prérequis

- Python ≥ 3.10
- Modules nécessaires :
  - `aes_module` : fonctions `encrypt_message` et `decrypt_message`
  - `file_module` : fonctions `encrypt_file`, `decrypt_file`, `save_encrypted_file`, `load_encrypted_file`
  - `El_gamal_module` : génération de clés ElGamal (`generate_keypair`)
  - `digital_signature_module` : signature et vérification (`sign`, `verify`)

---

## 3. Fonctionnalités

### 3.1 `secure_file_encrypt`
- **Description** : chiffre un fichier avec AES et signe son hash avec ElGamal.
- **Paramètres** :
  - `infile_path: str` → chemin du fichier à chiffrer
  - `aes_key: bytes` → clé AES
  - `sender_private_key: dict` → clé privée pour signer le fichier
  - `outfile_json: str` → chemin de sortie du fichier JSON
- **Retour** : chemin du fichier JSON créé
- **Actions** :
  1. Chiffrement AES du fichier
  2. Signature ElGamal du hash
  3. Sauvegarde dans un fichier JSON
  4. Affichage du contenu chiffré dans la console

### 3.2 `secure_file_decrypt`
- **Description** : déchiffre un fichier JSON et vérifie la signature.
- **Paramètres** :
  - `infile_json: str` → fichier JSON chiffré
  - `aes_key: bytes` → clé AES
  - `sender_public_key: dict` → clé publique pour vérification
  - `output_path: str` → chemin de sauvegarde du fichier déchiffré
- **Retour** : `True` si la signature est valide, sinon `False`
- **Actions** :
  1. Lecture du JSON
  2. Extraction et suppression de la signature du JSON
  3. Déchiffrement AES
  4. Vérification de la signature
  5. Sauvegarde du fichier déchiffré

---

## 4. Exemple d’utilisation

```python
from secure_file_transfer import secure_file_encrypt, secure_file_decrypt
from aes_module import generate_aes_key
from El_gamal_module import generate_keypair

# Génération des clés
public_key, private_key = generate_keypair("user_test")
aes_key = generate_aes_key()

# Chiffrement
json_path = secure_file_encrypt("files/exemple.txt", aes_key, private_key, "files/exemple_secure.json")

# Déchiffrement
is_valid = secure_file_decrypt(json_path, aes_key, public_key, "files/exemple_decrypted.txt")
print("Signature valide :", is_valid)
