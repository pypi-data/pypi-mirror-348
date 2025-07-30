import textwrap
from pathlib import Path
from typing import Annotated

import semver
import typer

from pvm import config
from pvm.changelog.utils import update_changelog
from pvm.cli.changelog import handle_project_changelog
from pvm.git import repo
from pvm.version import VersionBumper, VersionSyncer

app = typer.Typer(
    no_args_is_help=True,
    help='PVM - Python Version Manager',
)


@app.command('bump')
def bump_version(
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
            hidden=True,
            show_default=False,
            help=textwrap.dedent(
                """
                Whether or not to create a release in the remote VCS, if supported
                """
            ),
        ),
    ] = bool(config.get('release')),
    final_version: Annotated[
        bool,
        typer.Option(
            '--final',
            show_default=False,
            help=textwrap.dedent(
                """
                Force the next version to be a final version.
                No prerelease token, no build metadata will be included.
                """
            ),
        ),
    ] = bool(config.get('final')),
    prerelease: Annotated[
        bool,
        typer.Option(
            '--prerelease',
            '-p',
            show_default=False,
            # metavar='PRERELEASE',
            help=textwrap.dedent(
                """
                Force the next version to be a prerelease.
                """
            ),
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
    prerelease_offset: Annotated[
        int | None,
        typer.Option(
            hidden=True,
            metavar='OFFSET',
            show_default=False,
            help=textwrap.dedent(
                """
                Force the next prerelease to start from this offset, if --prerelease.
                e.g. 1, 10, 50, 100.
                """
            ),
        ),
    ] = config.get('prerelease-offset'),
    build: Annotated[
        bool,
        typer.Option(
            '--build',
            '-b',
            show_default=False,
            # metavar='METADATA',
            help=textwrap.dedent(
                """
                Force the next version to include build metadata.
                """
            ),
        ),
    ] = False,
    build_token: Annotated[
        str | None,
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
    build_offset: Annotated[
        int | None,
        typer.Option(
            hidden=True,
            metavar='OFFSET',
            show_default=False,
            help=textwrap.dedent(
                """
                Force the next build to start from this offset, if --build.
                e.g. 1, 10, 50, 100.
                """
            ),
        ),
    ] = config.get('build-offset'),
    changelog: Annotated[
        bool,
        typer.Option(
            '--changelog',
            '-c',
            help='Generate changelog',
        ),
    ] = bool(config.get('changelog')),
    changelog_file: Annotated[
        str | None,
        typer.Option(
            metavar='FILE',
            help='Path to changelog file',
        ),
    ] = config.get('changelog-file'),
    tag: Annotated[
        bool,
        typer.Option(
            '--tag',
            '-t',
            help='Whether or not to create a tag for the new version',
        ),
    ] = bool(config.get('tag')),
    tag_prefix: Annotated[
        str,
        typer.Option(
            '--tag-prefix',
            help='Tag prefix for version',
        ),
    ] = str(config.get('tag-prefix', 'v')),
    push: Annotated[
        bool,
        typer.Option(
            hidden=True,
            help='Whether or not to push the new commit and tag to the remote',
        ),
    ] = bool(config.get('tag')),
    commit: Annotated[
        bool,
        typer.Option(
            hidden=True,
            help='Whether or not to commit changes locally',
        ),
    ] = bool(config.get('tag')),
):
    """Bump the version of the project."""
    if tag:
        validate_tag_prefix(tag_prefix)

    try:
        bumper = VersionBumper()
        old_version = bumper.commits.latest_version()
        new_version = semver.Version.parse(
            bumper.bump_version(
                target=target,
                final_version=final_version,
                prerelease=prerelease,
                prerelease_token=prerelease_token,
                build=build,
                build_token=build_token,
            )
        )

        if str(new_version) == str(old_version):
            message = f'New version is the same as the current version: {old_version}'
            raise ValueError(message)

        version_files: list[str] | None = config.get('version-files')

        if version_files:
            syncer = VersionSyncer()
            syncer.sync(
                version=str(new_version),
                targets=version_files
            )

        if tag:
            tag_name = f'{tag_prefix}{new_version}'
            typer.echo(f'[i] Committing version change to {tag_name}')
            if version_files:
                files = []
                for target in version_files:
                    if ':' not in target:
                        raise ValueError("Target must be in format 'file:keypath' or 'file:regex'")
                    file_path, _ = target.split(':', 1)
                    path = Path(file_path)
                    if not path.exists():
                        raise FileNotFoundError(f'File not found: {file_path}')
                    files.append(path)

                if files:
                    repo.add(files)
                    repo.commit(f'chore: bump version to {tag_name}')

        if changelog:
            if changelog_file:
                handle_project_changelog(changelog_file)
                if tag:
                    update_changelog(changelog_file, f'{tag_prefix}{new_version}')

                    repo.add([changelog_file])
                    repo.commit(f'chore: update changelog file to include {tag_prefix}{new_version}')

        if tag:
            repo.tag(str(new_version), prefix=tag_prefix)

        tag_display = f'{tag_prefix}{new_version}' if tag else new_version
        typer.echo(
            f'[i] Version bumped and tagged: {old_version} -> {tag_display}'
            if tag
            else f'[i] Version bumped: {old_version} -> {new_version}'
        )

    except Exception as e:
        typer.echo(f'[~] Error: {e}', err=True)
        raise typer.Exit(1) from e


def validate_tag_prefix(tag_prefix: str):
    if tag_prefix not in ['', 'v', 'V']:
        typer.echo(
            textwrap.dedent(
                f"""
                [-] Invalid tag prefix `{tag_prefix}`.
                Use an empty tag or a tag starting with `v`.
                """
            ),
            err=True,
        )
        raise typer.Exit(1)
