import base64
import json
from src.aes_module import encrypt_message, decrypt_message

def encrypt_file(aes_key: bytes, infile_path: str, chunk_size: int = 1024 * 1024) -> dict:
    """
    Chiffre un fichier par morceaux (chunks) avec AES-GCM.
    Retourne un dictionnaire contenant les morceaux chiffrés.
    """
    chunks = []

    with open(infile_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break

            enc = encrypt_message(aes_key, chunk)
            chunks.append({
                "nonce": base64.b64encode(enc["nonce"]).decode(),
                "ciphertext": base64.b64encode(enc["ciphertext"]).decode(),
                "tag": base64.b64encode(enc["tag"]).decode()
            })

    return {
        "filename": infile_path,
        "total_chunks": len(chunks),
        "chunks": chunks
    }


def save_encrypted_file(enc_dict: dict, outfile_json: str):
    """
    Sauvegarde la structure chiffrée dans un fichier JSON.
    """
    with open(outfile_json, "w") as f:
        json.dump(enc_dict, f, indent=4)


def load_encrypted_file(json_path: str) -> dict:
    """
    Charge un fichier JSON contenant les données chiffrées.
    """
    with open(json_path, "r") as f:
        return json.load(f)


def decrypt_file(aes_key: bytes, enc_dict: dict, output_path: str):
    """
    Déchiffre tous les morceaux et reconstruit le fichier original.
    """
    with open(output_path, "wb") as f:
        for chunk in enc_dict["chunks"]:
            nonce = base64.b64decode(chunk["nonce"])
            ciphertext = base64.b64decode(chunk["ciphertext"])
            tag = base64.b64decode(chunk["tag"])

            plaintext = decrypt_message(aes_key, nonce, ciphertext, tag)
            f.write(plaintext)
