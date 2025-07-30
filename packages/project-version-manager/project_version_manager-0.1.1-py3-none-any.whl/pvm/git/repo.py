import logging
from pathlib import Path

from git import GitCommandError, Repo

repo_path: Path = Path('.')

logger = logging.getLogger('pvm:git')

repo: Repo | None = None

try:
    repo = Repo(repo_path)
except GitCommandError:
    repo = None


def is_git_repo() -> bool:
    return repo is not None and repo.bare is False


def clone(repo_url, to_path=None):
    to_path = to_path or repo_path
    try:
        global repo
        repo = Repo.clone_from(repo_url, to_path)
        logger.info(f'Cloned repo from {repo_url} to {to_path}')
    except GitCommandError as e:
        logger.error(f'Clone failed: {e}')


def status():
    global repo
    if repo:
        return repo.git.status()
    logger.error('Repository not loaded.')


def add(items: list[str] | None = None):
    if items is None:
        items = ['.']

    global repo
    if repo:
        repo.index.add(items)
        # repo.git.add(items)
        logger.info(f'Added: {items}')


def commit(message):
    global repo
    if repo:
        try:
            repo.index.commit(message)
            logger.info(f'Committed: {message}')
        except GitCommandError as e:
            logger.error(f'Commit failed: {e}')


def push(remote_name='origin', branch='main'):
    global repo
    if repo:
        try:
            remote = repo.remote(name=remote_name)
            remote.push(refspec=branch)
            logger.info(f'Pushed to {remote_name}/{branch}')
        except GitCommandError as e:
            logger.error(f'Push failed: {e}')


def pull(remote_name='origin', branch='main'):
    global repo
    if repo:
        try:
            remote = repo.remote(name=remote_name)
            remote.pull(branch)
            logger.info(f'Pulled from {remote_name}/{branch}')
        except GitCommandError as e:
            logger.error(f'Pull failed: {e}')


def current_branch():
    global repo
    if repo:
        return repo.active_branch.name
    logger.error('No active branch.')
    return None


def log(max_count=5):
    global repo
    if repo:
        return repo.git.log('--oneline', f'-n {max_count}')
    logger.error('Repository not loaded.')
    return None


def tag(version: str, push: bool = False, prefix: str = 'v', repo_path: str | Path = '.') -> None:
    """Tag the version in the Git repository."""
    global repo
    tag_name = f'{prefix}{version}'
    if repo:
        if repo.is_dirty():
            logger.warning('[!] Repository has uncommitted changes.')
        repo.create_tag(f'{tag_name}')

        logger.info(f'[*] Git tag created: {tag_name}')

        if push and 'origin' in repo.remotes:
            repo.remotes.origin.push()
            repo.remotes.origin.push(tag_name)
            logger.debug(f'[+] Git tag pushed to remote: {tag_name}')
        else:
            logger.debug('[+] Git tag not pushed. Use --push to push the tag.')


def latest_tag(path='.'):
    # global repo

    if repo and repo.tags:
        latest_tag = repo.git.describe(tags=True, abbrev=0)
        return latest_tag
    return None


def latest_tag_by_date(path='.'):
    if repo and repo.tags:
        tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
        return tags[-1].name if tags else None

    return None
