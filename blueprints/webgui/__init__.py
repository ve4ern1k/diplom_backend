from flask import Blueprint


webgui_bl = Blueprint('webgui', __name__)


from .admin import webgui_admin
from .client import webgui_client

webgui_bl.register_blueprint(webgui_client)
webgui_bl.register_blueprint(webgui_admin, url_prefix='/admin')
