from PIL import Image
from flask import Blueprint, request
from sqlalchemy import delete
from tokens import check_auth
from services import ImgService
from datetime import datetime
from database import SessionCtx, Publication


publication_edit_bl = Blueprint('publication_edit', __name__)


def map_publication(publ: Publication, extend = False):
    result = {
        'id': publ.id,
        'title': publ.title,
        'date': publ.date.strftime('%d.%m.%Y'),
        'author': publ.author_model.fullname,
        'lastUpdatesDate': publ.last_updates_date.strftime('%d.%m.%Y')
    }

    if extend:
        result.update({
            'structure': publ.structure,
            'image': publ.image,
            'lastUpdatesAuthor': publ.last_updates_author_model.fullname
        })
    
    return result


@publication_edit_bl.post('/image')
@check_auth(need_right='update_publications')
def upload_image():
    img_name = ImgService().save(
        Image.open(
            request.files['image']
        )
    )

    return {'imageName': img_name}



@publication_edit_bl.post('/create')
@check_auth(need_right='write_publications', insert_user_id=True)
def create_publication(user_id: int):
    data = request.json
    today = datetime.now().date()
    with SessionCtx() as session:
        publication = Publication(
            title=data['title'],
            image=data.get('image'),
            date=today,
            author=user_id,
            structure=data['structure'],
            last_updates_date=today,
            last_updates_author=user_id
        )
        session.add(publication)
        session.commit()

        return map_publication(publication, extend=True)


@publication_edit_bl.get('/all')
@check_auth(need_right='update_publications')
def get_all_publications():
    with SessionCtx() as session:
        return [
            map_publication(publ)
            for publ in session.query(Publication).all()
        ]


@publication_edit_bl.get('/<int:id_publ>')
@check_auth(need_right='update_publications')
def get_public(id_publ: int):
    with SessionCtx() as session:
        return map_publication(
            session.query(Publication).get(id_publ),
            extend=True
        )
    

@publication_edit_bl.post('/update')
@check_auth(need_right='update_publications', insert_user_id=True)
def update_public(user_id: int):
    data = request.json
    with SessionCtx() as session:
        publ: Publication = session.query(Publication).get(data['id'])
        
        if 'title' in data:
            publ.title = data['title']
        if 'image' in data:
            publ.image = data['image']
        if 'structure' in data:
            publ.structure = data['structure']

        publ.last_updates_date = datetime.now().date()
        publ.last_updates_author = user_id

        session.commit()

        return map_publication(publ, extend=True)


@publication_edit_bl.delete('/delete')
@check_auth(need_right='update_publications')
def deletePublications():
    delete_ids = request.json.get('idList', [])
    with SessionCtx() as session:
        session.execute(
            delete(Publication).where(Publication.id.in_(delete_ids))
        )
        session.commit()
    
    return {'result': True}


@publication_edit_bl.delete('/image')
@check_auth(need_right='update_publications')
def delete_image():
    ImgService().delete(
        request.json['imageName']
    )
    return {'result': True}
