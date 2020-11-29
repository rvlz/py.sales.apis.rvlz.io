"""Database."""
import psycopg2


def get_connection(config):
    """Set up and return database connection."""
    DB_NAME = "DB_NAME" if not config["TESTING"] else "DB_NAME_TEST"
    return psycopg2.connect(
        dbname=config[DB_NAME],
        user=config["DB_USERNAME"],
        password=config["DB_PASSWORD"],
        host=config["DB_HOST"],
        port=config["DB_PORT"],
    )
