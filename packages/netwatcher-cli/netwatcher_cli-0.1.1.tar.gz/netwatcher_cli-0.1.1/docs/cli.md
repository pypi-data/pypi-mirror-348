# NetWatcher

NetWatcher CLI - Monitor outbound network connections.

**Usage**:

```console
$ netwatcher [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `scan`: Scan IP addresses using IP-API with...
* `version`: Print the installed version of the package.

## `netwatcher scan`

Scan IP addresses using IP-API with configurable logging and language support.

Args:
    country_code (str): User&#x27;s ISO 3166-1 alpha-2 two-leter country code. Defaults to `US`.
    html_dir (Path | None): Optional directory location for which to write an HTML report. Defaults to `None`.
    ip_api_lang (str): Language code for the IP API response. Defaults to `en`.
    log_dir (Path | None): Optional directory location for which to write a log file. Defaults to `None`.
    verbose (int): Verbosity level (-v, -vv, -vvv). Defaults to 0.

**Usage**:

```console
$ netwatcher scan [OPTIONS]
```

**Options**:

* `-c, --country-code TEXT`: User&#x27;s ISO 3166-1 alpha-2 two-leter country code.  [default: US]
* `--html-dir PATH`: Optional directory location for which to write an HTML report.
* `--lang TEXT`: Language code for the IP API response.  [default: en]
* `--log-dir PATH`: Optional directory location for which to write a log file.
* `-v, --verbose`: Increase verbosity (-v, -vv, -vvv)  [default: 1]
* `--help`: Show this message and exit.

## `netwatcher version`

Print the installed version of the package.

**Usage**:

```console
$ netwatcher version [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.
