import os
from logging.config import dictConfig

from flask import Flask

from apps.database import db
from config import config

from .api import configure_api
from apps.jwt import configure_jwt

basedir = os.path.abspath(os.path.dirname(__file__))


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'custom_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'standard',
            'filename': 'api.log'
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'WARNING',
            'propagate': False
        },
        'apps.auth': {
            'handlers': ['default', 'custom_handler'],
            'level': 'INFO',
            'propagate': False
        },
        '__main__': {
            'handlers': ['default', 'custom_handler'],
            'level': 'DEBUG',
            'propagate': False
        },
    }
}


dictConfig(LOGGING_CONFIG)


def config_db(app):
    database_uri = os.environ.get('DATABASE_URL') \
                                                or 'sqlite:///' + os.path.join(basedir, 'cpfcheck.db')
    if app.config['FLASK_ENV'] == 'testing':
        database_uri = os.environ.get('DATABASE_TEST_URL') \
                                  or 'sqlite:///' + os.path.join(basedir, 'cpfcheck_test.db')

    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    db.create_all(app=app)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config_db(app)

    configure_jwt(app)

    configure_api(app)
    return app
