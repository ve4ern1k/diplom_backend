import random
from datetime import datetime
from flask import Blueprint, request
from sqlalchemy.orm import Session
from database import SessionCtx, Order, OrderItem, Product, orm_to_dict
from services import OrderService
from tokens import check_auth


order_bl = Blueprint('order', __name__)


def generate_code(session: Session) -> int:
    numb = None
    while True:
        numb = random.randint(10000000, 99999999)
        if session.query(Order).where(Order.code == numb).first() is None:
            break
    
    return numb


@order_bl.post('/create')
def create_order():
    data = request.json
    with SessionCtx() as session:
        order = Order(
            code = generate_code(session),
            customer = data['customer'],
            phone = data['phone'],
            email = data['email'],
            date = datetime.now().date(),
            status = 'Принят',
            prepaid = False
        )
        session.add(order)
        session.flush((order,))

        session.add_all(
            OrderItem(
                order = order.id,
                product = product['id'],
                count = product['count'],
                price = session.query(Product).get(product['id']).cost
            )
            for product in data['structure']
        )
        session.commit()

        return OrderService(session).map_order(order)


@order_bl.get('/all')
@check_auth(need_right='see_orders')
def get_all_orders():
    with SessionCtx() as session:
        return [
            {
                **orm_to_dict(order),
                'fullPrice': sum(item.price * item.count for item in order.items)
            }
            for order in session.query(Order).all()
        ]


@order_bl.get('/<int:id>')
@check_auth(need_right='update_orders')
def get_order_info(id: int):
    with SessionCtx() as session:
        return OrderService(session).get_order_info(id)


@order_bl.post('/update')
@check_auth(need_right='update_orders')
def update_order():
    data = request.json

    with SessionCtx() as session:
        order: Order = session.query(Order).get(data['id'])

        if 'phone' in data:
            order.phone = data['phone']
        if 'email' in data:
            order.email = data['email']
        if 'status' in data:
            order.status = data['status']
        if 'prepaid' in data:
            order.prepaid = data['prepaid']

        session.commit()
        return OrderService(session).map_order(order)
