import logging
import pathlib
from typing import Any

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    import tomli as tomllib  # type: ignore # For Python <3.11

log = logging.getLogger('pvm')


def load_config_from_pyproject() -> dict:
    """Load the PVM tool config from pyproject.toml, if it exists in the user's working directory.

    Returns an empty dictionary if the file or expected section does not exist.
    """
    pyproject_path = pathlib.Path.cwd() / 'pyproject.toml'

    if not pyproject_path.is_file():
        return {}

    try:
        with pyproject_path.open('rb') as f:
            pyproject_data = tomllib.load(f)

        return pyproject_data.get('tool', {}).get('pvm', {})
    except Exception as e:
        # Optional: log or handle parsing errors
        log.exception(f'Failed to load pyproject.toml: {e}')
        return {}


def _get_changelog_file(default: Any) -> str:
    config: dict = load_config_from_pyproject()
    fallback = default if default else 'CHANGELOG.md'
    file = config.get('changelog-file', 'CHANGELOG.md')
    if isinstance(file, str):
        path = pathlib.Path(file)
        if not file.endswith('/') and path.name != '':
            return file

    log.error(f'[-] changelog-file must be a valid file name. Using default value: {fallback}')
    return fallback


def _get_version_files(default: Any| None = None) -> list[str]:
    config: dict = load_config_from_pyproject()
    fallback = default if default else []

    files = config.get('version-files', fallback)
    if isinstance(files, list):
        return files

    log.error(f'[-] version-files must be a valid list of files. Using default value: {fallback}')
    return fallback


def get(var: str, default: Any | None = None) -> Any | None:
    config = load_config_from_pyproject()
    defaults = {
        'mode': default,
        'bump-target': default,
        'prerelease': default,
        'build': default,
        'changelog': False,
        'tag': default if default is not None else False,
        'prerelease-token': default if default is not None else 'rc',
        'build-token': default if default is not None else 'build',
        'tag-prefix': default if default is not None else 'v',
        # 'version-files': default,
    }

    if var in defaults:
        return config.get(var, defaults[var])
    else:
        match var:
            case 'changelog_file':
                return _get_changelog_file(default)
            case 'changelog-file':
                return _get_changelog_file(default)
            case 'version-files':
                return _get_version_files(default)
            case _:
                return default
