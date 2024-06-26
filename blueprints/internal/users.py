from PIL import Image
from flask import Blueprint, request
from sqlalchemy import select, delete
from database import SessionCtx, User, orm_to_dict, UserGroupLink
from exceptions import AuthorizationException, NotFoundException, ReferenceException
from utils import generate_hash
from tokens import generate_token, check_auth
from services import ImgService, UserGroupService


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


@user_bl.get('/all')
@check_auth(need_right='see_staff')
def get_all_staff():
    with SessionCtx() as session:
        users = session.query(User).all()

        return [ orm_to_dict(user, exclude_fields=['age', 'hid', 'birthday', 'login', 'quality', 'sex']) for user in users ]


@user_bl.get('/<int:id>')
@check_auth(need_right='update_staff')
def get_staff(id: int):
    with SessionCtx() as session:
        user = session.execute(
            select(User).where(User.id == id)
        ).first()
        
        if not user:
            raise NotFoundException(f'Сотрудник с id={id} не найден')

        user: User = user[0]
        result = orm_to_dict(user, ['hid'])
        result['userGroups'] = [ group_link.user_group_obj.title for group_link in user.user_group_links ]
        return result


@user_bl.post('/create')
@check_auth(need_right='update_staff')
def create_user():
    data = request.json
    with SessionCtx() as session:
        if session.query(User).where(User.login == data['login']).first() is not None:
            raise ReferenceException(f'Сотрудник с логином \"{data["login"]}\" уже существует')

        if not data['login'] or not data['password']:
            raise ReferenceException('Поля login и password являются обязательными для создания пользователя')

        created_user = User(
            login      = data['login'],
            hid        = generate_hash(f'{data.get("login")}{data.get("password")}'),
            firstname  = data['firstname'],
            lastname   = data['lastname'],
            middlename = data['middlename'],
            age        = data['age'],
            birthday   = data['birthday'],
            sex        = data['sex'],
            quality    = data['quality'],
            post       = data['post'],
            experience = data['experience'],
            salary     = data['salary'],
            email      = data['email'],
            phone      = data['phone'],
        )
        session.add( created_user )
        session.flush([ created_user ])

        UserGroupService(session).update_for_user(created_user.id, data.get('userGroups', []))

        session.commit()

        result = orm_to_dict(created_user, ['hid'])
        result['userGroups'] = [ group_link.user_group_obj.title for group_link in created_user.user_group_links ]
        return result


@user_bl.delete('/delete')
@check_auth(need_right='update_staff', insert_user_id=True)
def delete_user(user_id: int):
    delete_ids = request.json.get('idList', [])

    if any(user_id == deleted_id for deleted_id in delete_ids):
        raise ReferenceException('Вы не можете удалить собственный аккаунт')

    with SessionCtx() as session:
        session.execute(
            delete(UserGroupLink).where(UserGroupLink.user.in_(delete_ids))
        )
        session.execute(
            delete(User).where(User.id.in_(delete_ids))
        )
        session.commit()
    
    return {'result': True}


@user_bl.post('/image')
@check_auth(insert_user_id=True)
def update_user_pic(user_id: int):
    img_name = ImgService().save(
        Image.open(
            request.files['image']
        )
    )

    with SessionCtx() as session:
        user: User = session.query(User).get(user_id)
        user.img = img_name
        session.commit()
    
    return {'imageName': img_name}


@user_bl.post('/update_my')
@check_auth(insert_user_id=True)
def update_my_data(user_id: int):
    data = request.json

    with SessionCtx() as session:
        user: User = session.query(User).get(user_id)

        user.main_page = data.get('mainPage')

        if data.get('oldPassword') and data.get('newPassword'):
            if generate_hash(f'{user.login}{data.get("oldPassword")}') != user.hid:
                raise AuthorizationException('Неверный старый пароль')
            
            user.hid = generate_hash(f'{user.login}{data.get("newPassword")}')
        
        session.commit()
    
        return {'result': True}


@user_bl.post('/update')
@check_auth(need_right='update_staff')
def update_user():
    data = request.json
    user_id = data.get('id')

    with SessionCtx() as session:
        user: User | None = session.query(User).get(user_id)
        
        if user is None:
            raise NotFoundException(f'Сотрудник с id={user_id} не найден')

        if 'login' in data and session.query(User).where((User.login == data['login']) & (User.id != user_id)).first() is not None:
            raise ReferenceException('Пользователь с таким логином уже существует')

        for field, value in data.items():
            if field not in ('id', 'userGroups', 'hid') and hasattr(user, field):
                setattr(user, field, value)
        
        UserGroupService(session).update_for_user(user_id, data.get('userGroups', []))

        session.commit()

        result = orm_to_dict(user, ['hid'])
        result['userGroups'] = [ group_link.user_group_obj.title for group_link in user.user_group_links ]
        return result


@user_bl.post('/update_auth')
@check_auth(need_right='change_auth_data')
def update_auth_data():
    data = request.json
    user_id = data.get('id')

    with SessionCtx() as session:
        user: User | None = session.query(User).get(user_id)
        if user is None:
            raise NotFoundException(f'Сотрудник с id={user_id} не найден')
        
        if not data.get('login') or not data.get('password'):
            raise ReferenceException('Поля логина и пароля являются обязательными')

        user.login = data['login']
        user.hid = generate_hash(f'{user.login}{data["password"]}')

        session.commit()

        return { 'result': 'success' }
