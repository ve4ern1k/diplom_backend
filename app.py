from flask import Flask
from blueprints import internal_bl, media_bl, webgui_bl


def build_app():
    app = Flask(__name__)
    app.register_blueprint(internal_bl, url_prefix='/internal')
    app.register_blueprint(media_bl, url_prefix='/media')
    app.register_blueprint(webgui_bl)

    return app
