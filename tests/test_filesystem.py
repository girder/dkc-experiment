from fs.base import FS
from marshmallow.exceptions import ValidationError
import pytest

from girder_dkc import db
from girder_dkc.models import Filesystem, FilesystemSchema

filesystem_schema = FilesystemSchema()


def test_create_new_filesystem(app):
    a = filesystem_schema.load({'base_uri': 'mem://'})
    db.session.add(a)
    db.session.commit()

    assert Filesystem.query.get(a.id) is not None


def test_filesystem_fs(filesystem):
    assert isinstance(filesystem.fs, FS)


def test_invalid_filesystem(app):
    with pytest.raises(ValidationError):
        filesystem_schema.load({'base_uri': 'not-a-protocol://'})
