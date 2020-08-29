import pytest

from os.path import dirname, isfile, join

from dotenv import load_dotenv

_ENV_FILE = join(dirname(__file__), '../.env')

if isfile(_ENV_FILE):
    load_dotenv(dotenv_path=_ENV_FILE)


@pytest.fixture(scope='session')
def client():
    from apps import create_app, db
    flask_app = create_app('testing')

    testing_client = flask_app.test_client()

    with flask_app.app_context():
        db.create_all()
        yield testing_client
        db.drop_all()
