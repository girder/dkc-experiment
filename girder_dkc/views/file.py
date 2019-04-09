from functools import partial

from flask import Blueprint, current_app, jsonify
from webargs import fields
from webargs.flaskparser import use_args, use_kwargs

from girder_dkc import db
from girder_dkc.models import File, FileSchema
from girder_dkc.pagination import paged_response, pagination_args

file_schema = FileSchema()
file_bp = Blueprint('file', __name__)


@file_bp.route('/file', methods=['GET'])
@use_args(pagination_args)
def list_files(args):

    # TODO: add filtering parameters
    return paged_response(File.query, args, partial(file_schema.dump, many=True))


@file_bp.route('/file', methods=['POST'])
@use_kwargs({
    'filesystem_id': fields.UUID(required=True),
    'path': fields.Str(required=True),
    'data': fields.Field(location='files', required=False)
})
def create_file(filesystem_id, path, **kwargs):
    try:
        file = file_schema.load(filesystem_id=filesystem_id, path=path, **kwargs)
        db.session.add(file)

        if 'data' in kwargs:
            file.upload(kwargs['data'])

        db.session.commit()
        return jsonify(file_schema.dump(file)), 201
    except Exception:
        try:
            file.delete_blob()
        except Exception:
            current_app.logger.exception('Could not delete blob in error handler')
        db.session.rollback()
        raise


@file_bp.route('/file/<uuid:file_id>', methods=['GET'])
def get_file(file_id):
    return jsonify(file_schema.dump(File.query.get_or_404(file_id)))


@file_bp.route('/file/<uuid:file_id>', methods=['PUT'])
def modify_file(file_id):
    file = File.query.get_or_404(file_id)

    # TODO: add attribute changes
    db.session.add(file)
    db.session.commit()
    return file


@file_bp.route('/file/<uuid:file_id>', methods=['DELETE'])
def delete_file(file_id):
    File.query.get_or_404(file_id).delete()
    db.session.commit()
    return '', 204
