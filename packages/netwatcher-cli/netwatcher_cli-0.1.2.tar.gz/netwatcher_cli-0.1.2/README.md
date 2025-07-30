# NetWatcher

**NetWatcher** is a lightweight network connection monitoring tool written in Python. It helps you track active outbound
connections on your system, monitor associated processes, and provides geolocation information for remote IP addresses.

This tool is designed for:

- Developers monitoring network traffic.
- Security-conscious users detecting unauthorized network connections.
- Anyone interested in inspecting live network connections and associated processes.

## Features

- Monitor active network connections.
- View details about local and remote connections (IP address, port).
- Retrieve process information associated with each connection (PID, process name).
- Geolocation lookup for remote IP addresses.
- Lightweight and fast CLI tool built with **Typer**.
- Uses **uv**, the fast Python package and project manager, to manage dependencies and execution.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [CLI Usage](#cli-usage)
- [Configuration](#configuration)
- [License](#license)

## Installation

### Install with `uv`

1. **Install `uv`**:

   To manage dependencies and install **NetWatcher** efficiently, use **uv**. First, install `uv` if you haven't already
   ([instructions](https://docs.astral.sh/uv/getting-started/installation/)).

### From Source

1. Clone the repository:

   ```bash
   git clone https://github.com/pfischer1687/netwatcher.git
   cd netwatcher
   ```

2. Install Python 3.13:

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

5. Run the script:

```bash
uv run nw scan
```

## Usage

### CLI Usage

The primary interface for NetWatcher is a command-line tool that can be executed with the following command:

```bash
uv run nw scan
```

This will scan active network connections and output the following information:

- Local IP and Port: The local endpoint of the connection.
- Remote IP and Port: The external endpoint the local process is connected to.
- Process Name (PID): The name and PID of the process using the connection.
- Geolocation Information: The city, region, and country of the remote IP.

## For Developers

### Running Tests

```bash
# -s allows print() output
# -vvv increases verbosity
uv run pytest -s -vvv
```

### Changelog Generation

This project uses [`git-cliff`](https://git-cliff.org/docs/) to generate changelogs automatically based on conventional
commit messages. To use or update the changelog, you must have `git-cliff` installed locally or in your CI environment.
You can do this via cargo, the Rust package manager (which you can install
[here](https://www.rust-lang.org/tools/install)):

```bash
cargo install git-cliff
```

### Run All Pre-Commit Hooks

```bash
# This runs formatters, linters, type checks (Pyright), secret scanners, and doc generators.
uv run pre-commit run --all-files
```

## Configuration

By default, NetWatcher uses the `ipapi` service for IP geolocation lookups. If you need to change the geolocation
service or provide your own API key, you can modify the `ip_lookup.py` file.

### Configure a Custom Geolocation Service

To use a different geolocation service, update the httpx API call in `ip_lookup.py` to integrate with your preferred
provider. Ensure the response format remains consistent.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

NetWatcher is a tool for monitoring active network connections with ease, using a simple and extensible design. Whether
you're troubleshooting, securing your network, or just curious about what's happening on your machine, NetWatcher makes
network monitoring simple and accessible.
