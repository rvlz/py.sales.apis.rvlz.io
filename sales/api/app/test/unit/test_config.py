"""Configuration tests."""
import os

import pytest

from app.main import create_app


@pytest.mark.parametrize("env", ["development"])
def test_development_config(config):
    app = create_app()
    assert app.config["TESTING"] is False
    assert app.config["DB_NAME"] is not None
    assert app.config["DB_NAME"] == os.getenv("DB_NAME")
    assert app.config["DB_USERNAME"] is not None
    assert app.config["DB_USERNAME"] == os.getenv("DB_USERNAME")
    assert app.config["DB_PASSWORD"] is not None
    assert app.config["DB_PASSWORD"] == os.getenv("DB_PASSWORD")
    assert app.config["DB_HOST"] is not None
    assert app.config["DB_HOST"] == os.getenv("DB_HOST")
    assert app.config["DB_PORT"] is not None
    assert app.config["DB_PORT"] == os.getenv("DB_PORT")


@pytest.mark.parametrize("env", ["testing"])
def test_testing_config(config):
    app = create_app()
    assert app.config["TESTING"] is True
    assert app.config["DB_NAME"] is not None
    assert app.config["DB_NAME"] == os.getenv("DB_NAME_TEST")
    assert app.config["DB_USERNAME"] is not None
    assert app.config["DB_USERNAME"] == os.getenv("DB_USERNAME")
    assert app.config["DB_PASSWORD"] is not None
    assert app.config["DB_PASSWORD"] == os.getenv("DB_PASSWORD")
    assert app.config["DB_HOST"] is not None
    assert app.config["DB_HOST"] == os.getenv("DB_HOST")
    assert app.config["DB_PORT"] is not None
    assert app.config["DB_PORT"] == os.getenv("DB_PORT")
