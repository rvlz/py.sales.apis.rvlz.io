"""Utility functions."""


def row_to_dict(cols, row):
    """Convert row data to dictionary."""
    return dict(zip(cols, row))


def field_from_constraint(constraint):
    """Extract field name from constraint name."""
    if constraint.endswith("pkey"):
        return "id"
    raise ValueError("Malformed constraint name")
