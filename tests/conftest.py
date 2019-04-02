from io import BytesIO
from tempfile import TemporaryDirectory

import dotenv
import pytest

from girder_dkc import db
from girder_dkc.app import create_app
from girder_dkc.models import FileSchema, FilesystemSchema


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

    with app.test_request_context():
        yield app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client


@pytest.fixture
def filesystem(app):
    filesystem_schema = FilesystemSchema()
    with TemporaryDirectory() as d:
        a = filesystem_schema.load({'base_uri': f'file://{d}'})
        db.session.add(a)
        db.session.commit()
        yield a


@pytest.fixture
def file(filesystem):
    file_schema = FileSchema()
    file = file_schema.load({'path': '/test.txt', 'filesystem_id': filesystem.id})
    db.session.add(file)
    db.session.commit()
    file.upload(BytesIO(b'test'))
    yield file
