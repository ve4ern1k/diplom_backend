from flask import Blueprint

from database import SessionCtx, orm_to_dict, Category


products_bl = Blueprint('products', __name__)


@products_bl.get('/categories')
def get_categories():
    with SessionCtx() as session:
        return [ 
            orm_to_dict(category) 
            for category in session.query(Category).where(Category.parent == None).all()
        ]


@products_bl.get('/category/<int:id_category>')
def get_items_for_category(id_category: int):
    with SessionCtx() as session:
        category_root: Category = session.query(Category).get(id_category)
        
        if len(category_root.children) != 0:
            return {
                'categories': [
                    {
                        **orm_to_dict(category),
                        'products': [ orm_to_dict(product) for product in category.products ]
                    }
                    for category in category_root.children
                ]
            }
        else:
            return {
                'products': [ orm_to_dict(product) for product in category_root.products ]
            }
