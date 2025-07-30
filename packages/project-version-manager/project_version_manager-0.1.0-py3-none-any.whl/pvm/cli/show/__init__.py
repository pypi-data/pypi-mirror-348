import typer

from .current import app as current_app
from .next import app as next_app

app = typer.Typer(no_args_is_help=True, help='Show version details.')
app.add_typer(current_app)
app.add_typer(next_app)
