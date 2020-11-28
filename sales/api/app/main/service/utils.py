"""Service utilities."""
from uuid import uuid4


def generate_id() -> str:
    """Generate id."""
    return uuid4().hex
