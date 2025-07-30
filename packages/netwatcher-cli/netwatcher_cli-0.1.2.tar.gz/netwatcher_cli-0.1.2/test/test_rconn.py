"""Test NetWatcher CLI network connection monitoring."""

from ipaddress import IPv4Address
from socket import AddressFamily, SocketKind
from unittest.mock import MagicMock, patch

import psutil

from netwatcher_cli.rconn import RemoteConnection, get_remote_connections


def get_mock_connection() -> list[tuple]:
    """Returns mock psutil connection response for testing.

    Returns:
        list[tuple]: A mock connection matching the psutil.net_connections format.
    """
    return [
        (
            42,  # fd
            AddressFamily.AF_INET,
            SocketKind.SOCK_STREAM,
            MagicMock(ip="192.168.1.2", port=12345),  # laddr
            MagicMock(ip="93.184.216.34", port=80),  # raddr
            psutil.CONN_ESTABLISHED,
            9999,  # pid
        )
    ]


def test_get_remote_connections_returns_valid_models() -> None:
    """Tests that `netwatcher_cli.rconn.get_remote_connections` returns a list of `RemoteConnection` instances."""
    mock_conn = get_mock_connection()

    with patch("netwatcher_cli.rconn.net_connections", return_value=mock_conn):
        remote_conns = get_remote_connections()

    assert isinstance(remote_conns, list)
    assert len(remote_conns) == 1

    conn = remote_conns[0]
    assert isinstance(conn, RemoteConnection)
    assert conn.local_ip == IPv4Address("192.168.1.2")
    assert conn.remote_ip == IPv4Address("93.184.216.34")
    assert conn.pid == 9999
    assert conn.status == psutil.CONN_ESTABLISHED
