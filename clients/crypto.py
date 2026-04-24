import secrets
import os.path
import json
import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes 
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.exceptions import InvalidTag


def generate_session_key():
    session_key = secrets.token_bytes(32)

    return session_key

def load_public_pem_key(key_pem):
    key_pem = key_pem.encode()

    public_key = serialization.load_pem_public_key(key_pem)
    
    return public_key

def encrypt_session_key(session_key, public_key_pem):
    public_key = load_public_pem_key(public_key_pem)

    encrypted_key = public_key.encrypt(
        session_key,
        padding.OAEP(
            mgf = padding.MGF1(algorithm=hashes.SHA256()),
            algorithm = hashes.SHA256(),
            label = None
        )
    )

    encrypted_key = base64.b64encode(encrypted_key).decode()

    return encrypted_key

def generate_nonce():
    nonce = secrets.token_bytes(12)

    return nonce

def encrypt_message(message, session_key):
    data = message.encode("utf-8")

    nonce = generate_nonce()

    cipher = Cipher(
        algorithms.AES(session_key),
        modes.GCM(nonce)
    )

    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(data) + encryptor.finalize()

    tag = encryptor.tag

    payload_dict = {
        "nonce_b64" : base64.b64encode(nonce).decode("utf-8"),
        "ciphertext_b64" : base64.b64encode(ciphertext).decode("utf-8"),
        "tag_b64": base64.b64encode(tag).decode("utf-8")
    }

    payload_json = json.dumps(payload_dict)
    return payload_json

def decrypt_message(payload_json, session_key):
    payload_dict = json.loads(payload_json)

    nonce = base64.b64decode(payload_dict["nonce_b64"])
    ciphertext = base64.b64decode(payload_dict["ciphertext_b64"])
    tag = base64.b64decode(payload_dict["tag_b64"])

    cipher = Cipher(
        algorithms.AES(session_key),
        modes.GCM(nonce, tag)
    )

    decryptor = cipher.decryptor()

    try:
        decrypted_message = decryptor.update(ciphertext) + decryptor.finalize()
    except InvalidTag:
        print("Tag invalide.")

    return decrypted_message.decode("utf-8")


if __name__ == "__main__":
    session_key = generate_session_key()
    payload_json = encrypt_message("bonjour", session_key)
    print(payload_json)

    print(decrypt_message(payload_json, session_key))