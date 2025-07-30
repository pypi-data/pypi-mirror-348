"""Asynchronous HTTP client for querying the IP-API batch JSON endpoint."""

from asyncio import gather
from enum import Enum
from pathlib import Path
from types import TracebackType
from typing import Self

from httpx import AsyncClient, HTTPError
from loguru import logger
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from pydantic_settings import BaseSettings
from yarl import URL


class Iso639LanguageCode(str, Enum):
    """ISO 639 language codes supported by the IP-API service."""

    EN = "en"
    DE = "de"
    ES = "es"
    PTBR = "pt-BR"
    FR = "fr"
    JA = "ja"
    ZHCN = "zh-CN"
    RU = "ru"


class Settings(BaseSettings):
    """Configuration settings for interacting with the IP-API batch endpoint.

    Attributes:
        country_code (str, optional): User's ISO 3166-1 alpha-2 two-leter country code. Defaults to `US`.
        fields (int | str, optional): Fields to return in the response. Defaults to bitmask for all including `status,
            message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,
            offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query` (66846719).
        html_dir (Path | None, optional): Optional directory location for which to write an HTML report. Defaults to
            `None`.
        ip_api_batch_json_base_url (URL, optional): Base URL for the batch JSON endpoint. Defaults to
            `http://ip-api.com/batch`
        ip_api_lang (Iso639LanguageCode, optional): Language code for localizing response messages. Defaults to `EN`.
        max_batch_size (int, optional): Maximum number of IP addresss in the query to the IP-API batch endpoint before
            rate-limiting occurs. Defaults to 100.
        max_cmdline_display (int, optional): Maximum number of command line arguments to display for the process in the
            table. Defaults to 5.
        max_queries (int, optional): Maximum number of batched queries sent to the IP-API batch endpoint before
            rate-limiting occurs. Defaults to 15 (per minute).
        timeout (float, optional): Timeout (in seconds) for the HTTP requests. Defaults to 5.0
    """

    country_code: str = "US"
    fields: int | str = 66846719
    html_dir: Path | None = None
    ip_api_batch_json_base_url: URL = URL("http://ip-api.com/batch")
    ip_api_lang: Iso639LanguageCode = Iso639LanguageCode.EN
    max_batch_size: int = 100
    max_cmdline_display: int = 5
    max_queries: int = 15
    timeout: float = 5.0

    def get_ip_api_batch_json_url(self) -> str:
        """Construct the full IP-API batch endpoint URL with query parameters.

        Returns:
            str: Fully formatted URL with `fields` and `ip_api_lang` parameters applied.
        """
        url = self.ip_api_batch_json_base_url.update_query({"fields": self.fields, "lang": self.ip_api_lang.value})
        return str(url)


class IPApiResponse(BaseModel):
    """Schema for a single IP-API batch response entry."""

    model_config = ConfigDict(populate_by_name=True, validate_assignment=True, validate_by_name=True)

    status: str | None = None
    message: str | None = None
    continent: str | None = None
    continent_code: str | None = Field(default=None, alias="continentCode")
    country: str | None = None
    country_code: str | None = Field(default=None, alias="countryCode")
    region: str | None = None
    region_name: str | None = Field(default=None, alias="regionName")
    city: str | None = None
    district: str | None = None
    zip: str | None = None
    lat: float | None = None
    lon: float | None = None
    timezone: str | None = None
    offset: int | None = None
    currency: str | None = None
    isp: str | None = None
    org: str | None = None
    as_: str | None = Field(default=None, alias="as")
    asname: str | None = None
    reverse: str | None = None
    mobile: bool | None = None
    proxy: bool | None = None
    hosting: bool | None = None
    query: str | None = None


class IPApiClient:
    """Asynchronous HTTP client for querying the IP-API batch endpoint."""

    def __init__(self, settings: Settings) -> None:
        """Initialize the client with a settings object.

        Args:
            settings (Settings): Configuration for the client.
        """
        self.client = AsyncClient(timeout=settings.timeout)
        self.settings = settings

    async def __aenter__(self) -> Self:
        """Enter the asynchronous context manager.

        Returns:
            Self: The IPApiClient instance, ready to use in an async context.
        """
        return self

    async def __aexit__(
        self, _exc_type: type[BaseException] | None, _exc_val: BaseException | None, _exc_tb: TracebackType | None
    ) -> None:
        """Exit the asynchronous context manager, ensuring the client is closed."""
        await self.aclose()

    async def aclose(self) -> None:
        """Close the underlying HTTP client to release resources."""
        logger.debug("Closing HTTP client session.")
        await self.client.aclose()

    async def fetch_single_batch(self, batch: list[str]) -> list[IPApiResponse]:
        """Perform a single batch geolocation lookup.

        Args:
            batch (list[str]): Batch of IP addresses to look up.

        Returns:
            list[IPApiResponse]: Parsed API responses.
        """
        url = self.settings.get_ip_api_batch_json_url()
        logger.debug(f"Sending batch IP request to {url} with {len(batch)} IPs.")

        try:
            response = await self.client.post(url, json=batch)
            response.raise_for_status()
            results = response.json()

            if not isinstance(results, list):
                err_msg = "Unexpected response format from IP API."
                logger.error(err_msg)
                raise HTTPError(err_msg)

            parsed = []
            for item in results:
                try:
                    parsed.append(IPApiResponse.model_validate(item))
                except ValidationError as e:
                    logger.warning(f"Skipping invalid response item {item}: {e}")
            return parsed

        except HTTPError as e:
            logger.warning(f"HTTPError for {getattr(e.request, 'url', 'unknown')}: {e}")
            return []

    async def fetch_batch_ip_data(self, ips: list[str]) -> list[IPApiResponse]:
        """Fetch geolocation data in concurrent batches in accordance with rate limits.

        Args:
            ips (list[str]): Collection of IP addresses.

        Returns:
            list[IPApiResponse]: Parsed API responses.
        """
        batches = [ips[i : i + self.settings.max_batch_size] for i in range(0, len(ips), self.settings.max_batch_size)]
        if len(batches) > 45:
            logger.warning(
                f"Only sending the first {self.settings.max_queries} batches of {self.settings.max_batch_size} IP "
                f"addresses each out of {len(batches)} batches."
            )
        logger.info(f"Processing {len(batches)} IP batches concurrently.")
        batch_responses = await gather(*(self.fetch_single_batch(batch) for batch in batches))
        flattened_batch_responses = [response for batch in batch_responses for response in batch]
        logger.info(f"Fetched {len(flattened_batch_responses)} valid IP responses.")
        return flattened_batch_responses

    @classmethod
    async def managed_fetch_batch_ip_data(cls, ips: list[str], settings: Settings) -> list["IPApiResponse"]:
        """Fetch geolocation data for IP addresses encapsulating asynchronous context management.

        Args:
            ips (list[str]): A list of IP addresses to query.
            settings (Settings): Configuration settings for the IP-API client.

        Returns:
            list[IPApiResponse]: List of parsed responses from the IP-API batch JSON post request.
        """
        async with IPApiClient(settings) as client:
            return await client.fetch_batch_ip_data(ips)
