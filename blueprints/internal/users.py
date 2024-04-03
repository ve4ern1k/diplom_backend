from flask import Blueprint, request
from sqlalchemy import select
from database import SessionCtx, User, orm_to_dict
from exceptions import AuthorizationException
from utils import generate_hash
from tokens import generate_token, check_auth


user_bl = Blueprint('user_bl', __name__)


@user_bl.post('/login')
def login_user():
    data = request.json
    with SessionCtx() as session:
        user = session.execute(
            select(User).where(User.login == data.get('login'))
        ).first()

        if not user:
            raise AuthorizationException('Неверный логин или пароль')
        
        user: User = user[0]
        if user.hid != generate_hash(f'{data.get("login")}{data.get("password")}'):
            raise AuthorizationException('Неверный логин или пароль')

        return {'token': generate_token(user)}
    

@user_bl.get('/my_info')
@check_auth(insert_user_id=True)
def get_my_info(user_id: int):
    with SessionCtx() as session:
        user = session.execute(
            select(User).where(User.id == user_id)
        ).first()
        user: User = user[0]

        result = orm_to_dict(user, ['hid'])
        result['userGroups'] = [ group_link.user_group_obj.title for group_link in user.user_group_links ]
        return result
