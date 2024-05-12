from typing import Optional, List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    parent: Mapped[Optional[int]] = mapped_column(ForeignKey('categories.id'))

    parent_model: Mapped[Optional['Category']] = relationship(back_populates='children', uselist=False, remote_side=[id])
    children: Mapped[List['Category']] = relationship(back_populates='parent_model', uselist=True)

    products: Mapped[List['Product']] = relationship(back_populates='category_model', uselist=True)

from .product import Product
