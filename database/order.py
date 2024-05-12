from typing import List
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[int] = mapped_column(unique=True)
    customer: Mapped[str]
    phone: Mapped[str]
    email: Mapped[str]
    date: Mapped[date]
    status: Mapped[str]
    prepaid: Mapped[bool]

    items: Mapped[List['OrderItem']] = relationship(back_populates='order_model', uselist=True)


from .order_item import OrderItem
