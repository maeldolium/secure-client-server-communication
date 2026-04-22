import secrets
import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import padding, hashes


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


