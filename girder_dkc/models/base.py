from marshmallow import post_load, Schema

from girder_dkc import db

BaseModel = db.Model


class BaseSchema(Schema):
    __model__ = None

    @post_load
    def make_object(self, data):
        return self.__model__(**data)
