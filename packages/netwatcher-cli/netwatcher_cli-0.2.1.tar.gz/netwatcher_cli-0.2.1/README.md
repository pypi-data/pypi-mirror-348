# NetWatcher CLI

[![PyPI version](https://badge.fury.io/py/netwatcher-cli.svg)](https://pypi.org/project/netwatcher-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/pfischer1687/netwatcher-cli/blob/main/LICENSE)

**NetWatcher CLI** monitors outbound network connections on your local machine and enriches them with IP geolocation and
ownership data to help identify potentially suspicious processes. See [example output](#example-output) below.

### Features

- Displays geolocation and BGP table details about remote internet connections.
- Retrieves process information associated with each connection.
- Flags reasons to suspect possibly malicious activity.
- Optionally generates threat assessment as HTML report.
- Optionally outputs serialized logs to disk.

See the [CLI docs](https://github.com/pfischer1687/netwatcher-cli/blob/main/docs/cli.md) for the full CLI usage
reference.

### Example Output

```text
┏━━━━━━━━━┳━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ IP      ┃ Geolocation     ┃ Ownership          ┃ Threat Level ┃ Assessment              ┃ Process Info            ┃
┡━━━━━━━━━╇━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 8.8.8.8 │ City, State Zip │ - ISP: Example ISP │ Suspicious   │ - Hosting provider      │ - Executable Path: …    │
│         │ Country         │ - Org: Example Org │              │ - Proxy or VPN detected │ - Command Line: …       │
│         │                 │ - AS: ASEXAMPLE    │              │ ...                     │ - Process Name: sus.exe │
│         │                 │ - AS Name: EX      │              │                         │ - PID: 1234             │
│         │                 │ ...                │              │                         │ ...                     │
└─────────┴─────────────────┴────────────────────┴──────────────┴─────────────────────────┴─────────────────────────┘
...
```

## Table of Contents

- [Installation](#installation)
- [Basic Usage](#usage)
- [Development](#development)
- [License](#license)

## Installation

Install from [PyPI](https://pypi.org/project/netwatcher-cli):

```bash
pip install netwatcher-cli
```

## Basic Usage

```console
$ nw scan [OPTIONS]
```

**Options**:

- `-c, --country-code TEXT`: User&#x27;s ISO 3166-1 alpha-2 two-leter country code. [default: US]
- `--html-dir PATH`: Optional directory location for which to write an HTML report.
- `--lang TEXT`: Language code for the IP API response. [default: en]
- `--log-dir PATH`: Optional directory location for which to write a log file.
- `-v, --verbose`: Increase verbosity (-v, -vv, -vvv) [default: 1]
- `--help`: Show this message and exit.

See the [CLI docs](https://github.com/pfischer1687/netwatcher-cli/blob/main/docs/cli.md) for the full CLI usage
reference.

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
uv run pytest [OPTIONS]
```

Some useful options:

- `-s` – allows `print()` output
- `-vvv` – increases verbosity

See the [pytest docs](https://docs.pytest.org/en/stable/) for full usage and configuration details.

6. Run pre-commit (requires **git-cliff**, see [Changelog Generation](#changelog-generation) for more) to run the
   formatter/linter (Ruff), type checker (Pyright), doc generators (Typer/git-cliff), etc.

```bash
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

This project is licensed under the MIT License. See the
[LICENSE](https://github.com/pfischer1687/netwatcher-cli/blob/main/LICENSE) file for more details.
