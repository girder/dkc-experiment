from girder_dkc import db
from girder_dkc.models import File, FileSchema

file_schema = FileSchema()


def test_create_file(filesystem):
    f = file_schema.load({'path': '/test.txt', 'filesystem_id': filesystem.id})
    db.session.add(f)
    db.session.commit()

    assert File.query.get(f.id) is not None


def test_open_file(filesystem):
    file = file_schema.load({'path': '/test.txt', 'filesystem_id': filesystem.id})
    db.session.add(file)
    db.session.commit()

    with file.open('w') as f:
        f.write('test')

    with file.open('r') as f:
        assert f.read() == 'test'


def test_delete_file(file):
    assert file.filesystem.fs.exists(file.path)
    db.session.delete(file)
    db.session.commit()
    assert file.filesystem.fs.exists(file.path)
