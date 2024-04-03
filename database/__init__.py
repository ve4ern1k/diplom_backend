from settings import DB_DATABASE_NAME, DB_HOST, DB_PASSWORD, DB_PORT, DB_USER
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session


engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE_NAME}', echo=False)
Base = declarative_base()

Session_factory = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    ),
)

@contextmanager
def SessionCtx(old_session:Session = None):
    
    if old_session is None:
        session: Session = Session_factory()
    else:
        session: Session = old_session
        
    try:
        yield session
    except Exception:
        print('Session rollback because of exception')
        session.rollback()
        raise
    else:
        session.commit()
    finally:
        session.close() 


from .user import User
from .user_group import UserGroup
from .user_group_link import UserGroupLink
