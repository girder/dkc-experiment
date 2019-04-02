from shutil import copyfileobj

from flask import current_app
from marshmallow import fields, validate
from sqlalchemy import event
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy_utils.types.uuid import UUIDType

from girder_dkc import BaseSchema, db

# TODO: Prevent paths containing '.' and '..' directories?
# pyfilesystem will prevent accessing outside the root of the filesystem,
# but to make indexing easier, it might be best to avoid path normalization
# concerns.
_path_regexp = r'/.+'


class File(db.Model):
    __table_args__ = (UniqueConstraint('path', 'filesystem_id'),)

    path = db.Column(db.String, nullable=False)

    filesystem_id = db.Column(UUIDType, db.ForeignKey('filesystem.id'))
    filesystem = db.relationship('Filesystem')

    def upload(self, stream):
        # TODO: This is bad for cloud storage because all data passes through here.
        #       Ideally, we would want to do this async and commit the file model
        #       once it is done.
        with self.open('wb') as f:
            copyfileobj(stream, f)

    def open(self, *args, **kwargs):
        return self.filesystem.fs.open(self.path, *args, **kwargs)

    @classmethod
    def _delete_file_blob(cls, mapper, connection, target):
        try:
            with target.filesystem.fs as fs:
                fs.remove(target.path)
        except Exception as e:
            current_app.logger.exception(e)


event.listens_for(File, 'after_delete', File._delete_file_blob)


class FileSchema(BaseSchema):
    __model__ = File

    path = fields.Str(required=True, validate=validate.Regexp(_path_regexp))
    filesystem_id = fields.UUID(required=True, load_only=True)
    filesystem = fields.Nested('FilesystemSchema', dump_only=True)
