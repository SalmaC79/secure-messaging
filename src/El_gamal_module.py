from Crypto.PublicKey import ElGamal
from Crypto import Random
from Crypto.Util.number import bytes_to_long, long_to_bytes
import json
import os

# ---------------------------------------------------------
# UTILITAIRE : vérifier si les clés existent
# ---------------------------------------------------------

def keys_exist(prefix):
    """
    Vérifie si les clés ElGamal existent déjà pour un utilisateur
    """
    return (
        os.path.exists(f"{prefix}_public.json") and
        os.path.exists(f"{prefix}_private.json")
    )


# ---------------------------------------------------------
# GENERATION DES CLES (avec vérification)
# ---------------------------------------------------------

def generate_keypair(prefix, bits=256):
    """
    Génère les clés ElGamal seulement si elles n'existent pas déjà.
    """
    if keys_exist(prefix):
        print(f"✔ Keys already exist for user '{prefix}'. Loading keys.")
        return load_keys(prefix)

    print(f"🔐 Generating ElGamal keys for user '{prefix}'...")

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

    save_keys(prefix, public, private)
    print(f"✔ Keys generated and saved for user '{prefix}'")

    return public, private


# ---------------------------------------------------------
# SAUVEGARDE DES CLES
# ---------------------------------------------------------

def save_keys(prefix, public, private):
    """
    Sauvegarde les clés ElGamal en JSON
    """
    with open(f"{prefix}_public.json", "w") as f:
        json.dump(public, f)

    with open(f"{prefix}_private.json", "w") as f:
        json.dump(private, f)


# ---------------------------------------------------------
# CHARGEMENT DES CLES
# ---------------------------------------------------------

def load_keys(prefix):
    """
    Charge les clés ElGamal depuis les fichiers JSON
    """
    if not keys_exist(prefix):
        raise FileNotFoundError(f"❌ No keys found for user '{prefix}'")

    with open(f"{prefix}_public.json", "r") as f:
        pub = json.load(f)

    with open(f"{prefix}_private.json", "r") as f:
        priv = json.load(f)

    # Reconversion en int
    pub = {k: int(v) for k, v in pub.items()}
    priv = {k: int(v) for k, v in priv.items()}

    return pub, priv


# ---------------------------------------------------------
# CHIFFREMENT DE LA CLE AES
# ---------------------------------------------------------

def encrypt_aes_key(aes_key_bytes, public):
    """
    Chiffre une clé AES avec la clé publique ElGamal
    """
    m = bytes_to_long(aes_key_bytes)

    p = int(public["p"])
    g = int(public["g"])
    y = int(public["y"])

    if m >= p:
        raise ValueError("❌ AES key too large for ElGamal modulus")

    k = Random.random.StrongRandom().randint(1, p - 2)

    a = pow(g, k, p)
    b = (pow(y, k, p) * m) % p

    return {"a": int(a), "b": int(b)}


# ---------------------------------------------------------
# DECHIFFREMENT DE LA CLE AES
# ---------------------------------------------------------

def decrypt_aes_key(cipher, private):
    """
    Déchiffre une clé AES chiffrée avec ElGamal
    """
    a = int(cipher["a"])
    b = int(cipher["b"])

    p = int(private["p"])
    x = int(private["x"])

    s = pow(a, x, p)
    s_inv = pow(s, -1, p)

    m = (b * s_inv) % p

    return long_to_bytes(m)
