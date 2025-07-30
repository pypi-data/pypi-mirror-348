# import os
# from pathlib import Path

# from git import GitCommandError, Repo

# from pvm.git.tag_manager import TagManager


# class Git:
#     def __init__(self, repo_path):
#         self.repo_path = repo_path
#         if os.path.exists(repo_path):
#             try:
#                 self.repo = Repo(repo_path)
#                 print(f"Repo loaded from: {repo_path}")
#             except GitCommandError as e:
#                 print(f"Failed to load repo: {e}")
#         else:
#             self.repo = None

#     def clone(self, repo_url, to_path=None):
#         to_path = to_path or self.repo_path
#         try:
#             self.repo = Repo.clone_from(repo_url, to_path)
#             print(f"Cloned repo from {repo_url} to {to_path}")
#         except GitCommandError as e:
#             print(f"Clone failed: {e}")

#     def status(self):
#         if self.repo:
#             return self.repo.git.status()
#         return "Repository not loaded."

#     def add(self, file_pattern='.'):
#         if self.repo:
#             self.repo.git.add(file_pattern)
#             print(f"Added: {file_pattern}")

#     def commit(self, message):
#         if self.repo:
#             try:
#                 self.repo.index.commit(message)
#                 print(f"Committed: {message}")
#             except GitCommandError as e:
#                 print(f"Commit failed: {e}")

#     def push(self, remote_name='origin', branch='main'):
#         if self.repo:
#             try:
#                 remote = self.repo.remote(name=remote_name)
#                 remote.push(refspec=branch)
#                 print(f"Pushed to {remote_name}/{branch}")
#             except GitCommandError as e:
#                 print(f"Push failed: {e}")

#     def pull(self, remote_name='origin', branch='main'):
#         if self.repo:
#             try:
#                 remote = self.repo.remote(name=remote_name)
#                 remote.pull(branch)
#                 print(f"Pulled from {remote_name}/{branch}")
#             except GitCommandError as e:
#                 print(f"Pull failed: {e}")

#     def current_branch(self):
#         if self.repo:
#             return self.repo.active_branch.name
#         return "No active branch."

#     def log(self, max_count=5):
#         if self.repo:
#             return self.repo.git.log('--oneline', f'-n {max_count}')
#         return "Repository not loaded."


# def tag(version: str, push: bool = False, prefix: str = 'v', repo_path: str | Path = '.') -> None:
#     """Tag the version in the Git repository."""
#     tag_manager = TagManager(repo_path)
#     tag_manager.tag(version, push, prefix)
