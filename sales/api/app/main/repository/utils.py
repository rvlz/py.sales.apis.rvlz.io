"""Utility functions."""


def row_to_dict(cols, row):
    """Convert row data to dictionary."""
    return dict(zip(cols, row))


def field_from_constraint(constraint):
    """Extract field name from constraint name."""
    if constraint.endswith("pkey"):
        return "id"
    raise ValueError("Malformed constraint name")


def extract_update_values(model, fields):
    """Check update method input."""
    values = []
    if len(fields) == 0:
        raise ValueError('"fields" argument cannot be empty list.')
    if model.id is None:
        raise ValueError('Instance attribute "id" cannot be None.')
    if "id" in fields:
        raise ValueError('"id" cannot be changed.')
    for f in fields:
        if not hasattr(model, f):
            raise ValueError(f'"{f}" not valid field.')
        values.append(getattr(model, f))
    values.append(model.id)
    return tuple(values)
