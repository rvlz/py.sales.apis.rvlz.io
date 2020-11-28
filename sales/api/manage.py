"""Flask CLI commands."""
import sys

import pytest
import click
from flask.cli import FlaskGroup

from app.main import create_app

cli = FlaskGroup(create_app=create_app)


@cli.command("test")
@click.option("--verbose", "-v", is_flag=True)
@click.option("--base")
def run_tests(verbose, base):
    directory = f"app/test/{base}" if base is not None else "app/test"
    options = ["-x", directory]
    if verbose:
        options.append("-v")
    result = pytest.main(options)
    if result == pytest.ExitCode.OK:
        return 0
    sys.exit(result.value)


if __name__ == "__main__":
    cli()
