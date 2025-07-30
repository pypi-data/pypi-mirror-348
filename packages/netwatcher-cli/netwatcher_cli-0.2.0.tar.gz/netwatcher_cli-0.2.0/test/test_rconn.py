"""Test `RemoteConnection` and network connection parsing logic."""

from ipaddress import IPv4Address
from socket import AddressFamily, SocketKind
from unittest.mock import MagicMock

import psutil
import pytest

from netwatcher_cli.rconn import RemoteConnection


def get_mock_connection() -> list[tuple]:
    """Returns mock psutil connection response for testing.

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
            psutil.CONN_ESTABLISHED,
            9999,
        )
    ]


@pytest.mark.usefixtures("mock_remote_connection_map")
def test_get_remote_connection_map(mock_remote_connection_map: dict[str, RemoteConnection]) -> None:
    """Tests that `RemoteConnection.get_remote_connection_map` returns a map from IPs to `RemoteConnection`s."""
    assert isinstance(mock_remote_connection_map, dict)
    assert len(mock_remote_connection_map) == 1

    conn = mock_remote_connection_map["93.184.216.34"]

    assert isinstance(conn, RemoteConnection)
    assert conn.local_ip == IPv4Address("192.168.1.2")
    assert conn.local_port == 12345
    assert conn.remote_ip == IPv4Address("93.184.216.34")
    assert conn.remote_port == 80
    assert conn.status == psutil.CONN_ESTABLISHED
    assert conn.process_info is None
