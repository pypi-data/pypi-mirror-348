"""Shared test fixtures for Netwatcher CLI unit tests."""

import pytest

from netwatcher.ip_api_client import IPApiResponse, Settings


@pytest.fixture
def mock_batch_ip_data() -> list[dict[str, str]]:
    """Gets a mock API response.

    Returns:
        list[dict[str, str]]: A simulated IP-API batch JSON endpoint response.
    """
    return [
        {
            "status": "success",
            "country": "United States",
            "countryCode": "US",
            "regionName": "California",
            "city": "Mountain View",
            "isp": "Google LLC",
            "org": "Google LLC",
            "asname": "GOOGLE",
            "mobile": "false",
            "proxy": "false",
            "hosting": "false",
            "query": "8.8.8.8",
        },
        {
            "status": "fail",
            "country": "Australia",
            "countryCode": "AU",
            "regionName": "New South Wales",
            "city": "Sydney",
            "isp": "Cloudflare",
            "org": "Cloudflare",
            "asname": "CLOUDFLARENET",
            "mobile": "true",
            "proxy": "true",
            "hosting": "true",
            "query": "1.1.1.1",
        },
    ]


@pytest.fixture
def mock_ip_api_responses(mock_batch_ip_data: list[dict[str, str]]) -> list[IPApiResponse]:
    """Return a list of validated IPApiResponse objects for testing.

    Args:
        mock_batch_ip_data (list[dict[str, str]]): Mock batch IP data.

    Returns:
        list[IPApiResponse]: List of validated IPApiResponse objects for testing.
    """
    return [IPApiResponse.model_validate(entry) for entry in mock_batch_ip_data]


@pytest.fixture
def mock_settings() -> Settings:
    """Fixture that returns a default `Settings` object..

    Returns:
        Settings: A settings object configured for testing.
    """
    return Settings()
