from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base


class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    product: Mapped[int] = mapped_column(ForeignKey('products.id'))
    count: Mapped[int]
    price: Mapped[int]

    order_model: Mapped['Order'] = relationship(back_populates='items', uselist=False)
    product_model: Mapped['Product'] = relationship(back_populates='order_items', uselist=False)


from .order import Order
from .product import Product
