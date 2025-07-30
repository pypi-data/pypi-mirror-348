"""Test NetWatcher CLI IP table renderer."""

import pytest

from netwatcher_cli.ip_api_client import IPApiResponse
from netwatcher_cli.ui import IPTableRenderer


@pytest.mark.usefixtures("mock_ip_api_responses")
def test_get_geolocation(mock_ip_api_responses: list[IPApiResponse]) -> None:
    """Test that geolocation formatting returns expected output.

    Args:
        mock_ip_api_responses (list[IPApiResponse]): Mock IP API responses.
    """
    geolocation = IPTableRenderer.get_geolocation(mock_ip_api_responses[0])
    expected_geolocation = "Mountain View\nUnited States"
    assert geolocation == expected_geolocation


@pytest.mark.usefixtures("mock_ip_api_responses")
def test_get_ownership(mock_ip_api_responses: list[IPApiResponse]) -> None:
    """Test that ownership formatting returns expected output.

    Args:
        mock_ip_api_responses (list[IPApiResponse]): Mock IP API responses.
    """
    ownership = IPTableRenderer.get_ownership(mock_ip_api_responses[0])
    expected_ownership = "- ISP: Google LLC\n- Organization: Google LLC\n- AS Name (RIR): GOOGLE"
    assert ownership == expected_ownership
