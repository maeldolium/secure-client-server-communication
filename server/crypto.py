from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import base64

class CryptoManager:

    def __init__(self):
        self.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key = self.private_key.public_key()
    
    def export_public_key(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    def decrypt_session_key(self, encrypted_session_key_b64):
        encrypted_session_key_bytes = base64.b64decode(encrypted_session_key_b64)

        decrypted_key = self.private_key.decrypt(
            encrypted_session_key_bytes,
            padding.OAEP(
                mgf = padding.MGF1(algorithm=hashes.SHA256()),
                algorithm = hashes.SHA256(),
                label = None
            ))
        
        return decrypted_key


    