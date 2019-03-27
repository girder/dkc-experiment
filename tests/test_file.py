from girder_dkc import db
from girder_dkc.models import File, FileSchema

file_schema = FileSchema()


def test_create_file(asset_store):
    f = file_schema.load({'path': '/test.txt', 'asset_store_id': asset_store.id})
    db.session.add(f)
    db.session.commit()

    assert File.query.get(f.id) is not None


def test_open_file(asset_store):
    file = file_schema.load({'path': '/test.txt', 'asset_store_id': asset_store.id})
    db.session.add(file)
    db.session.commit()

    with file.open('w') as f:
        f.write('test')

    import ipdb
    ipdb.set_trace()
    with file.open('r') as f:
        assert f.read() == 'test'
