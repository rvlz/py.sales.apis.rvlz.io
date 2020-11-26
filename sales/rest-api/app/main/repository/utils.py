"""Utility functions."""


def row_to_dict(cols, row):
    """Convert row data to dictionary."""
    return dict(zip(cols, row))
