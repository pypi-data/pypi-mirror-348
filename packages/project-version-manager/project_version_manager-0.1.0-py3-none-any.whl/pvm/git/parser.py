import logging

from git import GitCommandError, Repo

logger = logging.getLogger('pvm:git')


class CommitParser:
    def __init__(self, repo_path: str = '.', tag_prefix: str | None = 'v'):
        self.repo = Repo(repo_path)
        self.tag_prefix = tag_prefix or ''

    def strip_prefix(self, tag: str) -> str:
        return tag[len(self.tag_prefix) :] if self.tag_prefix and tag.startswith(self.tag_prefix) else tag

    def latest_version(self) -> str:
        try:
            tag = self.repo.git.describe(tags=True, abbrev=0)
            return self.strip_prefix(tag)
        except GitCommandError:
            return '0.0.0'

    def since(self, version: str) -> list[str]:
        try:
            tag = f'{self.tag_prefix}{version}'
            if tag in self.repo.tags:
                logs = self.repo.git.log(f'{tag}..HEAD', pretty='format:%s')
            else:
                logs = self.repo.git.log('HEAD', pretty='format:%s')
            return logs.splitlines() if logs else []
        except GitCommandError:
            return []
