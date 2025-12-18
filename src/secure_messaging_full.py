import os
from aes_module import encrypt_message, decrypt_message
from El_gamal_module import encrypt_aes_key, decrypt_aes_key
from digital_signature_module import sign, verify


# --------------------------------------------------
# Secure Encrypt
# --------------------------------------------------
def secure_encrypt(data, aes_key, sender_private_key, data_type="message"):
    """
    data: message string OR file path
    data_type: 'message' or 'file'
    """

    # --- Prepare raw bytes ---
    if data_type == "message":
        data_bytes = data.encode()
    else:
        raise ValueError("data_type must be 'message' or 'file'")

    # --- AES encrypt ---
    enc = encrypt_message(aes_key, data_bytes)


    # --- Sign original data ---
    signature = sign(data, sender_private_key, data_type=data_type)

    # --- Package everything ---
    package = {
        "data_type": data_type,
        "ciphertext": enc["ciphertext"].hex(),
        "nonce": enc["nonce"].hex(),
        "tag": enc["tag"].hex(),
        "signature": signature
    }

    return package


# --------------------------------------------------
# Secure Decrypt
# --------------------------------------------------
def secure_decrypt(package, aes_key, sender_public_key):

    # --- Decode AES fields ---
    ciphertext = bytes.fromhex(package["ciphertext"])
    nonce = bytes.fromhex(package["nonce"])
    tag = bytes.fromhex(package["tag"])

    # --- AES decrypt ---
    plaintext_bytes = decrypt_message(aes_key, nonce, ciphertext, tag)

    # --- Restore data ---
    if package["data_type"] == "message":
        data = plaintext_bytes.decode()
    else:
        data = plaintext_bytes  # file bytes

    # --- Verify signature ---
    valid = verify(
        data,
        package["signature"],
        sender_public_key,
        data_type=package["data_type"]
    )

    return data, valid
