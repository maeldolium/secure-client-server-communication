from crypto import CryptoManager

crypto = CryptoManager()

public_key = crypto.export_public_key()

print(public_key)