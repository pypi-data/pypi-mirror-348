from typing import Annotated

import typer

from pvm import config
from pvm.changelog.generator import Generator

app = typer.Typer(no_args_is_help=True, help='PVM - Python Version Manager')


def handle_project_changelog(changelog_file: str):
    """Generate a changelog for the project."""
    typer.echo('[i] Generating changelog...')

    if not changelog_file:
        typer.echo('[-] invalid changelog file...', err=True)
        return

    generator = Generator()
    generator.write_changelog(output_path=changelog_file)


@app.command('changelog')
def changelog(
    file: Annotated[str, typer.Option('--file', '-f', help='Path to changelog file')] = str(
        config.get('changelog-file')
    ),
):
    """Generate a changelog for the project."""
    handle_project_changelog(file)
