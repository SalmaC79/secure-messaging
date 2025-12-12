import os
import math
# BASE_DIR = os.path.dirname(__file__)       # /project/tests
# SRC_PATH = os.path.abspath(os.path.join(BASE_DIR, ".."))  # /project
from hash_module import hash_message, hash_file
from Crypto.PublicKey import ElGamal
from Crypto.Random.random import randint




def sign(data, private_key, data_type=None, algorithm="SHA-256"):
    # --- Auto-detect type ---
    if data_type is None:
        if isinstance(data, str) and os.path.isfile(data):
            data_type = "file"
        else:
            data_type = "message"

    # --- Hash the data ---
    if data_type == "file":
        digest = hash_file(data)
    elif data_type == "message":
        digest = hash_message(data)
    else:
        raise ValueError("data_type must be 'message' or 'file'")

    # Convert digest to integer for ElGamal signing
    digest_int = int(digest, 16)

    # ElGamal parameters (cast to int!)
    p = int(private_key.p)
    g = int(private_key.g)
    x = int(private_key.x)

    # Generate k coprime with p−1
    while True:
        k = randint(1, p - 2)
        if math.gcd(k, p - 1) == 1:
            break

    r = pow(g, k, p)
    k_inv = pow(k, -1, p-1)
    s = (k_inv * (digest_int - x * r)) % (p-1)

    signature = {
        "r": r,
        "s": s,
        "hash": digest,
        "algorithm": algorithm,
        "data_type": data_type
    }

    return signature



def verify(data, signature, public_key, data_type=None):
    # --- Auto-detect type ---
    if data_type is None:
        if isinstance(data, str) and os.path.isfile(data):
            data_type = "file"
        else:
            data_type = "message"

    # --- Hash the data again ---
    if data_type == "file":
        digest = hash_file(data)
    elif data_type == "message":
        digest = hash_message(data)
    else:
        raise ValueError("data_type must be 'message' or 'file'")

    digest_int = int(digest, 16)

    # --- Extract signature ---
    r = signature["r"]
    s = signature["s"]

    # --- Public key components ---
    p = int(public_key.p)
    g = int(public_key.g)
    y = int(public_key.y)

    # --- ElGamal verification ---
    if not (1 < r < p):
        return False

    left = (pow(y, r, p) * pow(r, s, p)) % p
    right = pow(g, digest_int, p)

    return left == right
