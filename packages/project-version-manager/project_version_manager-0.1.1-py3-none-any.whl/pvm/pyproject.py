from __future__ import annotations

import logging
from pathlib import Path
from typing import Self

import semver
from tomlkit.toml_document import TOMLDocument
from tomlkit.toml_file import TOMLFile

logger = logging.getLogger('pvm')


class PyProject:
    def __init__(self: Self, pyproject_path: str | Path | None = None):
        if pyproject_path is None:
            pyproject_path = Path.cwd() / 'pyproject.toml'
        self.pyproject_path = Path(pyproject_path)

        if not self.pyproject_path.exists():
            raise FileNotFoundError(f"pyproject.toml not found at: {self.pyproject_path}")

        self.toml_file = TOMLFile(str(self.pyproject_path))
        self.document: TOMLDocument | None = None
        self.version: semver.Version | None = None
        self._load()

    def _load(self: Self):
        """Load the version from pyproject.toml."""
        self.document = self.toml_file.read()
        raw_version: str | None = None

        if 'project' in self.document:
            raw_version = self.document.get('project', {}).get('version', None)
        elif self.document.get('tool', {}).get('poetry', {}).get('version', None):
            raw_version = self.document.get('tool', {}).get('poetry', {}).get('version', None)

        if raw_version is None:
            message = 'No version field found in pyproject.toml'
            logger.error(f'[-] {message}')
            raise ValueError(message)

        self.version = semver.Version.parse(raw_version)

        logger.debug(f'f"[+] Loaded version: {self.version}')

    def _set_version(self: Self, version: str) -> None:
        """Set the new version in the in-memory document."""
        if self.document is None:
            message = 'TOML document not loaded. Cannot set version.'
            logger.error(f'[-] {message}')
            raise ValueError(message)

        if self.document.get('project', {}).get('version', None):
            self.document['project']['version'] = version  # type: ignore

        # Poetry uses a different structure for the version field
        elif self.document.get('tool', {}).get('poetry', {}).get('version', None):
            self.document['tool']['poetry']['version'] = version  # type: ignore

        self.version = semver.Version.parse(version)

    def _save(self: Self):
        """Write the updated version back to pyproject.toml."""
        if self.document is None:
            message = 'TOML document not loaded.'
            logger.error(f'[-] {message}')
            raise ValueError(message)
        self.toml_file.write(self.document)

    def bump(self: Self, version: str) -> None:
        """Public method to bump version. Handles metadata and saving."""
        self._set_version(version)
        self._save()
