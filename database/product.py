from typing import Optional, List
from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base


class Product(Base):
    __tablename__ = 'products'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    image: Mapped[Optional[str]]
    category: Mapped[int] = mapped_column(ForeignKey('categories.id'))
    cost: Mapped[int]
    data: Mapped[JSON] = mapped_column(type_=JSON)

    category_model: Mapped['Category'] = relationship(back_populates='products', uselist=False)
    order_items: Mapped[List['OrderItem']] = relationship(back_populates='product_model', uselist=True)


from .category import Category
from .order_item import OrderItem
