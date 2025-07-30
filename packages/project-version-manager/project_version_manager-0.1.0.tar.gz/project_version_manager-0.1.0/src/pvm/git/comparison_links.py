import logging
from urllib.parse import quote

from git import Repo

logger = logging.getLogger('pvm:git')


class GitComparisonLinks:
    def __init__(self, repo_path, remote_name='origin'):
        """Initialize the GitComparisonLinks class with the path to the Git repository.

        Args:
            repo_path (str): Path to the local Git repository.
            remote_name (str): Name of the remote repository (default is 'origin').

        """
        self.repo_path = repo_path
        self.remote_name = remote_name
        self.repo = Repo(repo_path)

        if self.repo.bare:
            raise ValueError('The provided repository is bare.')

        # Get the remote URL
        self.remote_url = self._get_remote_url()

    def _get_remote_url(self) -> str:
        """Get the remote repository URL and normalize it for comparison link generation."""
        remote_url = self.repo.remotes[self.remote_name].url

        # Normalize GitHub/GitLab-style HTTPS or SSH URLs
        if remote_url.startswith('git@'):
            # git@github.com:user/repo.git -> https://github.com/user/repo
            remote_url = remote_url.replace(':', '/').replace('git@', 'https://')
        elif remote_url.startswith('http'):
            pass
        else:
            raise ValueError('Unsupported remote URL format.')

        # Remove trailing `.git` if present
        if remote_url.endswith('.git'):
            remote_url = remote_url[:-4]

        return remote_url

    def generate_comparison_link(self, base_ref, compare_ref) -> str:
        """Generate a comparison URL between two tags (or commits, branches).

        Args:
            base_ref (str): The base ref (e.g., 'v1.0').
            compare_ref (str): The compare ref (e.g., 'v2.0').

        Returns:
            str: A URL to view the comparison on the Git remote (GitHub/GitLab).

        """
        # Encode refs in case they contain special characters
        base_ref_encoded = quote(base_ref, safe='')
        compare_ref_encoded = quote(compare_ref, safe='')

        # GitHub/GitLab comparison path
        compare_url = f'{self.remote_url}/compare/{base_ref_encoded}...{compare_ref_encoded}'

        return compare_url

    def generate_all_tag_comparisons(self) -> list[dict[str, str]]:
        """Generate comparison links for all tags in the repository, sorted such that the latest tag appears at the top.

        The format follows:
        - [unreleased]: compares the latest tag to HEAD
        - [first tag]: links to the tag itself
        - [other tags]: compares previous tag to current tag

        Returns:
            list: A list of dictionaries with tags and comparison URLs.

        """
        tags = list(self.repo.tags)
        # tags = [tag for tag in self.repo.tags]

        if len(tags) < 1:
            logger.warning('[!] No tags found in the repository.')
            return []

        tags_sorted = sorted(tags, key=lambda tag: tag.commit.committed_date)

        comparison_links = []

        # Generate comparison links between consecutive tags
        for i in range(1, len(tags_sorted)):
            prev_tag = tags_sorted[i - 1].name
            curr_tag = tags_sorted[i].name
            comparison_links.append({'tag': f'{curr_tag}', 'link': self.generate_comparison_link(prev_tag, curr_tag)})

        comparison_links.reverse()

        # First tag has no previous version; link to its release page
        first_tag = tags_sorted[0].name
        comparison_links.append({'tag': f'{first_tag}', 'link': f'{self.remote_url}/releases/tag/{first_tag}'})

        # Add [unreleased] comparing the latest tag to HEAD
        latest_tag = tags_sorted[-1].name
        comparison_links.insert(0, {'tag': 'unreleased', 'link': self.generate_comparison_link(latest_tag, 'HEAD')})

        return comparison_links
