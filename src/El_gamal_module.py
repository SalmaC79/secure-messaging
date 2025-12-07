from Crypto.PublicKey import ElGamal
from Crypto import Random
from Crypto.Util.number import bytes_to_long, long_to_bytes
import json

# ---------------------------------------------------------
# GENERATION DES CLES
# ---------------------------------------------------------

def generate_keypair(bits=256):
    key = ElGamal.generate(bits, Random.get_random_bytes)

    public = {
        "p": int(key.p),
        "g": int(key.g),
        "y": int(key.y)
    }

    private = {
        "p": int(key.p),
        "g": int(key.g),
        "x": int(key.x)
    }

    return public, private


# ---------------------------------------------------------
# SAUVEGARDE & CHARGEMENT
# ---------------------------------------------------------

def save_keys(prefix, public, private):
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

    # Reconversion en int (JSON met en str)
    pub = {k: int(v) for k, v in pub.items()}
    priv = {k: int(v) for k, v in priv.items()}

    return pub, priv


# ---------------------------------------------------------
# CHIFFREMENT DE LA CLE AES
# ---------------------------------------------------------

def encrypt_aes_key(aes_key_bytes, public):

    m = bytes_to_long(aes_key_bytes)

    # ⚠ Conversion obligatoire (évite les erreurs BigNum)
    p = int(public["p"])
    g = int(public["g"])
    y = int(public["y"])

    k = Random.random.StrongRandom().randint(1, p - 2)

    a = pow(g, k, p)
    b = (pow(y, k, p) * m) % p

    return {"a": int(a), "b": int(b)}


# ---------------------------------------------------------
# DECHIFFREMENT DE LA CLE AES
# ---------------------------------------------------------

def decrypt_aes_key(cipher, private):
    a = int(cipher["a"])
    b = int(cipher["b"])

    # ⚠ Conversion obligatoire
    p = int(private["p"])
    x = int(private["x"])

    s = pow(a, x, p)
    s_inv = pow(int(s), -1, p)

    m = (b * s_inv) % p

    return long_to_bytes(m)
