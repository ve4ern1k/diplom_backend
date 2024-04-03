import json
from flask import Blueprint, Response
from exceptions import KBZBAdminBackBaseException


internal_bl = Blueprint('internal_bl', __name__)


@internal_bl.after_request
def add_body(r: Response):
    if r.is_json and r.status_code == 200:
        r.data = json.dumps({'error': r.status_code != 200, 'data': r.json})
    return r


@internal_bl.errorhandler(Exception)
def handle_internal_error(exc: Exception):
    return {
        'error': True,
        'error_class': exc.__class__.__name__,
        'message': str(exc)
    }, exc.status_code if isinstance(exc, KBZBAdminBackBaseException) else 500


from .users import user_bl

internal_bl.register_blueprint(user_bl, url_prefix='/user')