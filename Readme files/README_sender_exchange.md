# Sender Module
# Description

Ce script simule l’envoi d’une clé AES (clé de session) à un destinataire (receiver) en utilisant ElGamal pour le chiffrement.

Il fait partie du pipeline de messagerie sécurisée :

Le sender génère une clé AES (session).

La clé AES est chiffrée avec la clé publique ElGamal du receiver.

Le ciphertext est sauvegardé dans un fichier JSON, prêt à être envoyé.

Optionnel : la clé AES originale peut être sauvegardée localement pour test.

# Dépendances

Python 3.10+

PyCryptodome
 (Crypto package)

# Modules locaux :

El_gamal_module.py

aes_module.py

# Fichiers générés

cipher_aes_key.json : contient la clé AES chiffrée avec ElGamal

sender_session_key.bin (optionnel) : copie locale de la clé AES originale

# Utilisation

Assurez-vous que les clés ElGamal du receiver sont déjà générées et sauvegardées dans receiver_public.json et receiver_private.json.




Exemple de sortie :

Sender AES Key: db2599af13d5d30b1831148e3a9bb5150bfd42c43c599b10a7daac0bf914142c
Ciphertext sent → cipher_aes_key.json


Le fichier cipher_aes_key.json peut être envoyé au receiver pour déchiffrement.

# Notes

Le chiffrement de la clé AES est réalisé avec ElGamal, donc il est sécurisé pour l’échange de clés.

La clé AES est utilisée ensuite pour le chiffrement de messages ou fichiers via AES-GCM (Task 1.2).

Les nombres ElGamal sont convertis en string dans le fichier JSON pour compatibilité.