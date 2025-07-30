"""NetWatcher CLI - Monitor outbound network connections."""

import typer

from .scan import app as scan_app
from .version import app as version_app

app = typer.Typer(help="NetWatcher CLI - Monitor outbound network connections.")

app.add_typer(scan_app)
app.add_typer(version_app)

if __name__ == "__main__":
    app()
