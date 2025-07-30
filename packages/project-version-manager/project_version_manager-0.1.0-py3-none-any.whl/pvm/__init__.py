from pathlib import Path

from pvm.pyproject import PyProject

BASE_DIR = Path(__file__).resolve().parent.parent.parent

__version__ = PyProject(BASE_DIR / 'pyproject.toml').version
