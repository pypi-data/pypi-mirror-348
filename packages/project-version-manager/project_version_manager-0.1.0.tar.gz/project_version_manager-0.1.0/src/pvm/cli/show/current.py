import typer

# from pvm.pyproject import Pyproject
from pvm.version import latest

app = typer.Typer(help='Show the current version of the project.')


@app.command('current')
def show_current_version():
    """Display the current project version."""
    # version = Pyproject().version
    version = latest()
    typer.echo(f'{version}')
