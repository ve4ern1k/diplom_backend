from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base


class UserGroup(Base):
    __tablename__ = 'user_groups'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]

    see_staff: Mapped[bool]
    see_staff_groups: Mapped[bool]
    see_orders: Mapped[bool]
    see_publications: Mapped[bool]
    update_staff: Mapped[bool]
    update_staff_groups: Mapped[bool]
    update_orders: Mapped[bool]
    update_publications: Mapped[bool]
    change_auth_data: Mapped[bool]
    write_publications: Mapped[bool]

    user_group_links: Mapped[List['UserGroupLink']] = relationship(back_populates='user_group_obj')


from .user_group_link import UserGroupLink
