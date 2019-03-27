import click

from girder_dkc import db
from girder_dkc.app import create_app


@click.command()
def create_tables():
    import girder_dkc.models  # noqa
    app = create_app()

    with app.app_context():
        db.create_all()
