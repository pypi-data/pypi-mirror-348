"""Monitor outbound network connections and fetch IP geolocation data."""

import asyncio
from pathlib import Path
from typing import Annotated

from loguru import logger
from typer import Exit, Option, Typer

from .ip_api_client import IPApiClient, Iso639LanguageCode, Settings
from .ip_threat_assessment import IPThreatAssessment
from .logging_config import setup_logging
from .rconn import RemoteConnection
from .ui import IPTableRenderer

app = Typer()


@app.command()
def scan(
    country_code: Annotated[
        str, Option("-c", "--country-code", help="User's ISO 3166-1 alpha-2 two-leter country code.")
    ] = "US",
    html_dir: Annotated[
        Path | None, Option(help="Optional directory location for which to write an HTML report.")
    ] = None,
    ip_api_lang: Annotated[str, Option("--lang", help="Language code for the IP API response.")] = "en",
    log_dir: Annotated[Path | None, Option(help="Optional directory location for which to write a log file.")] = None,
    verbose: Annotated[int, Option("-v", "--verbose", count=True, help="Increase verbosity (-v, -vv, -vvv)")] = 1,
) -> None:
    """Scan IP addresses using IP-API with configurable logging and language support.

    Args:
        country_code (str, optional): User's ISO 3166-1 alpha-2 two-leter country code. Defaults to `US`.
        html_dir (Path | None, optional): Optional directory location for which to write an HTML report. Defaults to
            `None`.
        ip_api_lang (str, optional): Language code for the IP API response. Defaults to `en`.
        log_dir (Path | None, optional): Optional directory location for which to write a log file. Defaults to `None`.
        verbose (int, optional): Verbosity level (-v, -vv, -vvv). Defaults to 0.
    """
    setup_logging(log_dir=log_dir, verbose=verbose)

    logger.info(
        f"Initializing scan with country_code={country_code}, html_dir={html_dir}, ip_api_lang={ip_api_lang}, "
        f"log_dir={log_dir}, verbose={verbose}"
    )

    try:
        iso_language_code = Iso639LanguageCode(ip_api_lang)
        settings = Settings(country_code=country_code, html_dir=html_dir, ip_api_lang=iso_language_code)
    except ValueError as e:
        logger.error("Invalid language: {language}. Must be one of: {[i.value for i in Iso639LanguageCode]}")
        raise Exit(code=1) from e

    logger.info("Getting remote connections.")
    remote_conn_map = RemoteConnection.get_remote_connection_map()
    ips = list(remote_conn_map)

    if not ips:
        logger.warning("No established connections to remote IP addresses found. Exiting.")
        raise Exit()

    logger.info(f"Querying IP-API for {len(ips)} IPs")
    batch_ip_data = asyncio.run(IPApiClient.managed_fetch_batch_ip_data(ips, settings))
    if not batch_ip_data:
        logger.error("Fetching IP geolocation data yielded no results.")
        raise Exit(code=1)

    ip_threat_assessments = IPThreatAssessment.from_batch_ip_data(
        remote_conn_map, batch_ip_data, country_code=settings.country_code
    )
    renderer = IPTableRenderer(html_dir=settings.html_dir, max_cmdline_display=settings.max_cmdline_display)
    renderer.render(ip_threat_assessments)
