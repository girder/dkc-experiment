from fs.base import FS
from marshmallow.exceptions import ValidationError
import pytest

from girder_dkc import db
from girder_dkc.models import AssetStore, AssetStoreSchema

asset_store_schema = AssetStoreSchema()


def test_create_new_asset_store(app):
    a = asset_store_schema.load({'base_uri': 'mem://'})
    db.session.add(a)
    db.session.commit()

    assert AssetStore.query.get(a.id) is not None


def test_asset_store_fs(asset_store):
    assert isinstance(asset_store.fs, FS)


def test_invalid_asset_store(app):
    with pytest.raises(ValidationError):
        asset_store_schema.load({'base_uri': 'not-a-protocol://'})
