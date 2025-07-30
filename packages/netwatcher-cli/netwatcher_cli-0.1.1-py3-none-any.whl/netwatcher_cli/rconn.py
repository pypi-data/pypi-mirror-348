"""Provides a model to represent remote network connections including IP parsing and connection filtering."""

from ipaddress import IPv4Address, IPv6Address, ip_address
from socket import AddressFamily, SocketKind
from typing import Any, NamedTuple

from psutil import CONN_ESTABLISHED, net_connections
from pydantic import BaseModel


class Addr(NamedTuple):
    """Represents a local or remote network address."""

    ip: str
    port: int


class Sconn(NamedTuple):
    """Represents a socket connection."""

    fd: int
    family: AddressFamily
    type: SocketKind
    laddr: Addr
    raddr: Addr
    status: str
    pid: int

    @classmethod
    def from_psutil(cls, raw: Any) -> "Sconn | None":
        """Deserialize socket connection from `psutil` connection.

        Args:
            raw (Any): `psutil` connection.

        Returns:
            Sconn | None: Deserialized socket connection if input is valid, else `None`.
        """
        try:
            conn = cls(*raw)
        except Exception:
            return None

        # PID will likely be present for an established remote connection
        if conn.pid is None:
            return None

        if not (conn.laddr and hasattr(conn.laddr, "ip") and hasattr(conn.laddr, "port")):
            return None
        if not (conn.raddr and hasattr(conn.raddr, "ip") and hasattr(conn.raddr, "port")):
            return None
        if not isinstance(conn.laddr.port, int) or not isinstance(conn.raddr.port, int):
            return None

        try:
            ip_address(conn.laddr.ip)
            ip_address(conn.raddr.ip)
        except ValueError:
            return None

        return conn


class RemoteConnection(BaseModel):
    """Represents a remote network connection."""

    local_ip: IPv4Address | IPv6Address
    local_port: int
    pid: int
    remote_ip: IPv4Address | IPv6Address
    remote_port: int
    status: str

    @classmethod
    def from_psutil(cls, raw: Any) -> "RemoteConnection | None":
        """Deserialize socket connection from `psutil` connection if it is an established remote connection.

        Args:
            raw (Any): `psutil` connection.

        Returns:
            RemoteConnection | None: Deserialized remote network connection if input is an established remote
                connection, else `None`.
        """
        conn = Sconn.from_psutil(raw)

        if conn is None or conn.status != CONN_ESTABLISHED:
            return None

        remote_ip = ip_address(conn.raddr.ip)
        if not remote_ip.is_global:
            return None

        return cls(
            local_ip=ip_address(conn.laddr.ip),
            pid=conn.pid,
            local_port=conn.laddr.port,
            remote_ip=remote_ip,
            remote_port=conn.raddr.port,
            status=conn.status,
        )


def get_remote_connections() -> list[RemoteConnection]:
    """Get established remote network connections.

    Returns:
        list[RemoteConnection]: List of established remote network connections.
    """
    conns = net_connections(kind="inet")
    validated_remote_connections = []

    for conn in conns:
        validated_conn = RemoteConnection.from_psutil(conn)
        if validated_conn is not None:
            validated_remote_connections.append(validated_conn)

    return validated_remote_connections
