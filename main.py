from server import auth as server_auth, logger
from clients import auth as client_auth
# from config import users

def main():

    users = server_auth.load_users()
    username, password = client_auth.authentication()

    if server_auth.authentificate(username, password, users) == False:
        print('Connexion échouée')
    else:
        print('Connecté')



main()