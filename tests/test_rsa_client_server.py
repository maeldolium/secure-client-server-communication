import unittest
import sys
from pathlib import Path

# Ensure project root is importable when pytest runs from tests/
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from clients.crypto import encrypt_session_key, generate_session_key
from server.crypto import CryptoManager


class TestRSAClientServerFlow(unittest.TestCase):
    def test_session_key_roundtrip_client_to_server(self):
        # Cote client: generation et chiffrement de la session key
        session_key_original = generate_session_key()
        server_crypto = CryptoManager()
        public_key_pem = server_crypto.export_public_key().decode()
        encrypted_session_key = encrypt_session_key(session_key_original, public_key_pem)

        # Cote serveur: dechiffrement de la session key
        session_key_decrypted = server_crypto.decrypt_session_key(encrypted_session_key)

        # Verification finale
        are_equal = session_key_original == session_key_decrypted
        print(are_equal)
        self.assertTrue(are_equal)


if __name__ == "__main__":
    unittest.main()