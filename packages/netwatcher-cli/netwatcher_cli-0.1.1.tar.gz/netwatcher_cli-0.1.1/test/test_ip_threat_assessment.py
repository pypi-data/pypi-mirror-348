"""Unit tests for IPThreatAssessment model and logic."""

import pytest

from netwatcher_cli.ip_api_client import IPApiResponse
from netwatcher_cli.ip_threat_assessment import IPThreatAssessment


def get_mock_reasons() -> list[list[str]]:
    """Return mock reason lists for testing IP threat assessment output.

    Returns:
        list[list[str]]: A list containing:
            - An empty list representing a non-suspicious IP.
            - A list of sample threat reasons representing a suspicious IP.
    """
    return [
        [],
        [
            "Lookup failed",
            "Proxy or VPN detected",
            "Hosting provider or data center",
            "Mobile network",
            "IP origin country (AU) is different from user's country (US)",
        ],
    ]


@pytest.mark.usefixtures("mock_ip_api_responses")
def test_get_reasons_returns_expected_threat_flags(mock_ip_api_responses: list[IPApiResponse]) -> None:
    """Test that get_reasons returns correct threat indicators for different IP inputs.

    Args:
        mock_ip_api_responses (list[IPApiResponse]): Mock IP API responses.
    """
    no_threat_data_raw, threat_data_raw = mock_ip_api_responses
    no_threat_data = IPApiResponse.model_validate(no_threat_data_raw)
    threat_data = IPApiResponse.model_validate(threat_data_raw)

    expected_no_threat, expected_threat = get_mock_reasons()

    no_threat_result = IPThreatAssessment.get_reasons(no_threat_data, country_code="US")
    threat_result = IPThreatAssessment.get_reasons(threat_data, country_code="US")

    assert no_threat_result == expected_no_threat
    assert threat_result == expected_threat


@pytest.mark.usefixtures("mock_ip_api_responses")
def test_from_batch_ip_data_returns_enriched_assessments(mock_ip_api_responses: list[IPApiResponse]) -> None:
    """Test that from_batch_ip_data properly flags IPs and includes correct reasons.

    Args:
        mock_ip_api_responses (list[IPApiResponse]): Mock IP API responses.
    """
    assessments = IPThreatAssessment.from_batch_ip_data(mock_ip_api_responses, country_code="US")
    expected_reasons = get_mock_reasons()

    assert len(assessments) == 2

    # First IP should not be suspicious
    assert assessments[0].is_suspicious is False
    assert assessments[0].reasons == expected_reasons[0]

    # Second IP should be flagged
    assert assessments[1].is_suspicious is True
    assert assessments[1].reasons == expected_reasons[1]
