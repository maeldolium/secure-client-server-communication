
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
