from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    login: Mapped[str] = mapped_column(nullable=False)
    hid: Mapped[str] = mapped_column(nullable=False)

    firstname: Mapped[str]
    lastname: Mapped[str]
    middlename: Mapped[str]
    age: Mapped[int]
    birthday: Mapped[str]
    sex: Mapped[str]
    quality: Mapped[str]
    post: Mapped[str]
    experience: Mapped[float]
    salary: Mapped[int]
    email: Mapped[str]
    phone: Mapped[str]
    img: Mapped[Optional[str]]
    main_page: Mapped[str] = mapped_column(server_default='/me')

    user_group_links: Mapped[List['UserGroupLink']] = relationship(back_populates='user_obj')

    @property
    def fullname(self) -> str:
        return f'{self.lastname} {self.firstname} {self.middlename}'


from .user_group_link import UserGroupLink
