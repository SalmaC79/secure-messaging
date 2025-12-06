import unittest
from aes_module import (
    generate_aes_key,
    encrypt_message,
    decrypt_message,
    serialize_encrypted_message,
    deserialize_encrypted_message,
    DecryptionError
)

class TestAESModule(unittest.TestCase):

    def test_encrypt_decrypt_message(self):
        key = generate_aes_key()
        plaintext = b"This is a secret message."

        # Encrypt
        encrypted = encrypt_message(key, plaintext)

        # Decrypt
        decrypted = decrypt_message(
            key,
            encrypted['nonce'],
            encrypted['ciphertext'],
            encrypted['tag']
        )

        self.assertEqual(decrypted, plaintext, "Decrypted message should match original")

    def test_serialization(self):
        key = generate_aes_key()
        plaintext = b"Serialize this message"

        encrypted = encrypt_message(key, plaintext)
        serialized = serialize_encrypted_message(encrypted)
        deserialized = deserialize_encrypted_message(serialized)

        decrypted = decrypt_message(
            key,
            deserialized['nonce'],
            deserialized['ciphertext'],
            deserialized['tag']
        )

        self.assertEqual(decrypted, plaintext, "Decrypted message after serialization should match")

    def test_wrong_key(self):
        key = generate_aes_key()
        wrong_key = generate_aes_key()
        plaintext = b"Secret"

        encrypted = encrypt_message(key, plaintext)

        with self.assertRaises(DecryptionError):
            decrypt_message(
                wrong_key,
                encrypted['nonce'],
                encrypted['ciphertext'],
                encrypted['tag']
            )

    def test_tampered_ciphertext(self):
        key = generate_aes_key()
        plaintext = b"Tamper test"
        encrypted = encrypt_message(key, plaintext)

        # Tamper the ciphertext
        tampered = encrypted.copy()
        tampered['ciphertext'] = b'\x00' * len(encrypted['ciphertext'])

        with self.assertRaises(DecryptionError):
            decrypt_message(
                key,
                tampered['nonce'],
                tampered['ciphertext'],
                tampered['tag']
            )

if __name__ == "__main__":
    unittest.main()
