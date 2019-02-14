from Crypto.Hash import SHA256
import pylite.ms as ms


def create_login_table():
    ms.exec('CREATE auth WITH username password')
    

def add_user(username, password):
    password = SHA256.new( data=bytes(password, 'ascii') ).hexdigest()
    ms.exec(f'ADD {username} {password} TO auth')
    

def check_creds(username, password):
    password = SHA256.new( data=bytes(password, 'ascii') ).hexdigest()
    real_password = list( ms.exec(f'GET password WHERE username={username} FROM auth') )[0]
    return password == real_password
    
    
def remove_user(username):
    ms.exec(f'REMOVE username={username} FROM auth')
    