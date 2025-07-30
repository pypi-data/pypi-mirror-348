"""Print the installed version of the package."""

from importlib.metadata import version as metadata_version

import typer

DISTRIBUTION_NAME = "netwatcher"

app = typer.Typer()


@app.command()
def version() -> None:
    """Print the installed version of the package."""
    typer.echo(metadata_version(DISTRIBUTION_NAME))
