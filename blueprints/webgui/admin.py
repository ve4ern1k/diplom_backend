import os
from flask import Blueprint


webgui_admin = Blueprint('webgui_admin', __name__, static_folder=os.path.join(os.getcwd(), "static", "admin"))


@webgui_admin.route('/', defaults={'path': ''})
@webgui_admin.route('/<path:path>')
def index(path):
    if not ('.' in path):
        return webgui_admin.send_static_file('index.html')
    else:
        return webgui_admin.send_static_file(path)
