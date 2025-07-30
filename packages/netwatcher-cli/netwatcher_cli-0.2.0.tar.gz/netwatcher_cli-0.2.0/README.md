# NetWatcher CLI

[![PyPI version](https://badge.fury.io/py/netwatcher-cli.svg)](https://pypi.org/project/netwatcher-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**NetWatcher CLI** monitors outbound network connections on your local machine and enriches them with IP geolocation and
ownership data to help identify potentially suspicious processes.

### Example Output

```text
┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ IP      ┃ Geolocation     ┃ Ownership          ┃ Threat Level ┃ Assessment              ┃ Process Info            ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 8.8.8.8 │ City, State Zip │ - ISP: Example ISP │ Suspicious   │ - Hosting provider      │ - Executable Path: …    │
│         │ Country         │ - Org: Example Org │              │ - Proxy or VPN detected │ - Command Line: …       │
│         │                 │ - AS: ASEXAMPLE    │              │ ...                     │ - Process Name: sus.exe │
│         │                 │ - AS Name: EX      │              │                         │ - PID: 1234             |
└─────────┴─────────────────┴────────────────────┴──────────────┴─────────────────────────┴─────────────────────────┘
...
```

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
- [License](#license)

## Features

- View geolocation and BGP table details about remote internet connections.
- Retrieve process information associated with each connection.
- Flag reasons to suspect possibly malicious activity.
- Optionally generate threat assessment as HTML report.
- Optionally output logs to disk.

## Installation

Install from [PyPI](https://pypi.org/project/netwatcher-cli):

```bash
pip install netwatcher-cli
```

## Usage

See the Typer-generated [docs](docs/cli.md) for the full CLI usage reference.

## Development

1. Install `uv`:

   To manage dependencies and install **NetWatcher CLI** efficiently, use **uv**. You can install `uv`
   ([here](https://docs.astral.sh/uv/getting-started/installation/)).

2. Install Python >= 3.9:

```bash
uv python install 3.13
```

3. Create a virtual environment and activate it:

```bash
uv venv --python 3.13

# macOS and Linux
source .venv/activate/bin

# Windows
.venv\Scripts\activate
```

4. Install dependencies:

```bash
uv pip install -r pyproject.toml --all-extras
```

5. Run unit tests

```bash
# -s allows print() output
# -vvv increases verbosity
uv run pytest -s -vvv
```

6. Run pre-commit (requires **git-cliff**, see [Changelog Generation](#changelog-generation) for more)

```bash
# This runs formatters, linters, type checks (Pyright), secret scanners, and doc generators.
uv run pre-commit run --all-files
```

### Changelog Generation

This project uses [`git-cliff`](https://git-cliff.org/docs/) to generate changelogs automatically based on conventional
commit messages. To use or update the changelog, you must have `git-cliff` installed locally or in your CI environment.
You can do this via cargo, the Rust package manager (which you can install
[here](https://www.rust-lang.org/tools/install)):

```bash
cargo install git-cliff
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
