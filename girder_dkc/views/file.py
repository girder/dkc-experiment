from functools import partial

from flask import Blueprint, jsonify, request

from girder_dkc import db
from girder_dkc.models import File, FileSchema
from girder_dkc.pagination import paged_response

file_schema = FileSchema()
file_bp = Blueprint('file', __name__)


@file_bp.route('/file', methods=['GET'])
def list_files():

    # TODO: add filtering parameters

    return paged_response(File.query, partial(file_schema.dump, many=True))


@file_bp.route('/file', methods=['POST'])
def create_file():
    file = file_schema.load(request.json)
    db.session.add(file)
    db.session.commit()
    return jsonify(file_schema.dump(file)), 201


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
