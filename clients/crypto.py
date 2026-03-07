import secrets

def generate_session_key():
    key = secrets.token_bytes(32)

    return key