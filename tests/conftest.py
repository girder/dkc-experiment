import dotenv
import pytest

from girder_dkc.app import create_app
from girder_dkc.models import db


@pytest.fixture(autouse=True)
def mock_load_dotenv(monkeypatch):
    def do_nothing(*args, **kwargs):
        pass

    monkeypatch.setattr(dotenv, 'load_dotenv', do_nothing)


@pytest.fixture
def app():
    app = create_app({
        'ENV': 'testing',
        'SQLALCHEMY_DATABASE_URI': f'sqlite://'
    })
    with app.app_context():
        db.create_all()

    yield app


@pytest.fixture
def client(app):
    with app.test_request_context(), app.test_client() as client:
        yield client
