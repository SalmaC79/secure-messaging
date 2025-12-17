# Secure Messaging Module

This module provides high-level functions for **securely sending and receiving messages or files** using your cryptographic modules:

* **AES-GCM** for symmetric encryption (`aes_module.py`)
* **ElGamal** for AES key encryption (`El_gamal_module.py`)
* **Digital signatures** for authenticity (`digital_signature_module.py`)

The module **encrypts, signs, decrypts, and verifies** messages or files in a simple and unified way.

---

## Functions

### `secure_encrypt(data, aes_key, sender_private_key, receiver_public_key, data_type="message")`

Encrypts and signs a message or a file.

**Parameters:**

* `data` — message string or file path
* `aes_key` — AES key to use for encryption
* `sender_private_key` — sender’s ElGamal private key (used for signing)
* `receiver_public_key` — receiver’s ElGamal public key (used to encrypt AES key)
* `data_type` — `"message"` or `"file"` (default: `"message"`)

**Process:**

1. Converts `data` to bytes
2. Encrypts the data using **AES-GCM**
3. Encrypts the AES key using **ElGamal public key**
4. Signs the original data using **ElGamal private key**
5. Returns a dictionary containing:

   * `ciphertext` — encrypted data (hex)
   * `nonce` — AES-GCM nonce (hex)
   * `tag` — AES-GCM authentication tag (hex)
   * `aes_key_enc` — AES key encrypted with ElGamal
   * `signature` — digital signature
   * `data_type` — type of data (`"message"` or `"file"`)

---

### `secure_decrypt(package, receiver_private_key, sender_public_key)`

Decrypts a package created by `secure_encrypt` and verifies its authenticity.

**Parameters:**

* `package` — dictionary returned by `secure_encrypt`
* `receiver_private_key` — receiver’s ElGamal private key
* `sender_public_key` — sender’s ElGamal public key (for signature verification)

**Process:**

1. Decrypts the AES key using the **receiver’s private key**
2. Converts hex fields (`ciphertext`, `nonce`, `tag`) back to bytes
3. Decrypts the AES-GCM ciphertext
4. Restores data as a string (message) or bytes (file)
5. Verifies the digital signature
6. Returns a tuple:

   * `data` — decrypted message or file bytes
   * `valid` — `True` if signature is valid, otherwise `False`

---

## Dependencies

This module depends on the following project modules:

* `aes_module.py` — AES-GCM encryption/decryption
* `El_gamal_module.py` — ElGamal key generation, encryption, decryption
* `digital_signature_module.py` — Signing and verification

All modules must be present in the same project.

---