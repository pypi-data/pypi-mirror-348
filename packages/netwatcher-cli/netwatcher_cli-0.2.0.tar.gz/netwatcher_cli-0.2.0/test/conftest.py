"""Shared test fixtures for Netwatcher CLI unit tests."""

from socket import AddressFamily, SocketKind
from unittest.mock import MagicMock, patch

import pytest
from psutil import CONN_ESTABLISHED

from netwatcher_cli.ip_api_client import IPApiResponse, Settings
from netwatcher_cli.rconn import ProcessInfo, RemoteConnection


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


@pytest.fixture
def mock_connection() -> list[tuple]:
    """Fixture that returns a mock `psutil` connection response for testing.

    Returns:
        list[tuple]: A mock connection matching the `psutil.net_connections` format (fd, family, type, laddr, raddr,
            status, pid).
    """
    return [
        (
            42,
            AddressFamily.AF_INET,
            SocketKind.SOCK_STREAM,
            MagicMock(ip="192.168.1.2", port=12345),
            MagicMock(ip="93.184.216.34", port=80),
            CONN_ESTABLISHED,
            9999,
        )
    ]


@pytest.fixture
def mock_remote_connection_map(mock_connection: list[tuple]) -> dict[str, RemoteConnection]:
    """Fixture that returns a map from mock IP addresses to mock `RemoteConnection`s.

    Returns:
        dict[str, RemoteConnection]: Map from mock IP addresses to mock `RemoteConnection`s.
    """
    with (
        patch("netwatcher_cli.rconn.net_connections", return_value=mock_connection),
        patch.object(ProcessInfo, "from_pid", return_value=None),
    ):
        return RemoteConnection.get_remote_connection_map()
