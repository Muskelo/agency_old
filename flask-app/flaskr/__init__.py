from flask import Flask
from flask_assets import Bundle, Environment
from flaskr.views import add_views

def add_assets(app):
    assets = Environment(app)
    assets.url = app.static_url_path
    scss = Bundle("style.scss", filters='pyscss', output='style.css')
    assets.register("scss_all", scss)

def create_app():
    app = Flask(__name__)

    add_assets(app)
    add_views(app)

    return app

