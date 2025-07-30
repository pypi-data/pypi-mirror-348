import typer

from pvm import __version__

from .bump import app as bump_app
from .changelog import app as changelog_app
from .show import app as show_app

app = typer.Typer(no_args_is_help=True, help='PVM - Project Version Manager')

app.add_typer(bump_app)
app.add_typer(changelog_app)
app.add_typer(show_app, name='show')


def show_version(value: bool):
    if value:
        typer.echo(f'Version {__version__}')
        raise typer.Exit()


@app.callback()
def callback(
    version: bool = typer.Option(
        None,
        '--version',
        callback=lambda value: show_version(value),
        is_eager=True,
        help='Show the version and exit.',
    ),
):
    pass


if __name__ == '__main__':
    app()
