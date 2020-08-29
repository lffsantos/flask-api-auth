from os import getenv


class Config:
    SECRET_KEY = getenv('SECRET_KEY') or 'random string'
    PORT = int(getenv('PORT', 5000))
    DEBUG = getenv('DEBUG') or False


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
