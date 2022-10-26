import hashlib
import jwt
import time
from django.http import HttpResponse

def password_is_valid(password):
    if len(password)>15 or len(password)<5:
        return False
    return password.isalnum()

#encrtyped
def calc_md5(password):
    md5_obj = hashlib.md5()
    md5_obj.update(password.encode('utf-8'))
    return md5_obj.hexdigest()


def get_jwt_token(username):
    payload = {
        'exp': int(time.time()) + 60 * 180,
        'iat': int(time.time()),
        'data': {'username': username}
    }
    encoded_jwt = jwt.encode(payload, 'secret', algorithm='HS256')
    return encoded_jwt

#verify identification
def verify_jwt_token(token):
    try:
        _payload = jwt.decode(token, 'secret', algorithms='HS256')
    except jwt.PyJWTError as e:
        print(e)
        print('Not match!')
        return {'res': False}
    else:
        exp = int(_payload.pop('exp'))

        if time.time() > exp:
            print('Out of time!')
            return {'res': False}
        return {'res': True, 'user': _payload['data']['username']}

def authenticate(token):
    auth = verify_jwt_token(token)
    if not auth['res']:
        msg = 'No permission, please log in.'
        return False
    return auth['user']
