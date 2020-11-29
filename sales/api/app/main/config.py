"""Application configuration."""
import os


class BaseConfig:
    """Base configuration."""

    TESTING = False
    DB_NAME = os.getenv("DB_NAME")
    DB_USERNAME = os.getenv("DB_USERNAME")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")


class DevelopmentConfig(BaseConfig):
    """Development configuration."""


class TestingConfig(BaseConfig):
    """Testing configuration."""

    TESTING = True
    DB_NAME = os.getenv("DB_NAME_TEST")
