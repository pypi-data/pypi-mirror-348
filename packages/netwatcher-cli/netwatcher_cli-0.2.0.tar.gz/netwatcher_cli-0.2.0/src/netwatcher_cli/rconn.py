"""Provides models for inspecting remote network connections and associated process metadata."""

from ipaddress import IPv4Address, IPv6Address, ip_address
from socket import AddressFamily, SocketKind
from typing import Any, NamedTuple

from psutil import CONN_ESTABLISHED, Process, net_connections
from pydantic import BaseModel


class Addr(NamedTuple):
    """Represents a local or remote network address."""

    ip: str
    port: int


class Sconn(NamedTuple):
    """Represents a socket connection with metadata.

    Attributes:
        fd (int): File descriptor.
        family (AddressFamily): Address family (e.g., AF_INET).
        type (SocketKind): Socket type (e.g., SOCK_STREAM).
        laddr (Addr): Local address.
        raddr (Addr): Remote address.
        status (str): Connection status (e.g., ESTABLISHED).
        pid (int): Process ID associated with the connection.
    """

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


class ProcessInfo(BaseModel):
    """Represents metadata about a process.

    Attributes:
        cmdline (list[str]): Command-line arguments used to start the process.
        exe (str): Path to the executable.
        name (str): Name of the executable.
        pid (int): Process ID.
        parent_name (str | None, optional): Name of the parent process. Defaults to `None`.
        parent_pid (int | None, optional): PID of the parent process. Defaults to `None`.
    """

    cmdline: list[str]
    exe: str
    name: str
    pid: int
    parent_name: str | None = None
    parent_pid: int | None = None

    @classmethod
    def from_pid(cls, pid: int) -> "ProcessInfo | None":
        """Extract process metadata from a PID.

        Args:
            pid (int): The process ID.

        Returns:
            ProcessInfo | None: Metadata about the process, `None` if it is not running.
        """
        try:
            proc = Process(pid)

            if not proc.is_running():
                return None

            with proc.oneshot():
                cmdline = proc.cmdline()
                exe = proc.exe()
                name = proc.name()
                parent = proc.parent()
                parent_name = parent.name() if parent else None
                parent_pid = parent.pid if parent else None

        except Exception:
            return None

        return cls(cmdline=cmdline, exe=exe, name=name, pid=pid, parent_name=parent_name, parent_pid=parent_pid)


class RemoteConnection(BaseModel):
    """Represents an established remote network connection."""

    local_ip: IPv4Address | IPv6Address
    local_port: int
    remote_ip: IPv4Address | IPv6Address
    remote_port: int
    status: str
    process_info: ProcessInfo | None = None

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
            local_port=conn.laddr.port,
            remote_ip=remote_ip,
            remote_port=conn.raddr.port,
            status=conn.status,
            process_info=ProcessInfo.from_pid(conn.pid),
        )

    @classmethod
    def get_remote_connection_map(cls) -> dict[str, "RemoteConnection"]:
        """Gets map from remote IP addresses to corresponding `RemoteConnection`s with process metadata.

        Returns:
            dict[str, RemoteConnection]: Map from remote IP address to `RemoteConnection`.
        """
        conns = net_connections(kind="inet")
        rconn_map: dict[str, RemoteConnection] = {}

        for raw_conn in conns:
            conn = RemoteConnection.from_psutil(raw_conn)
            if conn:
                rconn_map[str(conn.remote_ip)] = conn

        return rconn_map
