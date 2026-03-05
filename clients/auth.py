import bcrypt

# def hash_password(password):
#     hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
    
#     return hash_password

def authentication():
    username = str(input('Entrer votre identifiant: '))
    password = str(input('Entrer votre mot de passe'))

    return username, password