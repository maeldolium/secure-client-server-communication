import socket, json
from server.crypto import CryptoManager

# HOST, PORT = "localhost", 9999

def network(HOST, PORT, public_key):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)

    while True:
        client, address = server.accept()

        public_key_dict = {
            "type" : "public_key",
            "data" : public_key.decode()
        }

        public_key_json = json.dumps(public_key_dict)

        client.sendall(public_key_json.encode())

        response = client.recv(1024).decode()

        session_key = json.loads(response)

        session_key = CryptoManager.decrypt_session_key(session_key)

        print("Clé de session reçue.")

        client.close()
        server.close()