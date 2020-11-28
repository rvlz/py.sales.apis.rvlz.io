"""Application Factory."""
from flask import Flask


def create_app():
    """Application Factory."""
    app = Flask(__name__)

    @app.route("/ping")
    def _ping():
        return "rest api pong!"

    return app
