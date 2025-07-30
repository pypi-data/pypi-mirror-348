"""Unit tests for the IPApiClient asynchronous HTTP client."""

from unittest.mock import MagicMock, patch

import pytest

from netwatcher_cli.ip_api_client import IPApiClient, IPApiResponse, Settings


@pytest.mark.asyncio
@pytest.mark.usefixtures("mock_ip_api_responses", "mock_settings")
async def test_fetch_batch_ip_data(mock_ip_api_responses: list[IPApiResponse], mock_settings: Settings) -> None:
    """Test `IPApiClient.fetch_batch_ip_data` with a valid successful response.

    Args:
        mock_ip_api_responses (list[IPApiResponse]): Mock IP API responses.
        mock_settings (Settings): A fixture providing configuration for the API client.

    Asserts:
        - The response list contains exactly two entries.
        - Each entry is an instance of `IPApiResponse`.
        - The expected IP addresses and country values are returned correctly.
    """
    ips = ["8.8.8.8", "1.1.1.1"]

    mock_post_response = MagicMock()
    mock_post_response.status_code = 200
    mock_post_response.json.return_value = mock_ip_api_responses
    mock_post_response.raise_for_status = MagicMock()

    client = IPApiClient(mock_settings)

    with patch("httpx.AsyncClient.post", return_value=mock_post_response):
        results = await client.fetch_batch_ip_data(ips)

    assert len(results) == 2
    assert all(isinstance(r, IPApiResponse) for r in results)
    assert results[0].query == "8.8.8.8"
    assert results[1].country == "Australia"

    await client.aclose()
