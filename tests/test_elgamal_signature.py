from Crypto.PublicKey import ElGamal
from Crypto.Random import get_random_bytes
import sys
import os

BASE_DIR = os.path.dirname(__file__)       # /project/tests
SRC_PATH = os.path.abspath(os.path.join(BASE_DIR, ".."))  # /project

sys.path.append(SRC_PATH)

from src.digital_signature_module import sign, verify


def main():
    print("[+] Generating ElGamal key pair...")
    key = ElGamal.generate(256, get_random_bytes)

    private_key = key
    public_key = key.publickey()

    message = "Encrypted in the Chaos"

    print("[+] Signing message...")
    signature = sign(message, private_key)

    print("Signature:")
    print(signature)

    print("\n[+] Verifying correct message...")
    valid = verify(message, signature, public_key)
    print("Valid:", valid)

    print("\n[+] Verifying tampered message...")
    tampered_message = "Encrypted in the Chaos!!!"
    valid_tampered = verify(tampered_message, signature, public_key)
    print("Valid:", valid_tampered)

    assert valid is True
    assert valid_tampered is False

    print("\n✅ All tests passed!")


if __name__ == "__main__":
    main()
