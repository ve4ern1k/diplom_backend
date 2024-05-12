import settings
from app import build_app
from database import engine, Base, SessionCtx, User, UserGroup, UserGroupLink
from utils import generate_hash
from settings import USER_DEFAULT_LOGIN, USER_DEFAULT_PASSWORD


if __name__ == '__main__':
    print('Создание таблиц в БД...')
    Base.metadata.create_all(engine)
    print('Таблицы в БД созданы')

    print('Проверяем существование пользователя')
    with SessionCtx() as session:
        if session.query(User).count() == 0:
            print('Отсутствуют пользователи в БД, создаем пользователя по умолчанию')
            user = User(
                login=USER_DEFAULT_LOGIN,
                hid=generate_hash(f'{USER_DEFAULT_LOGIN}{USER_DEFAULT_PASSWORD}'),
                firstname='Admin',
                lastname='Default',
                middlename='Server',
                age=0,
                birthday='01.01.1900',
                sex='Мужской',
                quality='-',
                post='Серверная предустановка',
                experience=0,
                salary=0,
                email='-',
                phone='-',
            )
            
            group = UserGroup(
                title='Default admin',
                description='Серверная предустановка',
                see_staff=True,
                see_staff_groups=True,
                see_orders=True,
                see_publications=True,
                update_staff=True,
                update_staff_groups=True,
                update_orders=True,
                update_publications=True,
                change_auth_data=True,
                write_publications=True,
            )
            session.add_all((user, group))
            session.flush((user, group))

            session.add(
                UserGroupLink(
                    user=user.id,
                    user_group=group.id  
                )
            )

            session.commit()
            print('Был создан администратор по умолчанию')
        else:
            print('Пользователи в БД существуют')

    print(f'Запуск сервера на порту {settings.PORT}')
    build_app().run(settings.HOST, settings.PORT)
