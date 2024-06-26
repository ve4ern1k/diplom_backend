from typing import List
from settings import DB_DATABASE_NAME, DB_HOST, DB_PASSWORD, DB_PORT, DB_USER
from contextlib import contextmanager
from sqlalchemy import create_engine, Enum, Time, inspection
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base, Session
from utils import to_lower_camel_case


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


def orm_to_dict(item, exclude_fields: List[str] = list(), to_default_types = True) -> dict:
    result = {}
    inspect = inspection.inspect(item.__class__)
    for col in inspect.columns:
        if col.name in exclude_fields:
            continue
        
        colname_camel = to_lower_camel_case(col.name)
        if to_default_types:
            if isinstance(col.type, Enum):
                val = getattr(item, col.name)
                result[colname_camel] = val.name if val is not None else None
            elif isinstance(col.type, Time):
                result[colname_camel] = str(getattr(item, col.name))
            else:
                result[colname_camel] = getattr(item, col.name)
        else:
            result[colname_camel] = getattr(item, col.name)
    
    return result


from .user import User
from .user_group import UserGroup
from .user_group_link import UserGroupLink
from .category import Category
from .product import Product
from .order import Order
from .order_item import OrderItem
from .publication import Publication
