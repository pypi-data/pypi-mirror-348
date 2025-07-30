import logging
import re
from typing import Self

import semver

from pvm import config
from pvm.git.parser import CommitParser

logger = logging.getLogger('pvm')


class VersionBumper:
    """Handles version bumping based on Git commits and semantic versioning."""

    def __init__(self: Self, repo_path: str = '.', tag_prefix: str | None = 'v'):
        self.commits = CommitParser(repo_path=repo_path, tag_prefix=tag_prefix)

    @staticmethod
    def bump_type(commits: list[str]) -> str:
        bump = 'patch'
        type_scope_bang_pattern = re.compile(r'^(?P<type>\w+)(\([^)]+\))?!?:')

        for msg in commits:
            msg_lower = msg.lower().strip()

            if any(key in msg_lower for key in ['breaking change:', 'breaking-change:', 'breaking:']):
                return 'major'

            first_line = msg_lower.splitlines()[0]
            match = type_scope_bang_pattern.match(first_line)
            if match:
                commit_type = match.group('type')
                if '!' in first_line.split(':')[0]:
                    return 'major'
                if commit_type == 'feat':
                    bump = 'minor' if bump != 'major' else bump
                elif commit_type == 'fix':
                    bump = 'patch' if bump not in ['minor', 'major'] else bump
        return bump

    def _validate_target(self: Self, target: str | None):
        if target and target not in ['major', 'minor', 'patch'] and not semver.Version.is_valid(target):
            raise ValueError(
                f"[-] Invalid target `{target}`. Use 'major', 'minor', 'patch',  or a valid SemVer version."
            )

    # def _handle_semver_bump(self, parsed, target, commits, prerelease_token, token):
    #     parsed = semver.Version.parse(target)

    #     if parsed.prerelease:
    #         prerelease = False
    #         prerelease_token = None
    #     if parsed.build:
    #         build = False
    #         build_token = None
    #     return parsed.next_version(target)

    def _handle_target(self: Self, parsed: semver.version.Version, target: str | None):
        # parsed = parsed.replace(prerelease=None, build=None)
        match target:
            case 'major':
                parsed = parsed.bump_major()
            case 'minor':
                parsed = parsed.bump_minor()
            case 'patch':
                parsed = parsed.bump_patch()
            # case "prerelease":
            #     parsed = parsed.bump_prerelease(prerelease_token)
            # case "build":
            #     parsed = parsed.bump_build(build_token)
            case _:
                raise ValueError(f'Invalide target or semver: `{target}`')

        return parsed

    def _handle_prerelease(self: Self, parsed: semver.version.Version, prerelease_token: str | None):
        if parsed.build:
            parsed = parsed.bump_prerelease(token=prerelease_token)

        if parsed.prerelease:
            old_token, _, old_num = parsed.prerelease.partition('.')
            if old_token != prerelease_token:
                # Switching prerelease phases
                parsed = parsed.replace(prerelease=f'{prerelease_token}.1')
                parsed = parsed.replace(build=None)
        else:
            parsed = parsed.bump_prerelease(token=prerelease_token)

        return parsed

    def _handle_build(self: Self, parsed: semver.version.Version, build_token: str | None):
        if parsed.build:
            old_build_parts = parsed.build.split('.')
            old_token = old_build_parts[0] if old_build_parts else ''

            if old_token != build_token:
                parsed = parsed.replace(build=f'{build_token}.1')
        else:
            parsed = parsed.bump_build(token=build_token)

        return parsed

    def _handle_implicit_prerelease_bump(self, parsed: semver.version.Version):
        old_parsed = parsed
        parsed = parsed.bump_prerelease()
        if parsed.prerelease == old_parsed.prerelease:
            parsed = parsed.replace(prerelease=f'{parsed.prerelease}.1')

        return parsed

    def _handle_implicit_build_bump(self: Self, parsed: semver.version.Version):
        old_parsed = parsed
        parsed = parsed.bump_build()
        if parsed.build == old_parsed.build:
            parsed = parsed.replace(build=f'{parsed.build}.1')

        return parsed

    def _handle_implicit_bump(self: Self, parsed: semver.version.Version, commits: list[str], prerelease: bool):
        if parsed.build:
            if prerelease:
                parsed = parsed.replace(build=None)

                if parsed.prerelease:
                    parsed = self._handle_implicit_prerelease_bump(parsed)
                else:
                    bump_type = self.bump_type(commits)
                    parsed = parsed.next_version(bump_type)
            else:
                parsed = self._handle_implicit_build_bump(parsed)
        elif parsed.prerelease:
            parsed = self._handle_implicit_prerelease_bump(parsed)
        else:
            parsed = parsed.replace(prerelease=None, build=None)
            bump_type = self.bump_type(commits)
            match bump_type:
                case 'major':
                    parsed = parsed.bump_major()
                case 'major':
                    parsed = parsed.bump_minor()
                # case "patch":
                #     parsed = parsed.bump_patch()
                case _:
                    parsed = parsed.bump_patch()

        return parsed

    def bump_version(
        self: Self,
        target: str | None = None,
        final_version: bool = False,
        prerelease: bool = False,
        prerelease_token: str | None = str(config.get('prerelease-token')),
        build: bool = False,
        build_token: str | None = str(config.get('build-token')),
    ) -> str:
        self._validate_target(target)

        current_version = self.commits.latest_version()
        # current_version = '0.1.14-dev.1'
        # current_version = "0.1.14-alpha.10+build.1"
        commits = self.commits.since(current_version)
        parsed = semver.Version.parse(current_version)

        if not prerelease:
            prerelease_token = None

        if not build:
            build_token = None

        if target and semver.Version.is_valid(target):
            parsed = semver.Version.parse(target)

            if parsed.prerelease:
                prerelease = False
                prerelease_token = None
            if parsed.build:
                build = False
                build_token = None

        # elif target in {"major", "minor", "patch"}:
        elif target:
            # parsed = parsed.replace(prerelease=None, build=None)
            # parsed = parsed.next_version(target)
            parsed = self._handle_target(parsed, target)

        else:
            parsed = self._handle_implicit_bump(parsed, commits, prerelease)

        if prerelease and prerelease_token:
            parsed = self._handle_prerelease(parsed, prerelease_token)

        if build and build_token:
            parsed = self._handle_build(parsed, build_token)

        if final_version:
            # parsed = parsed.replace(prerelease=None, build=None)
            parsed = parsed.finalize_version()

        return str(parsed)


def bump(
    target: str | None = None,
    final_version: bool = False,
    prerelease: bool = False,
    prerelease_token: str | None = str(config.get('prerelease-token')),
    build: bool = False,
    build_token: str = str(config.get('build-token')),
) -> str:
    bumper = VersionBumper()
    new_version = bumper.bump_version(
        target=target,
        final_version=final_version,
        prerelease=prerelease,
        prerelease_token=prerelease_token,
        build=build,
        build_token=build_token,
    )
    return new_version


def latest() -> str:
    bumper = VersionBumper()
    return bumper.commits.latest_version()


# Example PEP 440 Version Ordering (from smallest to largest):
# 1.0.dev1 < 1.0a1 < 1.0a2 < 1.0b1 < 1.0rc1 < 1.0 < 1.0.post1 < 1.0.post2 < 1.0+build.1

# SemVer Version Ordering (from smallest to largest):
# 1.0.0-dev.1 < 1.0.0-alpha.1 < 1.0.0-alpha.2 < 1.0.0-beta.1 < 1.0.0-beta.2 < 1.0.0-rc.1 <
# 1.0.0 = 1.0.0+post.1 = 1.0.0+build.456
