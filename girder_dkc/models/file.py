from marshmallow import fields, validate
from sqlalchemy_utils.types.uuid import UUIDType

from girder_dkc import BaseSchema, db

# TODO: Prevent paths containing '.' and '..' directories?
# pyfilesystem will prevent accessing outside the root of the filesystem,
# but to make indexing easier, it might be best to avoid path normalization
# concerns.
_path_regexp = r'/.+'


class File(db.Model):
    path = db.Column(db.String, nullable=False)

    filesystem_id = db.Column(UUIDType, db.ForeignKey('filesystem.id'))
    filesystem = db.relationship('Filesystem')

    def open(self, *args, **kwargs):
        return self.filesystem.fs.open(self.path, *args, **kwargs)


class FileSchema(BaseSchema):
    __model__ = File

    path = fields.Str(required=True, validate=validate.Regexp(_path_regexp))
    filesystem_id = fields.UUID(required=True, load_only=True)
    filesystem = fields.Nested('FilesystemSchema', dump_only=True)
