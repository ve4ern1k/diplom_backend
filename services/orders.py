from sqlalchemy.orm import Session
from database import Order, orm_to_dict


class OrderService:

    def __init__(self, session: Session):
        self.session = session

    
    def map_order(self, order: Order) -> dict:
        structure = []
        full_price = 0
        for item in order.items:
            structure.append({
                'name': item.product_model.name,
                'category': item.product_model.category_model.name,
                'count': item.count,
                'price': item.price,
                'fullPrice': item.price * item.count
            })
            full_price += item.price * item.count
        
        return {
            'fullPrice': full_price,
            'structure': structure,
            **orm_to_dict(order)
        }


    def get_order_info(self, order_id: int) -> dict:
        return self.map_order(
            self.session.query(Order).get(order_id)
        )
