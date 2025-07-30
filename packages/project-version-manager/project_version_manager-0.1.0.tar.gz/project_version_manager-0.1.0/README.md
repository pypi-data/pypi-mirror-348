# PVM — Project Version Manager

**PVM** is a CLI tool for managing Python project versions using [Semantic Versioning 2.0.0](https://semver.org/). It automates version bumps, changelog generation, and Git tagging, all driven by your `pyproject.toml`.

## Content
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Show the Current Version](#show-the-current-version)
  - [Predict the Next Version](#predict-the-next-version)
  - [Bump the Version](#bump-the-version)
  - [Generate a Changelog](#generate-a-changelog)
- [CLI Reference](#cli-reference)
- [Example Workflows](#example-workflows)
- [Development](#development)
- [Configuration](#configuration)
- [Links](#links)
- [License](#license)


## Features

- **Semantic Versioning**: Bump major, minor, patch, prerelease, and build versions.
- **Git Integration**: Commit and tag version changes, with optional push.
- **Changelog Generation**: Automated changelog creation and updating.
- **Flexible CLI**: Powered by [Typer](https://typer.tiangolo.com/), with rich options.
- **Preserves Formatting**: Updates `pyproject.toml` without breaking formatting.


## Installation

```bash
pip install pvm
# or, with uv
uv pip install pvm
```

## Usage

### Show the Current Version

```bash
pvm show current
```

### Predict the Next Version

```bash
pvm show next
```

### Bump the Version

```bash
# Bump patch version (e.g., 1.2.3 → 1.2.4)
pvm bump patch

# Bump minor version and add prerelease
pvm bump minor --prerelease --prerelease-token rc

# Bump to a specific version
pvm bump 2.0.0

# Add build metadata
pvm bump patch --build --build-token build.5

# Bump and tag in Git (with prefix)
pvm bump patch --tag --tag-prefix v

# Bump and generate changelog
pvm bump patch --changelog --changelog-file CHANGELOG.md
```

### Generate a Changelog

```bash
pvm changelog --file CHANGELOG.md
```


## CLI Reference

| Command                  | Description                                      |
|--------------------------|--------------------------------------------------|
| `pvm --version`          | Show PVM CLI version                             |
| `pvm show current`       | Show current project version                     |
| `pvm show next`          | Predict next version                             |
| `pvm bump [target]`      | Bump version (target: major, minor, patch, etc.) |
| `pvm changelog`          | Generate or update changelog                     |

**Common Options for `bump`:**

- `--final`                 : Force a final version (no prerelease/build)
- `--prerelease, -p`        : Add a prerelease (e.g., alpha, beta, rc)
- `--prerelease-token`      : Set prerelease token (e.g., rc, alpha)
- `--build, -b`             : Add build metadata
- `--build-token`           : Set build metadata token
- `--tag, -t`               : Create a Git tag for the new version
- `--tag-prefix`            : Prefix for tag (default: `v`)
- `--changelog, -c`         : Generate changelog after bump
- `--changelog-file`        : Path to changelog file


## Example Workflows

**Bump patch, tag, and update changelog:**

```bash
pvm bump patch --tag --changelog --changelog-file CHANGELOG.md
```

**Show next prerelease version:**

```bash
pvm show next --prerelease
```


## Development

### Install Dev & Test Dependencies

```bash
uv sync --group dev --group test
```

### Run Tests

```bash
pytest
# or, for all environments:
tox
```

### Format, Lint, and Type-Check

```bash
uv run ruff format .
uv run ruff check --fix --exit-zero
uv run pre-commit run --all-files
uv run mypy .
```

## Configuration

PVM reads and writes the version from your `pyproject.toml`.
You can configure changelog file location and other options in your `pyproject.toml`.


## Links

- [Homepage](https://github.com/dazzymlv/pvm)
- [Source](https://github.com/dazzymlv/pvm.git)
- [Changelog](https://github.com/dazzymlv/pvm/CHANGELOG.md)
- [Issues](https://github.com/dazzymlv/pvm/issues)
- [Documentation](https://github.com/dazzymlv/pvm/README.md)


## License

MIT License © [Malvin Ndip](https://github.com/dazzymlv)
