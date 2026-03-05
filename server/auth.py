import bcrypt
from hashlib import sha256
import json
import os.path

def load_users():
    if os.path.exists("config/users.json"):
        with open("config/users.json", 'r') as file:
            users = json.load(file)
    else:
        with open("config/users.json", "x") as file:
            json.dump([], file, indent=4)
        with open("config/users.json", "r") as file:
            users = json.load(file)
    
    return users


def hash_password(password):

    password = password.encode()

    hashed = sha256(password)

    hashed = hashed.hexdigest()

    return hashed

def verify_password(hashed, stored_hash):

    if hashed == stored_hash:
        return True
    else:
        return False
    
def authentificate(username, password, users: dict):
    if username not in users:
        return False
    
    hashed = hash_password(password)

    stored_hash = users[username]
    
    return verify_password(hashed, stored_hash)

    
