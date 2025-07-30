from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import git
from jinja2 import Template

from pvm.git.comparison_links import GitComparisonLinks
from pvm.git.utils import format_commit_message

logger = logging.getLogger('pvm:changelog')

# 🔖 Constant: Keep a Changelog Jinja2 template
TEMPLATE_STR = """# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
{% for section, items in unreleased.items() if items %}
### {{ section }}
{% for item in items %}
- {{ item }}{% endfor %}
{% endfor %}
{% for log in changelogs %}## [{{ log.version }}] - {{ log.date.isoformat() }}
{% for section, items in log.changes.items() if items %}
### {{ section }}
{% for item in items %}
- {{ item }}{% endfor %}
{% endfor %}
{% endfor %}
{% if comparison_links %}
{{ comparison_links }}
{% endif %}
"""


# 🧱 Data Model (Changelog Structure)
@dataclass
class Changelog:
    # version: Version
    # version: semver.Version
    version: str
    date: datetime.date  # type: ignore
    changes: dict[str, list[str]] = field(
        default_factory=lambda: {
            'Added': [],
            'Changed': [],
            'Fixed': [],
            'Removed': [],
            'Security': [],
            'Deprecated': [],
            'Uncategorized': [],
        }
    )

    def add_change(self, section: str, message: str) -> None:
        if section not in self.changes:
            self.changes['Uncategorized'].append(message)
        else:
            self.changes[section].append(message)


# ⚙️ Generator (Logic Controller)
class Generator:
    def __init__(self, repo_path: str = '.'):
        self.repo_path = repo_path
        self.repo = git.Repo(repo_path)
        self.tags = sorted(self.repo.tags, key=lambda t: t.commit.committed_datetime)
        self.changelogs: list[Changelog] = []
        self.unreleased = Changelog(version='0.0.0', date=datetime.today().date())

    def categorize_commit(self, message: str) -> str:
        msg = message.strip().lower()
        if msg.startswith('feat:'):
            return 'Added'
        elif msg.startswith('fix:'):
            return 'Fixed'
        elif msg.startswith(('change:', 'refactor:')):
            return 'Changed'
        elif msg.startswith('remove:'):
            return 'Removed'
        elif msg.startswith('security:'):
            return 'Security'
        elif msg.startswith('deprecate:'):
            return 'Deprecated'
        else:
            return 'Uncategorized'

    def parse_commits(self) -> None:
        if not self.tags:
            commits = list(self.repo.iter_commits())
            # for commit in self.commits:
            for commit in commits:
                section = self.categorize_commit(str(commit.message))
                msg = format_commit_message(str(commit.message).strip())
                self.unreleased.add_change(section, msg)
            return

        prev_commit: str | None = None
        changelogs: list[Changelog] = []
        for tag in self.tags:
            # version = Version(tag.name)
            # version = semver.Version.parse(tag.name)
            version = tag.name
            date = tag.commit.committed_datetime.date()
            current_commit = tag.commit.hexsha
            commits = list(
                self.repo.iter_commits(f'{prev_commit}..{current_commit}' if prev_commit else f'{current_commit}')
            )
            changelog = Changelog(version=version, date=date)

            for commit in commits:
                section = self.categorize_commit(str(commit.message).strip())
                msg = format_commit_message(str(commit.message).strip())
                changelog.add_change(section, msg)

            changelogs.append(changelog)
            prev_commit = current_commit

        if prev_commit:
            latest_commit = self.repo.head.commit.hexsha
            for commit in self.repo.iter_commits(f'{prev_commit}..{latest_commit}'):
                section = self.categorize_commit(str(commit.message).strip())
                msg = format_commit_message(str(commit.message).strip())
                self.unreleased.add_change(section, msg)

        changelogs.reverse()

        self.changelogs = changelogs

    def render_changelog(self) -> str:
        template: Template = Template(TEMPLATE_STR)
        return template.render(
            changelogs=self.changelogs,
            unreleased=self.unreleased.changes,
            comparison_links=self.generate_comparison_links(),
        )

    def generate_comparison_links(self) -> str:
        links = []
        git_comparer = GitComparisonLinks(self.repo_path)

        # Generate comparison links for all tags
        comparison_links = git_comparer.generate_all_tag_comparisons()

        for entry in comparison_links:
            links.append(f'[{entry["tag"]}]: {entry["link"]}')

        return '\n'.join(links)

    def write_changelog(self, output_path: str = 'CHANGELOG.md') -> None:
        self.parse_commits()

        content = self.render_changelog()
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(content, encoding='utf-8')
        logger.debug(f'[+] Changelog written to {output_path}')
