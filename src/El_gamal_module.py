from Crypto.PublicKey import ElGamal
from Crypto import Random
from Crypto.Util.number import bytes_to_long, long_to_bytes
import json
import hashlib

def generate_keypair(bits=256):

    key = ElGamal.generate(bits, Random.get_random_bytes)

    public = {
        "p": key.p,
        "g": key.g,
        "y": key.y
    }

    private = {
        "p": key.p,
        "g": key.g,
        "x": key.x
    }

    return public, private



def save_keys(prefix, public, private):
    # Convertir tous les nombres en int standard avant JSON
    public_json = {k: int(v) for k, v in public.items()}
    private_json = {k: int(v) for k, v in private.items()}

    with open(f"{prefix}_public.json", "w") as f:
        json.dump(public_json, f)

    with open(f"{prefix}_private.json", "w") as f:
        json.dump(private_json, f)


def load_keys(prefix):

    with open(f"{prefix}_public.json", "r") as f:
        pub = json.load(f)

    with open(f"{prefix}_private.json", "r") as f:
        priv = json.load(f)

    return pub, priv


def encrypt_aes_key(aes_key_bytes, public):

    m = bytes_to_long(aes_key_bytes)

    p = public["p"]
    g = public["g"]
    y = public["y"]

    k = Random.random.StrongRandom().randint(1, p - 2)

    a = pow(g, k, p)
    b = (pow(y, k, p) * m) % p

    return {"a": a, "b": b}



def decrypt_aes_key(cipher, private):
    a = cipher["a"]
    b = cipher["b"]

    p = private["p"]
    x = private["x"]


    s = pow(a, x, p)
    s_inv = pow(s, -1, p)

    m = (b * s_inv) % p

    return long_to_bytes(m)
