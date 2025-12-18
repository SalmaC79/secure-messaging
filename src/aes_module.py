import json
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# ----------------------
# Custom Exceptions
# ----------------------
class DecryptionError(Exception):
    """Raised when AES decryption fails (authentication error)"""
    pass

# ----------------------
# AES Key Generation
# ----------------------
def generate_aes_key(bits: int = 256) -> bytes:
    """
    Generate a 256-bit AES key (32 bytes)
    """
    return get_random_bytes(bits // 8)

# ----------------------
# AES-GCM Encryption
# ----------------------
def encrypt_message(aes_key: bytes, plaintext: bytes, aad: bytes = None) -> dict:
    """
    Encrypt a plaintext message using AES-GCM.

    Args:
        aes_key: 32-byte AES key
        plaintext: bytes to encrypt
        aad: optional additional authenticated data

    Returns:
        dict: {'nonce': bytes, 'ciphertext': bytes, 'tag': bytes}
    """
    nonce = get_random_bytes(12)
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    if aad:
        cipher.update(aad)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    return {'nonce': nonce, 'ciphertext': ciphertext, 'tag': tag}

# ----------------------
# AES-GCM Decryption
# ----------------------
def decrypt_message(aes_key: bytes, nonce: bytes, ciphertext: bytes, tag: bytes, aad: bytes = None) -> bytes:
    """
    Decrypt AES-GCM encrypted message.

    Raises:
        DecryptionError if authentication fails
    """
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    if aad:
        cipher.update(aad)
    try:
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext
    except ValueError:
        raise DecryptionError("AES decryption/authentication failed")

# ----------------------
# JSON / Base64 Serialization Helpers
# ----------------------
def serialize_encrypted_message(enc_dict: dict) -> str:
    """
    Convert encrypted message dict to JSON string with base64 fields.
    """
    json_dict = {k: base64.b64encode(v).decode('utf-8') for k, v in enc_dict.items()}
    return json.dumps(json_dict)

def deserialize_encrypted_message(json_str: str) -> dict:
    """
    Convert JSON string with base64 fields back to bytes dict.
    """
    json_dict = json.loads(json_str)
    return {k: base64.b64decode(v) for k, v in json_dict.items()}

# ----------------------
# File Encryption Skeleton
# ----------------------
def encrypt_file(aes_key: bytes, infile_path: str, chunk_size: int = 1024*1024) -> list:
    """
    Skeleton for encrypting a file in chunks.
    Returns a list of encrypted chunks (each dict has nonce, ciphertext, tag)
    """
    encrypted_chunks = []
    with open(infile_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            encrypted_chunks.append(encrypt_message(aes_key, chunk))
    return encrypted_chunks

# ----------------------
# File Decryption Skeleton
# ----------------------
def decrypt_file(aes_key: bytes, encrypted_chunks: list, outfile_path: str):
    """
    Skeleton for decrypting encrypted file chunks
    """
    with open(outfile_path, 'wb') as f:
        for chunk_dict in encrypted_chunks:
            plaintext = decrypt_message(
                aes_key,
                chunk_dict['nonce'],
                chunk_dict['ciphertext'],
                chunk_dict['tag']
            )
            f.write(plaintext)

# ----------------------
# Example Usage
# ----------------------
#activate it when needed (ila bghiti chi demo dial code kfch kaykhdm)
"""if __name__ == "__main__": 
    # Generate AES key
    key = generate_aes_key()
    print("Generated AES Key (hex):", key.hex())

    # Encrypt a simple message
    message = b"Hello, this is a test message."
    encrypted = encrypt_message(key, message)
    print("\nEncrypted (raw bytes):", {k: v.hex() for k, v in encrypted.items()})

    # Serialize to JSON (for sending over network)
    serialized = serialize_encrypted_message(encrypted)
    print("\nSerialized JSON:", serialized)

    # Deserialize and decrypt
    deserialized = deserialize_encrypted_message(serialized)
    decrypted = decrypt_message(
        key, deserialized['nonce'], deserialized['ciphertext'], deserialized['tag']
    )
    print("\nDecrypted message:", decrypted.decode())
"""
    # Optional: file encryption/decryption skeleton usage
    # encrypted_chunks = encrypt_file(key, "example.txt")
    # decrypt_file(key, encrypted_chunks, "example_decrypted.txt")
