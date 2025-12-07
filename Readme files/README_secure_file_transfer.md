# Secure File Transfer - Tâche 2.3

Ce module permet de **transférer des fichiers de façon sécurisée** en utilisant :

- **AES-GCM** pour le chiffrement des fichiers
- **ElGamal** pour signer les fichiers et garantir leur intégrité

## Fonctions principales

### envoyer_fichier_secure(aes_key, fichier_path, private_key, public_key_receiver)
- Chiffre le fichier
- Génère la signature du fichier
- Retourne un paquet JSON à envoyer

### recevoir_fichier_secure(aes_key, paquet, public_key_sender, sortie_path)
- Vérifie la signature
- Déchiffre le fichier
- Sauvegarde le fichier original

## Exemple d'utilisation

```python
from src.El_gamal_module import generate_keypair, encrypt_aes_key, decrypt_aes_key
from src.aes_module import generate_aes_key
from secure_file_transfer import envoyer_fichier_secure, recevoir_fichier_secure

# Clés de l'expéditeur et du destinataire
public_sender, private_sender = generate_keypair()
public_receiver, private_receiver = generate_keypair()

# Clé AES pour la session
session_key = generate_aes_key()
encrypted_aes_key = encrypt_aes_key(session_key, public_receiver)
session_key_receiver = decrypt_aes_key(encrypted_aes_key, private_receiver)

# Envoi et réception sécurisés
paquet = envoyer_fichier_secure(session_key, "exemple.pdf", private_sender, public_receiver)
recevoir_fichier_secure(session_key_receiver, paquet, public_sender, "exemple_dechiffre.pdf")
