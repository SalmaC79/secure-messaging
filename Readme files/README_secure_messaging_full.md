
---

# Secure Messaging Module

This module provides two high-level functions for secure message encryption and decryption using your existing cryptographic modules:

* **AES-GCM** (from `aes_module.py`)
* **ElGamal key encryption** (from `El_gamal_module.py`)
* **SHA-256 hashing** (from `hash_module.py`)

The goal is to offer a simple interface for securely sending and receiving encrypted messages.

---

## Functions

### `secure_encrypt(message, receiver_public_key)`

Encrypts a plaintext message.

* Generates a random AES key
* Hashes the message (SHA-256)
* Encrypts the message using AES-GCM
* Encrypts the AES key using ElGamal
* Returns a dictionary containing:

  * ciphertext (hex)
  * nonce (hex)
  * tag (hex)
  * encrypted AES key
  * message hash

#### Example:

```python
package = secure_encrypt("Hello", receiver_public_key)
```

---

### `secure_decrypt(package, receiver_private_key)`

Decrypts the package produced by `secure_encrypt`.

* Decrypts the AES key (ElGamal)
* Converts hex values back to bytes
* Decrypts AES-GCM ciphertext
* Verifies integrity using SHA-256

#### Example:

```python
plaintext = secure_decrypt(package, receiver_private_key)
```

---

## Demo

Running the file directly executes a demo showing:

* Key generation
* Encryption
* Decryption
* Message integrity check

Run:

```bash
python secure_messaging_full.py
```

---

## Requirements

This module depends on your own cryptographic modules:

* `aes_module.py`
* `El_gamal_module.py`
* `hash_module.py`

These must be present in the same project.

---

