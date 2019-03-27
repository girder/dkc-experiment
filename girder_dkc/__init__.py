from datetime import datetime
from uuid import uuid4

from flask_sqlalchemy import Model as _Model, SQLAlchemy
from marshmallow import fields, post_load, Schema
from sqlalchemy import Column, DateTime, MetaData
from sqlalchemy_utils.types.uuid import UUIDType


# This is to avoid having to manually name all constraints
# See: http://alembic.zzzcomputing.com/en/latest/naming.html
metadata = MetaData(naming_convention={
    'pk': 'pk_%(table_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'ix': 'ix_%(table_name)s_%(column_0_name)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(column_0_name)s',
})


class BaseModel(_Model):
    id = Column(UUIDType, primary_key=True, default=uuid4)
    created = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated = Column(DateTime, onupdate=datetime.utcnow)


db = SQLAlchemy(model_class=BaseModel, metadata=metadata)


class BaseSchema(Schema):
    __model__ = None

    id = fields.UUID(missing=uuid4)
    created = fields.DateTime(dump_only=True)

    @post_load
    def make_object(self, data):
        return self.__model__(**data)
