import settings
from app import build_app
from database import engine, Base


if __name__ == '__main__':
    print('Создание таблиц в БД...')
    Base.metadata.create_all(engine)
    print('Таблицы в БД созданы')

    print(f'Запуск сервера на порту {settings.PORT}')
    build_app().run(settings.HOST, settings.PORT)
