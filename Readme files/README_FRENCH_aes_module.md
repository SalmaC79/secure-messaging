
---

# **secure-messaging / Module AES**

## Vue d’ensemble

Ce module fournit le chiffrement et déchiffrement **AES-256 GCM** pour les messages et fichiers, avec **authentification des données** et **sérialisation JSON**.

Il est **stateless, sécurisé et prêt pour l’intégration** dans le système de messagerie sécurisée.

---

## **Fonctions**

### 1. `generate_aes_key() -> bytes`

Génère une **clé AES aléatoire de 256 bits**.

```python
from aes_module import generate_aes_key

aes_key = generate_aes_key()
```

---

### 2. `encrypt_message(aes_key: bytes, plaintext: bytes, aad: bytes = None) -> dict`

Chiffre un message en clair avec AES-GCM.

* Retourne un dictionnaire : `nonce`, `ciphertext`, `tag` (tous en bytes)
* `aad` optionnel pour des données supplémentaires authentifiées

```python
from aes_module import encrypt_message

encrypted = encrypt_message(aes_key, b"Bonjour le monde !")
```

---

### 3. `decrypt_message(aes_key: bytes, nonce: bytes, ciphertext: bytes, tag: bytes, aad: bytes = None) -> bytes`

Déchiffre un message AES-GCM.

* Lève `DecryptionError` si l’authentification échoue.

```python
from aes_module import decrypt_message, DecryptionError

try:
    plaintext = decrypt_message(aes_key, encrypted['nonce'], encrypted['ciphertext'], encrypted['tag'])
    print(plaintext.decode())
except DecryptionError:
    print("Échec du déchiffrement ou message altéré")
```

---

### 4. `serialize_encrypted_message(enc_dict: dict) -> str`

Convertit le dictionnaire chiffré en **JSON avec base64**, prêt à être transmis.

```python
from aes_module import serialize_encrypted_message

json_str = serialize_encrypted_message(encrypted)
```

---

### 5. `deserialize_encrypted_message(json_str: str) -> dict`

Convertit une chaîne JSON en dictionnaire de bytes pour le déchiffrement.

```python
from aes_module import deserialize_encrypted_message

encrypted_bytes = deserialize_encrypted_message(json_str)
```

---

### 6. Chiffrement / déchiffrement de fichiers (squelette)

* `encrypt_file(aes_key: bytes, infile_path: str) -> list` → chiffre un fichier par blocs; retourne une liste de dictionnaires chiffrés
* `decrypt_file(aes_key: bytes, encrypted_chunks: list, outfile_path: str)` → déchiffre les blocs et écrit le fichier

> L’intégration complète pour les fichiers peut être réalisée par le membre 3 en utilisant ces fonctions.

---

## **Flux pour messages / fichiers**

**Expéditeur :**

1. Chiffre le message/fichier avec AES
2. Sérialise en JSON pour le transport
3. Envoie le JSON + la clé AES chiffrée via ElGamal

**Récepteur :**

1. Déchiffre la clé AES avec ElGamal
2. Désérialise le JSON du message/fichier
3. Déchiffre avec le module AES

---

## **Exceptions**

* `DecryptionError` → levée si le déchiffrement AES échoue (mauvaise clé ou données altérées)

---

## **Exemple d’utilisation**

```python
from aes_module import generate_aes_key, encrypt_message, decrypt_message, serialize_encrypted_message, deserialize_encrypted_message

# 1. Générer la clé AES
key = generate_aes_key()

# 2. Chiffrer un message
message = b"Bonjour équipe !"
encrypted = encrypt_message(key, message)

# 3. Sérialiser pour l’envoi
json_message = serialize_encrypted_message(encrypted)

# 4. Désérialiser côté récepteur
received = deserialize_encrypted_message(json_message)

# 5. Déchiffrer
plaintext = decrypt_message(key, received['nonce'], received['ciphertext'], received['tag'])
print("Message déchiffré :", plaintext.decode())
```

---
**ATTENTION !**

* Toujours **sérialiser avant l’envoi** et **désérialiser avant le déchiffrement**.
* Gérer `DecryptionError` dans l’interface graphique ou CLI.
* La clé AES provient de l’**échange de clés ElGamal** géré par le membre 1.
* Peut être utilisé pour les **messages et fichiers**.
---
