import click

from girder_dkc.app import create_app
from girder_dkc.models import db


@click.command()
def create_tables():
    app = create_app()

    with app.app_context():
        db.create_all()
