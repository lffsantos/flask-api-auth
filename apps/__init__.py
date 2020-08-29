import os

from flask import Flask

from apps.database import db
from config import config

from .api import configure_api

basedir = os.path.abspath(os.path.dirname(__file__))


def config_db(app):
    database_uri = os.environ.get('DATABASE_URL') \
                                                or 'sqlite:///' + os.path.join(basedir, 'cpfcheck.db')
    if app.config['FLASK_ENV'] == 'testing':
        database_uri = os.environ.get('DATABASE_TEST_URL') \
                                  or 'sqlite:///' + os.path.join(basedir, 'cpfcheck_test.db')

    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from apps.users import models
    db.create_all(app=app)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config_db(app)
    configure_api(app)
    return app
