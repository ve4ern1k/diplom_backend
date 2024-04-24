from flask import Blueprint, send_from_directory, abort
from services import ImgService
from werkzeug.exceptions import NotFound


media_bl = Blueprint('media', __name__)


@media_bl.get('/<str:pic_name>')
def get_pic(pic_name: str):
    try:
        return send_from_directory(
            ImgService().retreive_path(),
            pic_name
        )
    except NotFound:
        return abort(404)
