import socket, json
from clients.crypto import generate_session_key, encrypt_session_key 

# HOST, PORT = "localhost", 9999

def server_connection(HOST, PORT):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((HOST, PORT))

    response_json = client.recv(1024).decode()

    response_dict = json.loads(response_json)

    data = response_dict["data"]

    # print(data)


