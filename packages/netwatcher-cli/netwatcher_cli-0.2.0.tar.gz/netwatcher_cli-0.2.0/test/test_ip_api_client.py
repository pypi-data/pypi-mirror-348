"""Unit tests for the IPApiClient asynchronous HTTP client."""

from unittest.mock import MagicMock, patch

import pytest
from httpx import AsyncClient

from netwatcher_cli.ip_api_client import IPApiClient, IPApiResponse, Settings


@pytest.mark.asyncio
@pytest.mark.usefixtures("mock_ip_api_responses", "mock_settings")
async def test_managed_fetch_batch_ip_data_single_batch(
    mock_ip_api_responses: list[IPApiResponse], mock_settings: Settings
) -> None:
    """Tests `IPApiClient.managed_fetch_batch_ip_data` returns a valid result from a single batch."""
    ips = ["8.8.8.8", "1.1.1.1"]

    mock_post_response = MagicMock()
    mock_post_response.status_code = 200
    mock_post_response.json.return_value = mock_ip_api_responses
    mock_post_response.raise_for_status = MagicMock()

    with patch.object(AsyncClient, "post", return_value=mock_post_response):
        results = await IPApiClient.managed_fetch_batch_ip_data(ips, mock_settings)

    assert len(results) == 2
    assert all(isinstance(r, IPApiResponse) for r in results)
    assert results[0].query == "8.8.8.8"
    assert results[1].country == "Australia"


@pytest.mark.asyncio
async def test_managed_fetch_batch_ip_data_multiple_batches() -> None:
    """Tests that multiple batches are created and processed when input exceeds batch size."""
    total_ips = 250
    max_batch_size = 100
    expected_batch_calls = 3

    mock_ips = ["8.8.8.8"] * total_ips
    mock_response = IPApiResponse(query="8.8.8.8")
    settings = Settings(max_batch_size=max_batch_size)

    with patch.object(IPApiClient, "fetch_single_batch", return_value=[mock_response]) as mock_method:
        await IPApiClient.managed_fetch_batch_ip_data(mock_ips, settings)

    assert mock_method.call_count == expected_batch_calls
