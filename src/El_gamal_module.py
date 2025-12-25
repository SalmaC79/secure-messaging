from Crypto.PublicKey import ElGamal
from Crypto import Random
from Crypto.Random import random
from Crypto.Util.number import bytes_to_long, long_to_bytes
from colorama import init, Fore, Back, Style
import json
import os

init(autoreset=True)
KEYS_DIR = "keys"


# ---------------------------------------------------------
# UTILITAIRE : chemin des fichiers
# ---------------------------------------------------------

def public_key_path(prefix):
    return os.path.join(KEYS_DIR, f"{prefix}_public.json")


def private_key_path(prefix):
    return os.path.join(KEYS_DIR, f"{prefix}_private.json")


# ---------------------------------------------------------
# UTILITAIRE : vérifier si les clés existent
# ---------------------------------------------------------

def keys_exist(prefix):
    """
    Vérifie si les clés ElGamal existent déjà pour un utilisateur
    """
    return (
        os.path.exists(public_key_path(prefix)) and
        os.path.exists(private_key_path(prefix))
    )


# ---------------------------------------------------------
# GENERATION DES CLES (avec vérification)
# ---------------------------------------------------------

def generate_keypair(prefix, bits=256):
    """
    Génère les clés ElGamal seulement si elles n'existent pas déjà.
    """
    os.makedirs(KEYS_DIR, exist_ok=True)

    if keys_exist(prefix):
        #print(Style.DIM +f"✔ Keys already exist for user '{prefix}'. Loading keys.")
        return load_keys(prefix)

    print(Style.BRIGHT+f"\n🔐 Generating ElGamal keys for user '{prefix}'...")

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
    print(Style.DIM +f"✔ Keys generated and saved for user '{prefix}'")

    return public, private


# ---------------------------------------------------------
# SAUVEGARDE DES CLES
# ---------------------------------------------------------

def save_keys(prefix, public, private):
    """
    Sauvegarde les clés ElGamal en JSON dans le dossier 'keys'
    """
    os.makedirs(KEYS_DIR, exist_ok=True)

    with open(public_key_path(prefix), "w") as f:
        json.dump(public, f, indent=4)

    with open(private_key_path(prefix), "w") as f:
        json.dump(private, f, indent=4)


# ---------------------------------------------------------
# CHARGEMENT DES CLES
# ---------------------------------------------------------

def load_keys(prefix):
    """
    Charge les clés ElGamal depuis le dossier 'keys'
    """
    if not keys_exist(prefix):
        raise FileNotFoundError(f"❌ No keys found for user '{prefix}'")

    with open(public_key_path(prefix), "r") as f:
        pub = json.load(f)

    with open(private_key_path(prefix), "r") as f:
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

    p = public["p"]
    g = public["g"]
    y = public["y"]

    # k = Random.StrongRandom().randint(1, p - 2)
    k = random.randint(1, p - 2)


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

    p = private["p"]
    x = private["x"]

    s = pow(a, x, p)
    s_inv = pow(s, -1, p)

    m = (b * s_inv) % p

    return long_to_bytes(m)
