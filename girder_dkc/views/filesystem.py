from functools import partial

from flask import Blueprint, jsonify, request
from webargs.flaskparser import use_args

from girder_dkc import db
from girder_dkc.models import Filesystem, FilesystemSchema
from girder_dkc.pagination import paged_response

filesystem_schema = FilesystemSchema()
filesystem_bp = Blueprint('filesystem', __name__)


@filesystem_bp.route('/filesystem', methods=['GET'])
def list_filesystems(filesystem):

    # TODO: add filtering parameters

    return paged_response(Filesystem.query, partial(filesystem_schema.dump, many=True))


@filesystem_bp.route('/filesystem', methods=['POST'])
@use_args(FilesystemSchema())
def create_filesystem(args):
    filesystem = filesystem_schema.load(request.json)
    db.session.add(filesystem)
    db.session.commit()
    return jsonify(filesystem_schema.dump(filesystem)), 201


@filesystem_bp.route('/filesystem/<uuid:filesystem_id>', methods=['GET'])
def get_filesystem(filesystem_id):
    return jsonify(filesystem_schema.dump(Filesystem.query.get_or_404(filesystem_id)))


@filesystem_bp.route('/filesystem/<uuid:filesystem_id>', methods=['PUT'])
@use_args(FilesystemSchema(exclude=['base_uri']))
def modify_filesystem(args, filesystem_id):
    filesystem = Filesystem.query.get_or_404(filesystem_id)

    # TODO: This is a dumb no-op now.  Need to decide how to handle filesystem
    #       changes. e.g. should we try to move existing files?

    db.session.add(filesystem)
    db.session.commit()
    return filesystem


@filesystem_bp.route('/filesystem/<uuid:filesystem_id>', methods=['DELETE'])
def delete_filesystem(filesystem_id):
    Filesystem.query.get_or_404(filesystem_id).delete()
    db.session.commit()
    return '', 204
