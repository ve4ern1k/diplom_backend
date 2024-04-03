from flask import Blueprint, request
from sqlalchemy import select
from database import SessionCtx, User
from exceptions import AuthorizationException
from utils import generate_hash
from tokens import generate_token


user_bl = Blueprint('user_bl', __name__)


@user_bl.post('/login')
def login_user():
    data = request.json
    with SessionCtx() as session:
        user = session.execute(
            select(User)
                .where(User.login == data.get('login'))
        ).first()

        if not user:
            raise AuthorizationException('Неверный логин или пароль')
        
        user: User = user[0]
        if user.hid != generate_hash(f'{data.get("login")}{data.get("password")}'):
            raise AuthorizationException('Неверный логин или пароль')

        return {'token': generate_token(user)}
