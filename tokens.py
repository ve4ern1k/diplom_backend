import jwt
from functools import wraps
from flask import request
from sqlalchemy import select
from datetime import datetime
from database import User, SessionCtx
from exceptions import AuthorizationException, AccessExceptiom


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
    try:
        return jwt.decode(token, SECRET_TOKEN, algorithms=['HS256'])
    except jwt.DecodeError:
        raise AuthorizationException('Неверный токен')


def check_auth(need_right: str = None, insert_user_id = False):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            if token is None:
                raise AuthorizationException('Отсутствует заголовок "Authorization"')
            
            token_data = decode_token(token)

            with SessionCtx() as session:
                user = session.query(User).get(token_data['user_id'])

                if not user:
                    raise AuthorizationException('Пользователь не найден')

                if need_right is not None:
                    if not any(getattr(user_group_link.user_group_obj, need_right) for user_group_link in user.user_group_links):
                        raise AccessExceptiom('Недостаточно прав для доступа')
            
            if insert_user_id:
                kwargs['user_id'] = token_data['user_id']
            return function(*args, **kwargs)
        return wrapper
    return decorator
