"""Application Factory."""
import os

from flask import Flask


def create_app():
    """Application Factory."""
    app = Flask(__name__)

    register_configuration(app)

    @app.route("/ping")
    def _ping():
        return "rest api pong!"

    return app


def register_configuration(app):
    """Register configuration."""
    app.config.from_object(os.getenv("APP_CONFIG"))
