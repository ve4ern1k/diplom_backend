from flask import Blueprint, request
from sqlalchemy import delete
from tokens import check_auth
from database import SessionCtx, UserGroup, orm_to_dict, UserGroupLink
from exceptions import NotFoundException, ReferenceException
from utils import to_snake_case


user_group_bl = Blueprint('user_group_bl', __name__)


@user_group_bl.get('/all')
@check_auth(need_right='see_staff_groups')
def get_all_groups():
    with SessionCtx() as session:
        return [
            orm_to_dict(group, exclude_fields=[
                'see_staff', 
                'see_staff_groups', 
                'see_orders', 
                'see_publications', 
                'update_staff', 
                'update_staff_groups', 
                'update_orders', 
                'update_publications', 
                'change_auth_data', 
                'write_publications'
            ]) for group in session.query(UserGroup).all()
        ]


@user_group_bl.get('/<int:group_id>')
@check_auth(need_right='update_staff_groups')
def get_group(group_id: int):
    with SessionCtx() as session:
        group: UserGroup | None = session.query(UserGroup).get(group_id)
        if group is None:
            raise NotFoundException(f'Группа сотрудников с id={group_id} не найдена')

        return orm_to_dict(group)


@user_group_bl.post('/create')
@check_auth(need_right='update_staff_groups')
def create_user_group():
    data = request.json
    with SessionCtx() as session:
        if not data.get('title') or not data.get('description'):
            raise ReferenceException('Поля заголовка и описания являются обязательными')

        group = UserGroup(
            title=data['title'],
            description=data['description'],
            see_staff=data.get('seeStaff', False),
            see_staff_groups=data.get('seeStaffGroups', False),
            see_orders=data.get('seeOrders', False),
            see_publications=data.get('seePublications', False),
            update_staff=data.get('updateStaff', False),
            update_staff_groups=data.get('updateStaffGroups', False),
            update_orders=data.get('updateOrders', False),
            update_publications=data.get('updatePublications', False),
            change_auth_data=data.get('changeAuthData', False),
            write_publications=data.get('writePublications', False),
        )
        session.add(group)
        session.commit()

        return orm_to_dict(group)


@user_group_bl.post('/update')
@check_auth(need_right='update_staff_groups')
def update_group():
    data = request.json
    group_id = data.get('id')

    with SessionCtx() as session:
        group: UserGroup | None = session.query(UserGroup).get(group_id)
        
        if group is None:
            raise NotFoundException(f'Группа с id={group_id} не найден')
        
        if any(field in data and not data[field] for field in ('title', 'description')):
            raise ReferenceException('Поля заголовка и описания являются обязательными')

        for field, value in data.items():
            snake_field = to_snake_case(field)
            if snake_field not in ('id') and hasattr(group, snake_field):
                setattr(group, snake_field, value)

        session.commit()

        return orm_to_dict(group)


@user_group_bl.delete('/delete')
@check_auth(need_right='update_staff_groups')
def delete_groups():
    delete_ids = request.json.get('idList', [])
    with SessionCtx() as session:
        session.execute(
            delete(UserGroupLink).where(UserGroupLink.user_group.in_(delete_ids))
        )
        session.execute(
            delete(UserGroup).where(UserGroup.id.in_(delete_ids))
        )
        session.commit()
    
    return {'result': True}
