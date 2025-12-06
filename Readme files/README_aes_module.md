<<<<<<< HEAD
## Overview

This module provides AES-256 GCM encryption and decryption for messages and files, with authenticated encryption and JSON serialization.
---

## Functions

### 1. `generate_aes_key() -> bytes`

Generate a random 256-bit AES key.

```python
from aes_module import generate_aes_key

aes_key = generate_aes_key()
```

---

### 2. `encrypt_message(aes_key: bytes, plaintext: bytes, aad: bytes = None) -> dict`

Encrypt a plaintext message using AES-GCM.

* Returns a dictionary with: `nonce`, `ciphertext`, `tag` (all bytes)
* Optional `aad` for additional authenticated data

```python
from aes_module import encrypt_message

encrypted = encrypt_message(aes_key, b"Hello, World!")
```

---

### 3. `decrypt_message(aes_key: bytes, nonce: bytes, ciphertext: bytes, tag: bytes, aad: bytes = None) -> bytes`

Decrypt an AES-GCM encrypted message.

* Raises `DecryptionError` if authentication fails.

```python
from aes_module import decrypt_message, DecryptionError

try:
    plaintext = decrypt_message(aes_key, encrypted['nonce'], encrypted['ciphertext'], encrypted['tag'])
    print(plaintext.decode())
except DecryptionError:
    print("Decryption failed or message was tampered")
```

---

### 4. `serialize_encrypted_message(enc_dict: dict) -> str`

Convert an encrypted message dict to JSON with base64 fields, ready for transport.

```python
from aes_module import serialize_encrypted_message

json_str = serialize_encrypted_message(encrypted)
```

---

### 5. `deserialize_encrypted_message(json_str: str) -> dict`

Convert JSON string back to bytes dict for decryption.

```python
from aes_module import deserialize_encrypted_message

encrypted_bytes = deserialize_encrypted_message(json_str)
```

---

### 6. File encryption/decryption (skeleton)

* `encrypt_file(aes_key: bytes, infile_path: str) -> list` → encrypts a file in chunks; returns list of encrypted dicts
* `decrypt_file(aes_key: bytes, encrypted_chunks: list, outfile_path: str)` → decrypts chunks and writes to file

> Full file integration can be implemented by Member 3 using these functions.

---

## Message / File Flow

**Sender:**

1. Encrypt message/file using AES
2. Serialize to JSON for transport
3. Send JSON + AES key encrypted via ElGamal

**Receiver:**

1. Decrypt AES key using ElGamal
2. Deserialize JSON message/file
3. Decrypt using AES module

---

## **Exceptions**

* `DecryptionError` → raised if AES decryption fails (wrong key or tampered data)

---

## **Example Usage**

```python
from aes_module import generate_aes_key, encrypt_message, decrypt_message, serialize_encrypted_message, deserialize_encrypted_message

# 1. Generate AES key
key = generate_aes_key()

# 2. Encrypt a message
message = b"Hello team!"
encrypted = encrypt_message(key, message)

# 3. Serialize for sending
json_message = serialize_encrypted_message(encrypted)

# 4. Deserialize on receiver
received = deserialize_encrypted_message(json_message)

# 5. Decrypt
plaintext = decrypt_message(key, received['nonce'], received['ciphertext'], received['tag'])
print("Decrypted message:", plaintext.decode())
```

---
**BEWARE**

* Always **serialize before sending** and **deserialize before decrypting**.
* Handle `DecryptionError` in GUI or CLI.
* The AES key comes from the **ElGamal key exchange** managed by Member 1.
* Can be used for **messages or files**.
---
=======
# secure-messaging
>>>>>>> ed2b204da22b3bf54f83db6fdbcb5afabf7c9fe2
