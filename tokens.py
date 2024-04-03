import jwt
from flask import request
from datetime import datetime
from database import User
from exceptions import AuthorizationException


SECRET_TOKEN = 'sn6joCksX8xjtK18BB84GSgsLXF8sVhBiP1e7'


def generate_token(user: User):
    return jwt.encode(
        {
            'user_id': user.id,
            'created': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        },
        SECRET_TOKEN, 
        algorithm="HS256"
    )


def decode_token(token: str):
    return jwt.decode(token, SECRET_TOKEN, algorithms=['HS256'])


def check_auth(insert_user_id = False):
    def decorator(function):
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if token is None:
                raise AuthorizationException('Отсутствует заголовок "Authorization"')
            if insert_user_id:
                token_data = decode_token(token)
                kwargs['user_id'] = token_data['user_id']
            return function(*args, **kwargs)
        return wrapper
    return decorator
