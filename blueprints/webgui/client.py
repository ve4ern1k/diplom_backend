import os
from flask import Blueprint


webgui_client = Blueprint('webgui_client', __name__, static_folder=os.path.join(os.getcwd(), "static", "client"))


@webgui_client.route('/', defaults={'path': ''})
@webgui_client.route('/<path:path>')
def index(path):
    if not ('.' in path):
        return webgui_client.send_static_file('index.html')
    else:
        return webgui_client.send_static_file(path)
