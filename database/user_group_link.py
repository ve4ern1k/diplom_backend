from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base


class UserGroupLink(Base):
    __tablename__ = 'user_group_links'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user_group: Mapped[int] = mapped_column(ForeignKey('user_groups.id'))

    user_obj: Mapped['User'] = relationship(back_populates='user_group_links')
    user_group_obj: Mapped['UserGroup'] = relationship(back_populates='user_group_links')


from .user import User
from .user_group import UserGroup
