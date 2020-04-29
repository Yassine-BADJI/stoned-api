from flask import Flask
from apis import api
from config import config_by_name
from extensions import db


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    api.init_app(app)
    register_extensions(app)
    return app


def register_extensions(app):
    db.init_app(app)
