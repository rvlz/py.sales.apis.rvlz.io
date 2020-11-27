"""Flask CLI commands."""
from flask.cli import FlaskGroup

from app.main import create_app

cli = FlaskGroup(create_app=create_app)

if __name__ == "__main__":
    cli()
