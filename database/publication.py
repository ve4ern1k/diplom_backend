import datetime 
from typing import Optional, List
from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base


def cratch(obj: dict) -> dict:
    result = {**obj}
    try:
        result.pop('visible')
    except:
        pass
    return result


class Publication(Base):
    __tablename__ = 'publications'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    image: Mapped[Optional[str]]
    date: Mapped[datetime.  date]
    author: Mapped[int] = mapped_column(ForeignKey('users.id'))
    structure: Mapped[JSON] = mapped_column(type_=JSON)
    last_updates_date: Mapped[datetime.date]
    last_updates_author: Mapped[int] = mapped_column(ForeignKey('users.id'))

    author_model: Mapped['User'] = relationship(foreign_keys=[author], uselist=False)
    last_updates_author_model: Mapped['User'] = relationship(foreign_keys=[last_updates_author], uselist=False)

    @property
    def structure_only_visible(self):
        if not isinstance(self.structure, list):
            return self.structure
        else:
            return [
                cratch(item)
                for item in self.structure
            ]


from .user import User
