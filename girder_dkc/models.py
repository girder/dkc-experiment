from flask_sqlalchemy import SQLAlchemy
from marshmallow import post_load, Schema
from sqlalchemy import MetaData


# This is to avoid having to manually name all constraints
# See: http://alembic.zzzcomputing.com/en/latest/naming.html
metadata = MetaData(naming_convention={
    'pk': 'pk_%(table_name)s',
    'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'ix': 'ix_%(table_name)s_%(column_0_name)s',
    'uq': 'uq_%(table_name)s_%(column_0_name)s',
    'ck': 'ck_%(table_name)s_%(column_0_name)s',
})
db = SQLAlchemy(metadata=metadata)


class BaseSchema(Schema):
    __model__ = None

    @post_load
    def make_object(self, data):
        if self.__model__ is not None:
            return self.__model__(**data)
        return data
