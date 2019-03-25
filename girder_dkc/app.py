import os

from dotenv import load_dotenv
from flask import current_app, Flask, jsonify
from marshmallow import ValidationError
from werkzeug.contrib.fixers import ProxyFix

from girder_dkc import db


def handle_validation_error(e):
    return jsonify(e.messages), 400


def handle_general_error(e):
    current_app.logger.exception(e)
    return jsonify({'error': 'Something went wrong.'}), 500


def create_app(config=None):
    load_dotenv(os.getenv('DOTENV_PATH'))

    config = config or {}
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    app.config.update(config)
    db.init_app(app)

    app.register_error_handler(ValidationError, handle_validation_error)
    if app.config['ENV'] == 'production':
        app.register_error_handler(500, handle_general_error)

    return app
