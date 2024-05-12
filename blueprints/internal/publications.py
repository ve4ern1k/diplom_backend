from flask import Blueprint
from database import SessionCtx, Publication
from exceptions import NotFoundException


publication_bl = Blueprint('publication', __name__)


@publication_bl.get('/all')
def get_all_publication():
    with SessionCtx() as session:
        return [
            {
                'id': publ.id,
                'title': publ.title,
                'date': publ.date.strftime('%d.%m.%Y'),
                'image': publ.image
            }
            for publ in session.query(Publication).all()
        ]


@publication_bl.get('/<int:publ_id>')
def get_publication_for_id(publ_id: int):
    with SessionCtx() as session:
        publ: Publication | None = session.query(Publication).get(publ_id)
        if publ is None:
            raise NotFoundException(f'Публикация не найдена')
        
        return {
            'id': publ.id,
            'title': publ.title,
            'date': publ.date.strftime('%d.%m.%Y'),
            'image': publ.image,
            'structure': publ.structure_only_visible
        }
