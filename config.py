from os import getenv
from datetime import timedelta


class Config:
    SECRET_KEY = getenv('SECRET_KEY') or 'random string'
    PORT = int(getenv('PORT', 5000))
    DEBUG = getenv('DEBUG') or False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(getenv('JWT_REFRESH_TOKEN_EXPIRES'))
    )


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True


class TestingConfig(Config):
    FLASK_ENV = 'testing'
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
