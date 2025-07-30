import textwrap
from typing import Annotated

import typer

from pvm import config
from pvm.version import bump

app = typer.Typer(
    no_args_is_help=True,
    help='Show the next version, as predicted from commit history or rules.',
)


def get_next_version(value: bool):
    if value:
        typer.echo(bump())
        raise typer.Exit()


@app.command('next')
def show_version(
    target: Annotated[
        str | None,
        typer.Argument(
            show_default=False,
            help=textwrap.dedent(
                """
                Optinal version target to bump
                (major, minor, patch, prerelease, build, or valide smever
                (ex. 0.1.0, 0.1.0-alpha.1, 0.1.0-alpha.1+build.1))\n
                major   \t-   Force the next version to be a major release\n
                minor   \t-   Force the next version to be a minor release\n
                patch   \t-   Force the next version to be a patch release\n
                0.1.0   \t-   Force the next version to be 0.1.0-alpha.1+build.1\n
                0.1.0-alpha.1   \t-   Force the next version to be 0.1.0-alpha.1+build.1\n
                0.1.0-alpha.1+build.1  \t-   Force the next version to be 0.1.0-alpha.1+build.1\n
                0.1.0+build.1   \t-   Force the next version to be 0.1.0-alpha.1+build.1\n
                """
            ),
        ),
    ] = config.get('bump-target'),
    release: Annotated[
        bool,
        typer.Option(
            '--release',
            '-r',
             hidden=True,
            help='Release version',
        ),
    ] = False,
    final_version: Annotated[
        bool,
        typer.Option(
            '--final',
            help='Release version',
        ),
    ] = False,
    prerelease: Annotated[
        bool,
        typer.Option(
            '--prerelease',
            '-p',
            help='Prerelease version',
        ),
    ] = False,
    prerelease_token: Annotated[
        str | None,
        typer.Option(
            metavar='TOKEN',
            help=textwrap.dedent(
                """
                Force the next version to use this prerelease token, if --prerelease.
                e.g. `dev`, `alpha`, `beta`, `rc`.
                """
            ),
        ),
    ] = str(config.get('prerelease-token')),
    build: Annotated[
        bool,
        typer.Option(
            '--build',
            '-b',
            help='Build metadata',
        ),
    ] = False,
    build_token: Annotated[
        str,
        typer.Option(
            metavar='TOKEN',
            help=textwrap.dedent(
                """
                Force the next version to use this build metadata token, if --build.
                e.g. build, post, etc.
                """
            ),
        ),
    ] = str(config.get('build-token')),
):
    """Show the next project version."""
    version = bump(
        target=target,
        final_version=final_version,
        prerelease=prerelease,
        prerelease_token=prerelease_token,
        build=build,
        build_token=build_token,
    )

    typer.echo(version)
