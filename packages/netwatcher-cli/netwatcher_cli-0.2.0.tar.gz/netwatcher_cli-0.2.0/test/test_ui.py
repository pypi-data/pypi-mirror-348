"""Test NetWatcher CLI IP table renderer."""

import pytest

from netwatcher_cli.ip_api_client import IPApiResponse
from netwatcher_cli.rconn import ProcessInfo
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


@pytest.mark.parametrize(
    "process_info, expected_pid_info",
    [
        (
            None,
            "",
        ),
        (
            ProcessInfo(
                cmdline=["/usr/bin/python3", "app.py", "--flag", "value"],
                exe="/usr/bin/python3",
                name="python",
                pid=12345,
                parent_name="init",
                parent_pid=1,
            ),
            "- Executable Path: /usr/bin/python3\n"
            "- Command Line: /usr/bin/python3 app.py --flag value\n"
            "- Process Name: python\n"
            "- PID: 12345\n"
            "- Parent Name: init\n"
            "- Parent PID: 1",
        ),
    ],
)
def test_get_process_info(process_info: ProcessInfo | None, expected_pid_info: str) -> None:
    """Test that the process information is formatted correctly.

    Args:
        process_info (ProcessInfo | None): Parameterized process information.
        expected_pid_info (str): Parameterized correctly formatted process information.
    """
    ip_table_renderer = IPTableRenderer()
    pid_info = ip_table_renderer.get_process_info(process_info=process_info)
    assert pid_info == expected_pid_info
