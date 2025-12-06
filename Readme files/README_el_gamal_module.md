# ElGamal Key Module

Ce module Python implémente le chiffrement **ElGamal** pour générer, sauvegarder, charger, chiffrer et déchiffrer des clés AES dans un projet de messagerie sécurisée.

## 📌 Fonctionnalités

1. **Génération de clés ElGamal**

```python
public, private = generate_keypair(bits=2048)
```

* `public` : dictionnaire `{p, g, y}`
* `private` : dictionnaire `{p, g, x}`

2. **Sauvegarde des clés**

```python
save_keys('alice', public, private)
```

* Sauvegarde les clés en fichiers JSON : `alice_public.json` et `alice_private.json`

3. **Chargement des clés**

```python
public, private = load_keys('alice')
```

4. **Chiffrement d'une clé AES**

```python
cipher = encrypt_aes_key(aes_key_bytes, public)
```

* AES key (bytes) -> ciphertext `{a, b}`

5. **Déchiffrement d'une clé AES**

```python
aes_key_bytes = decrypt_aes_key(cipher, private)
```

* Retourne la clé AES d'origine

## ⚙️ Installation

1. Installer Python 3.9+
2. Installer PyCryptodome :

```bash
pip install pycryptodome
```

## 📝 Exemple d'utilisation

```python
from elgamal_module import generate_keypair, save_keys, load_keys, encrypt_aes_key, decrypt_aes_key
from Crypto.Random import get_random_bytes

# Générer des clés
public, private = generate_keypair()
save_keys('alice', public, private)

# Charger les clés
public, private = load_keys('alice')

# Générer une clé AES
aes_key = get_random_bytes(16)

# Chiffrer la clé AES
cipher = encrypt_aes_key(aes_key, public)

# Déchiffrer la clé AES
recovered_key = decrypt_aes_key(cipher, private)
print('Clé AES récupérée identique :', recovered_key == aes_key)
```

## 📚 Notes

* Les clés ElGamal sont stockées en JSON pour faciliter la gestion et le partage dans GitHub.
* La taille recommandée du prime `p` est de 2048 bits.
* Ce module est destiné à un usage pédagogique et de projet, **pas pour un usage en production**.
* Sert de base au module AES pour l’échange sécurisé des clés.

## 🔐 Licence

MIT (ou licence définie par le projet)
