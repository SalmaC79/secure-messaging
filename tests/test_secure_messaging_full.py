import sys
import os

# Add src/ folder to sys.path so imports work
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from secure_messaging_full import secure_encrypt, secure_decrypt
from El_gamal_module import generate_keypair

def test_basic_encryption_decryption():
    print("🔹 Testing secure messaging module...")

    # Generate ElGamal keypair for the receiver
    public_key, private_key = generate_keypair(256)

    # Message to test
    message = "This is a test message."

    # Encrypt
    package = secure_encrypt(message, public_key)
    print("Encryption OK ✔")

    # Decrypt
    recovered = secure_decrypt(package, private_key)
    print("Decryption OK ✔")

    # Validate
    if recovered == message:
        print("✅ Test passed: Plaintext matches!")
    else:
        print("❌ Test FAILED: Mismatch detected.")
        print("Original :", message)
        print("Recovered:", recovered)


if __name__ == "__main__":
    test_basic_encryption_decryption()
