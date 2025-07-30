import logging
import re
from datetime import date

logger = logging.getLogger('pvm:changelog')


def update_changelog(changelog_path: str, version: str):
    """Update the changelog file by replacing the '## [Unreleased]' section with the new version and date."""
    logger.info('[i] Updating changelog...')
    with open(changelog_path, encoding='utf-8') as f:
        changelog = f.read()

    today = date.today().strftime('%Y-%m-%d')

    # Step 1: Update Unreleased header
    changelog = re.sub(
        r'^## \[Unreleased\]', f'## [Unreleased]\n\n## [{version}] - {today}', changelog, count=1, flags=re.M
    )

    # Step 2: Find repo_url and compare path
    unreleased_link = re.search(
        r'^\[unreleased\]:\s*(.+?)/(compare|-/compare)/', changelog, re.IGNORECASE | re.MULTILINE
    )
    if not unreleased_link:
        logger.error('[+] Repository URL could not be detected.')
        return
    repo_url, compare_path = unreleased_link.groups()

    # Step 3: Find first existing version in links (after [unreleased])
    version_links = re.findall(r'^\[([^\]]+?)\]:\s*.+$', changelog, re.MULTILINE)
    previous_version = None
    for v in version_links:
        if v.lower() != 'unreleased':
            previous_version = v
            break

    if not previous_version:
        logger.error('[+] No previous version found.')
        return

    # Detect prefix style from previous_version
    prefix_match = re.match(r'^(v)?(.+)$', previous_version)
    if prefix_match:
        prefix = prefix_match.group(1) or ''
        clean_prev_version = prefix_match.group(2)

        def tag(v):
            return f'{prefix}{v}'

        # Step 4: Update [unreleased] link
        changelog = re.sub(
            r'^\[unreleased\]:\s*.+$',
            # f'[unreleased]: {repo_url}/{compare_path}/{tag(version)}...HEAD',
            f'[unreleased]: {repo_url}/{compare_path}/{version}...HEAD',
            changelog,
            flags=re.MULTILINE | re.IGNORECASE,
        )

        # Step 5: Insert new version link reference before previous_version's line
        changelog = re.sub(
            rf'^(\[{re.escape(previous_version)}\]: .+)',
            # f'[{version}]: {repo_url}/{compare_path}/{tag(clean_prev_version)}...{tag(version)}\n\\1',
            f'[{version}]: {repo_url}/{compare_path}/{tag(clean_prev_version)}...{version}\n\\1',
            changelog,
            flags=re.MULTILINE,
        )

    with open(changelog_path, 'w', encoding='utf-8') as f:
        f.write(changelog)
