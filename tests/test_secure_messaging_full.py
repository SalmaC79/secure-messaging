import sys
import os

# Add src/ folder to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from secure_messaging_full import secure_encrypt, secure_decrypt
from aes_module import generate_aes_key
from El_gamal_module import generate_keypair

# Dummy wrapper for digital_signature_module
class KeyObject:
    def __init__(self, key_dict):
        self.p = key_dict["p"]
        self.g = key_dict["g"]
        self.x = key_dict.get("x", 0)
        self.y = key_dict.get("y", 0)

def test_secure_message():
    print("🔹 Testing secure messaging module...")

    # --- Generate ElGamal keypair for receiver and sender ---
    sender_pub_dict, sender_priv_dict = generate_keypair("sender", bits=256)
    receiver_pub_dict, receiver_priv_dict = generate_keypair("receiver", bits=256)

    # --- Wrap keys for digital signature module ---
    sender_priv_obj = KeyObject(sender_priv_dict)
    sender_pub_obj = KeyObject(sender_pub_dict)
    receiver_priv_obj = KeyObject(receiver_priv_dict)
    receiver_pub_obj = KeyObject(receiver_pub_dict)

    # --- AES key ---
    aes_key = generate_aes_key()

    # --- Message to encrypt ---
    message = "This is a secure test message."

    # --- Encrypt & sign ---
    package = secure_encrypt(
        data=message,
        aes_key=aes_key,
        sender_private_key=sender_priv_obj,   # signature needs KeyObject
        receiver_public_key=receiver_pub_dict,  # AES encryption needs dict
        data_type="message"
    )
    print("Encryption & signing OK ✔")

    # --- Decrypt & verify ---
    recovered, valid = secure_decrypt(
        package,
        receiver_private_key=receiver_priv_dict,  # AES decryption needs dict
        sender_public_key=sender_pub_obj          # signature verification needs KeyObject
    )
    print("Decryption & verification OK ✔")

    # --- Check ---
    print("\n--- TEST RESULTS ---")
    print("Original message : ", message)
    print("Recovered message: ", recovered)
    print("Signature valid  : ", valid)

    if recovered == message and valid:
        print("✅ Test PASSED")
    else:
        print("❌ Test FAILED")

if __name__ == "__main__":
    test_secure_message()
