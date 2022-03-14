import os

from flask import Flask
from flask_migrate import Migrate
from flask_assets import Bundle, Environment

from flaskr.config import Configuration
from flaskr.resources import UserResource
from flaskr.views import add_views
from flaskr.db import db


def add_assets(app):
    assets = Environment(app)
    assets.url = app.static_url_path
    scss = Bundle("style.scss", filters='pyscss', output='style.css')
    assets.register("scss_all", scss)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Configuration)

    db.init_app(app)
    Migrate(app, db)

    add_assets(app)
    add_views(app)

    app.before_request(UserResource.load_user)

    @app.before_first_request
    def create_image_folder():
        try:
            if not os.path.exists(app.config['IMAGE_PATH']):
                os.makedirs(app.config['IMAGE_PATH'])
        except:
            pass

    return app

