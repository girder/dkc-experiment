from fs import open_fs
from marshmallow import fields
from marshmallow.exceptions import ValidationError

from girder_dkc import BaseSchema, db


def _validate_base_uri(base_uri):
    # TODO: Prevent exposing arbitrary path's on the server?
    try:
        open_fs(base_uri, create=True)
    except Exception as e:
        raise ValidationError(str(e).strip(), data=base_uri, field_name='base_uri')


class AssetStore(db.Model):
    base_uri = db.Column(db.String, nullable=False)

    @property
    def fs(self):
        return open_fs(self.base_uri)


class AssetStoreSchema(BaseSchema):
    __model__ = AssetStore

    base_uri = fields.Str(required=True, validate=_validate_base_uri)
