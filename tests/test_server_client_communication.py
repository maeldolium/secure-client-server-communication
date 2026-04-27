
import unittest
import multiprocessing
import time
import sys
from pathlib import Path

# Ajoute le dossier racine du projet au sys.path pour les imports
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from server.crypto import CryptoManager
from server.network import network
from clients.network import server_connection

HOST, PORT = "localhost", 9999

class TestServerClientCommunication(unittest.TestCase):
    def test_session_key_exchange(self):
        """
        Test that the session key sent by the client is correctly received and decrypted by the server.
        """
        import socket
        import json
        import base64
        from clients.crypto import generate_session_key, encrypt_session_key

        # Variable partagée pour récupérer la clé de session côté serveur
        manager = multiprocessing.Manager()
        server_session_key = manager.list()

    def server_with_session_key(HOST, PORT, public_key, session_key_list):
        from server.crypto import CryptoManager
        import socket, json
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((HOST, PORT))
        server.listen(1)
        client, address = server.accept()
        public_key_dict = {
            "type": "public_key",
            "data": public_key.decode()
        }
        public_key_json = json.dumps(public_key_dict)
        client.sendall(public_key_json.encode())
        response = client.recv(4096).decode()
        encrypted_session_key_b64 = json.loads(response)
        crypto = CryptoManager()
        session_key = crypto.decrypt_session_key(encrypted_session_key_b64)
        session_key_list.append(session_key)
        client.close()
        server.close()

        crypto = CryptoManager()
        public_key = crypto.export_public_key()
        server_proc = multiprocessing.Process(target=server_with_session_key, args=(HOST, PORT, public_key, server_session_key))
        server_proc.start()
        time.sleep(0.5)

        try:
            # Client: reçoit la clé publique, génère et envoie la clé de session
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST, PORT))
            response_json = client.recv(4096).decode()
            response_dict = json.loads(response_json)
            received_pem = response_dict["data"]
            session_key = generate_session_key()
            encrypted_session_key = encrypt_session_key(session_key, received_pem)
            client.send(json.dumps(encrypted_session_key).encode())
            client.close()

            # Vérification côté serveur
            time.sleep(0.5)
            self.assertEqual(len(server_session_key), 1)
            self.assertEqual(server_session_key[0], session_key)
        finally:
            server_proc.terminate()
            server_proc.join()
    def test_public_key_exchange(self):
        # Setup server in a separate process
        crypto = CryptoManager()
        public_key = crypto.export_public_key()
        print("[SERVER] Public key sent:\n", public_key.decode())
        server_proc = multiprocessing.Process(target=network, args=(HOST, PORT, public_key))
        server_proc.start()
        time.sleep(0.5)  # Wait for server to start

        # Client connects and receives public key
        try:
            import socket
            import json
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((HOST, PORT))
            response_json = client.recv(4096).decode()
            response_dict = json.loads(response_json)
            received_pem = response_dict["data"]
            print("[CLIENT] Public key received:\n", received_pem)
            self.assertEqual(received_pem, public_key.decode())
        finally:
            server_proc.terminate()
            server_proc.join()

if __name__ == "__main__":
    unittest.main()
